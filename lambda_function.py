import json
import logging
import urllib.request
import urllib.parse
import urllib.error
import base64
import os
from datetime import datetime, timezone

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Main Lambda handler for server down alerts
    Triggered by CloudWatch alarm via SNS
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Parse the SNS message from CloudWatch alarm
        alarm_data = parse_alarm_event(event)
        if not alarm_data:
            logger.error("Could not parse alarm data from event")
            return {'statusCode': 400, 'body': 'Invalid event format'}
        
        logger.info(f"Processing alarm for server: {alarm_data['server_name']}")
        
        # Get contact information from Google Sheets API
        contacts = get_contacts_from_sheets(alarm_data['server_name'])
        if not contacts:
            logger.warning(f"No contacts found for server: {alarm_data['server_name']}")
            return {'statusCode': 200, 'body': 'No contacts configured'}
        
        # Process server alert and make actual calls
        alert_results = process_server_alert_with_calls(contacts, alarm_data)
        
        # Log results
        logger.info(f"Alert processing results: {alert_results}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Server alert processed successfully',
                'server': alarm_data['server_name'],
                'team': alert_results.get('team', 'Unknown'),
                'contacts_found': len(contacts),
                'calls_initiated': alert_results.get('calls_initiated', 0),
                'escalation_time': alert_results.get('escalation_time', 5),
                'timestamp': alarm_data['timestamp']
            })
        }
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}

def parse_alarm_event(event):
    """
    Parse CloudWatch alarm data from SNS event
    """
    try:
        # If test event uses "event" wrapper, unwrap it
        if 'event' in event:
            event = event['event']

        if 'Records' in event and len(event['Records']) > 0:
            sns_message = json.loads(event['Records'][0]['Sns']['Message'])
        else:
            sns_message = event

        # Extract server name
        server_name = extract_server_name(sns_message.get('AlarmName', ''))

        # Add this log to see extracted server name
        logger.info(f"Extracted server name: '{server_name}' from AlarmName: '{sns_message.get('AlarmName', '')}'")

        alarm_data = {
            'alarm_name': sns_message.get('AlarmName', 'Unknown'),
            'server_name': server_name,
            'alarm_description': sns_message.get('AlarmDescription', ''),
            'new_state': sns_message.get('NewStateValue', 'ALARM'),
            'reason': sns_message.get('NewStateReason', ''),
            'timestamp': sns_message.get('StateChangeTime', datetime.now(timezone.utc).isoformat()),
            'region': sns_message.get('Region', 'unknown')
        }
        return alarm_data

    except Exception as e:
        logger.error(f"Error parsing alarm event: {str(e)}")
        return None


def extract_server_name(alarm_name):
    """
    Extracts the server name from CloudWatch alarm names.
    Handles flexible formats like:
        - "sns-test Server Down"
        - "SERVER is down"
    """
    if not alarm_name or not isinstance(alarm_name, str):
        return "unknown-server"

    name = alarm_name.strip()

    # Convert to lowercase for consistent matching
    lower_name = name.lower()

    # Remove common prefixes
    prefixes_to_remove = ["server:", "alarm:", "alert:"]
    for prefix in prefixes_to_remove:
        if lower_name.startswith(prefix):
            name = name[len(prefix):].strip()
            lower_name = name.lower()
            break

    # Remove common suffixes or extra words
    suffixes_to_remove = [" is down", " server down", "-down", "-alarm", "-alert"]
    for suffix in suffixes_to_remove:
        if lower_name.endswith(suffix):
            name = name[: -len(suffix)].strip()
            lower_name = name.lower()
            break

    # In case there's extra words like "is down" in the middle, take first word if needed
    # Optional: split by spaces and take first token (only if name looks long)
    if len(name.split()) > 1:
        # Take the first word that likely represents server name
        name = name.split()[0].strip()

    # Fallback
    if len(name) < 2:
        return "unknown-server"

    return name

def get_contacts_from_sheets(server_name):
    """
    Fetch contact information from Google Sheets via Apps Script Web API
    """
    try:
        # Google Apps Script Web App URL
        api_url = "https://script.google.com/macros/s/AKfycbzEmmqeoUyRjNGQYferubel0azlRBJIA2fsWijhbqC-WMpz-Llwoxxh75lKGHOZUFcJ/exec"
        
        # Build full URL with query parameters
        params = urllib.parse.urlencode({'server_name': server_name})
        full_url = f"{api_url}?{params}"
        
        logger.info(f"Fetching contacts from Google Sheets API: {full_url}")
        
        # Make the HTTP request with timeout
        req = urllib.request.Request(full_url)
        req.add_header('User-Agent', 'AWS Lambda Server Monitor')
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    logger.error(f"HTTP {response.status} error: {response.reason}")
                    return []
                data = response.read().decode('utf-8')
        except urllib.error.URLError as e:
            logger.error(f"Network error while connecting to Google Sheets API: {str(e)}")
            return []
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP error while connecting to Google Sheets API: {e.code} {e.reason}")
            return []

        # Log raw response for debugging
        logger.info(f"Raw response data: {data}")

        # Parse JSON response - handle edge cases
        try:
            parsed_response = json.loads(data)
            logger.info(f"Parsed response type: {type(parsed_response)}, value: {parsed_response}")

            # Handle different response types from Google Apps Script
            if isinstance(parsed_response, int):
                logger.warning(f"Google Sheets API returned integer: {parsed_response} (possibly an error code)")
                return []
            
            elif isinstance(parsed_response, str):
                logger.warning(f"Google Sheets API returned string: {parsed_response}")
                return []
            
            elif isinstance(parsed_response, dict):
                # Single record returned
                if 'error' in parsed_response:
                    logger.error(f"Google Sheets API returned error: {parsed_response['error']}")
                    return []
                records = [parsed_response]
                
            elif isinstance(parsed_response, list):
                # Multiple records returned
                records = parsed_response
                
            else:
                logger.error(f"Unexpected response type from API: {type(parsed_response)} - value: {parsed_response}")
                return []

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error from Google Sheets API response: {str(e)} - Raw data: {data}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error parsing JSON response: {str(e)} - Raw data: {data}")
            return []

        # Validate that we have a list of dictionaries
        if not isinstance(records, list):
            logger.error(f"Records is not a list after processing: {type(records)}")
            return []

        # Ensure all items in the list are dictionaries
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                logger.warning(f"Record at index {i} is not a dict: {record} (type: {type(record)})")
                # Remove invalid records
                records = [r for r in records if isinstance(r, dict)]
                break

        contacts = []
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                logger.warning(f"Skipping non-dict record at index {i}: {record} (type: {type(record)})")
                continue

            # Match server name (case-insensitive)
            record_server_name = record.get('Server Name', '').strip()
            if record_server_name.lower() == server_name.strip().lower():
                escalation_time = 5
                if record.get('Escalation Time (mins)'):
                    try:
                        escalation_time = max(1, int(record.get('Escalation Time (mins)')))
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid escalation time for {server_name}, using default 5 minutes")
                
                contact_info = {
                    'server_name': server_name,
                    'team': record.get('Team', 'Unknown'),
                    'primary_contact': record.get('Primary Contact', ''),
                    'primary_phone': clean_phone_number(record.get('Phone Number', '')),
                    'secondary_contact': record.get('Secondary Contact', ''),
                    'secondary_phone': clean_phone_number(record.get('Secondary Phone', '')),
                    'escalation_time': escalation_time
                }

                if contact_info['primary_contact'] and contact_info['primary_phone']:
                    contacts.append(contact_info)
                    logger.info(f"Added contact for server '{server_name}': {contact_info['primary_contact']}")
                else:
                    logger.warning(f"Skipping incomplete contact record for server '{server_name}': missing primary contact or phone")

        logger.info(f"Found {len(contacts)} valid contact records for server: {server_name}")
        return contacts

    except Exception as e:
        logger.error(f"Unexpected error fetching contacts from Google Sheets: {str(e)}")
        return []


def clean_phone_number(phone):
    """
    Clean and format phone number
    """
    if not phone:
        return None
    
    # Convert to string if it's a number
    if isinstance(phone, (int, float)):
        phone_str = str(int(phone))  # Convert to int first to remove decimals, then to string
        logger.info(f"Converted numeric phone {phone} to string: {phone_str}")
    else:
        phone_str = str(phone).strip()
    
    # Remove all non-digit characters except +
    cleaned = ''.join(char for char in phone_str if char.isdigit() or char == '+')
    
    if not cleaned:
        return None
    
    # Add country code if missing
    if not cleaned.startswith('+'):
        digits = ''.join(filter(str.isdigit, cleaned))
        if len(digits) == 10:
            cleaned = '+91' + digits  # Assume India number based on your location
        elif len(digits) == 11 and digits.startswith('1'):
            cleaned = '+' + digits
        else:
            logger.warning(f"Unusual phone number format: {phone} -> {cleaned}")
    
    # Basic validation
    digits_only = ''.join(filter(str.isdigit, cleaned))
    if len(digits_only) < 10 or len(digits_only) > 15:
        logger.warning(f"Invalid phone number length: {phone} -> {cleaned} (digits: {len(digits_only)})")
        return None
    
    return cleaned if cleaned else None

def process_server_alert_with_calls(contacts, alarm_data):
    """
    Process the server alert and make actual Twilio calls
    """
    results = {
        'server': alarm_data['server_name'],
        'team': 'Unknown',
        'escalation_time': 5,
        'calls_initiated': 0,
        'call_results': [],
        'alert_processed': True
    }
    
    if not contacts:
        logger.warning(f"No contacts found for server: {alarm_data['server_name']}")
        return results
    
    # Create the voice message
    voice_message = create_call_message(alarm_data)
    
    for contact in contacts:
        results['team'] = contact['team']
        results['escalation_time'] = contact['escalation_time']
        
        logger.info("=== MAKING EMERGENCY CALLS ===")
        logger.info(f"Server: {alarm_data['server_name']} (Team: {contact['team']})")
        logger.info(f"Status: DOWN since {alarm_data['timestamp']}")
        logger.info(f"Escalation time: {contact['escalation_time']} minutes")
        
        # Call primary contact immediately
        if contact['primary_contact'] and contact['primary_phone']:
            logger.info(f"📞 Calling Primary: {contact['primary_contact']} at {contact['primary_phone']}")
            call_result = make_twilio_call(
                to_number=contact['primary_phone'],
                message=voice_message,
                contact_name=contact['primary_contact'],
                contact_type='Primary'
            )
            results['call_results'].append(call_result)
            if call_result['success']:
                results['calls_initiated'] += 1
        
        # Note: In a real implementation, you'd want to schedule the secondary call
        # after escalation_time minutes using AWS Step Functions or similar
        # For now, we'll just make the call immediately with a note
        if contact['secondary_contact'] and contact['secondary_phone']:
            logger.info(f"📞 Calling Secondary: {contact['secondary_contact']} at {contact['secondary_phone']}")
            call_result = make_twilio_call(
                to_number=contact['secondary_phone'],
                message=voice_message,
                contact_name=contact['secondary_contact'],
                contact_type='Secondary'
            )
            results['call_results'].append(call_result)
            if call_result['success']:
                results['calls_initiated'] += 1
        
        logger.info("=== END EMERGENCY CALLS ===")
    
    return results

def make_twilio_call(to_number, message, contact_name, contact_type):
    """
    Make a call using Twilio API
    """
    try:
        # Get Twilio credentials from environment variables
        account_sid =  os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token =  os.environ.get('TWILIO_AUTH_TOKEN')
        from_number = os.environ.get('TWILIO_FROM_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            logger.error("Missing Twilio credentials in environment variables")
            return {
                'success': False,
                'contact_name': contact_name,
                'contact_type': contact_type,
                'phone': to_number,
                'error': 'Missing Twilio credentials'
            }
        
        # Twilio API endpoint
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls.json"
        
        # Create TwiML for text-to-speech with clearer settings
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" rate="slow" language="en-US">{message}</Say>
    <Pause length="3"/>
    <Say voice="alice" rate="slow" language="en-US">I will repeat this message.</Say>
    <Pause length="1"/>
    <Say voice="alice" rate="slow" language="en-US">{message}</Say>
    <Pause length="2"/>
    <Say voice="alice" rate="slow" language="en-US">Press any key to confirm you received this alert.</Say>
    <Gather input="dtmf" timeout="15" numDigits="1">
        <Say voice="alice" rate="slow">Thank you. Alert confirmed. Goodbye.</Say>
    </Gather>
    <Say voice="alice" rate="slow">No response received. Please check your servers immediately. Goodbye.</Say>
</Response>"""
        
        # Prepare the data for the POST request
        data = {
            'To': to_number,
            'From': from_number,
            'Twiml': twiml,
            'StatusCallback': '',  # Optional: Add webhook URL for call status
            'StatusCallbackEvent': 'completed',
            'StatusCallbackMethod': 'POST'
        }
        
        # Encode the data
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        
        # Create the request
        request = urllib.request.Request(url, data=encoded_data, method='POST')
        
        # Add authentication header
        auth_string = f"{account_sid}:{auth_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        request.add_header('Authorization', f'Basic {auth_b64}')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request.add_header('User-Agent', 'AWS Lambda Server Monitor')
        
        # Make the request
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                response_data = response.read().decode('utf-8')
                
                if response.status == 201:  # Twilio returns 201 for successful call creation
                    logger.info(f"✅ Call initiated successfully to {contact_name} ({contact_type}) at {to_number}")
                    
                    # Parse response to get call SID
                    try:
                        response_json = json.loads(response_data) if response_data.startswith('{') else {}
                        call_sid = response_json.get('sid', 'unknown')
                    except:
                        call_sid = 'unknown'
                    
                    return {
                        'success': True,
                        'contact_name': contact_name,
                        'contact_type': contact_type,
                        'phone': to_number,
                        'call_sid': call_sid,
                        'message': 'Call initiated successfully'
                    }
                else:
                    logger.error(f"❌ Twilio API error: HTTP {response.status} - {response_data}")
                    return {
                        'success': False,
                        'contact_name': contact_name,
                        'contact_type': contact_type,
                        'phone': to_number,
                        'error': f'HTTP {response.status}: {response_data}'
                    }
                    
        except urllib.error.HTTPError as e:
            error_response = e.read().decode('utf-8') if e.fp else str(e)
            logger.error(f"❌ HTTP error calling {contact_name}: {e.code} {e.reason} - {error_response}")
            return {
                'success': False,
                'contact_name': contact_name,
                'contact_type': contact_type,
                'phone': to_number,
                'error': f'HTTP {e.code}: {error_response}'
            }
            
        except urllib.error.URLError as e:
            logger.error(f"❌ Network error calling {contact_name}: {str(e)}")
            return {
                'success': False,
                'contact_name': contact_name,
                'contact_type': contact_type,
                'phone': to_number,
                'error': f'Network error: {str(e)}'
            }
            
    except Exception as e:
        logger.error(f"❌ Unexpected error making call to {contact_name}: {str(e)}")
        return {
            'success': False,
            'contact_name': contact_name,
            'contact_type': contact_type,
            'phone': to_number,
            'error': f'Unexpected error: {str(e)}'
        }

def create_call_message(alarm_data):
    """
    Create the voice message for emergency calls
    """
    server_name = alarm_data['server_name']
    timestamp_str = alarm_data['timestamp']
    
    # Parse timestamp to make it more readable
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        readable_time = dt.strftime('%B %d at %I:%M %p UTC')
    except:
        readable_time = timestamp_str
    
    message = f"""
    URGENT: Server Alert from AWS CloudWatch.
    Server {server_name} is currently down and requires immediate attention.
    The alert was triggered on {readable_time}.
    Please check your monitoring dashboard and take appropriate action immediately.
    This is an automated emergency call from your server monitoring system.
    """
    
    # Clean up the message - remove extra whitespace
    message = ' '.join(message.split())
    return message

# Keep the original function for backward compatibility and testing
def process_server_alert(contacts, alarm_data):
    """
    Process the server alert - log what would happen without actually making calls
    (Kept for backward compatibility and testing)
    """
    results = {
        'server': alarm_data['server_name'],
        'team': 'Unknown',
        'escalation_time': 5,
        'contacts_to_call': [],
        'alert_processed': True
    }
    
    if not contacts:
        logger.warning(f"No contacts found for server: {alarm_data['server_name']}")
        return results
    
    for contact in contacts:
        results['team'] = contact['team']
        results['escalation_time'] = contact['escalation_time']
        
        logger.info("=== ALERT ACTION REQUIRED ===")
        logger.info(f"Server: {alarm_data['server_name']} (Team: {contact['team']})")
        logger.info(f"Status: DOWN since {alarm_data['timestamp']}")
        logger.info(f"Escalation time: {contact['escalation_time']} minutes")
        logger.info("Contacts that would be called:")
        
        if contact['primary_contact'] and contact['primary_phone']:
            contact_info = {
                'name': contact['primary_contact'],
                'phone': contact['primary_phone'],
                'role': 'Primary',
                'escalation_delay': 0
            }
            results['contacts_to_call'].append(contact_info)
            logger.info(f"📞 Primary: {contact['primary_contact']} at {contact['primary_phone']}")
        
        if contact['secondary_contact'] and contact['secondary_phone']:
            contact_info = {
                'name': contact['secondary_contact'],
                'phone': contact['secondary_phone'],
                'role': 'Secondary',
                'escalation_delay': contact['escalation_time']
            }
            results['contacts_to_call'].append(contact_info)
            logger.info(f"📞 Secondary: {contact['secondary_contact']} at {contact['secondary_phone']} (after {contact['escalation_time']} mins)")
        
        logger.info("=== END ALERT ===")
    
    return results

# Utility functions for testing and maintenance

def test_google_sheets_connection():
    """
    Test function to verify Google Sheets API connectivity
    """
    try:
        contacts = get_contacts_from_sheets('test-server')
        return {'success': True, 'contacts_found': len(contacts)}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def test_server_alert_processing(server_name=None):
    """
    Test function to simulate server alert processing
    """
    try:
        test_server = server_name or 'prod-web-server'
        test_alarm = {
            'alarm_name': f'{test_server}-down',
            'server_name': test_server,
            'alarm_description': f'Test alert for {test_server}',
            'new_state': 'ALARM',
            'reason': 'Test simulation',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'region': 'us-east-1'
        }
        contacts = get_contacts_from_sheets(test_server)
        if contacts:
            results = process_server_alert(contacts, test_alarm)
            return {'success': True, 'results': results}
        else:
            return {'success': False, 'error': f'No contacts found for server: {test_server}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def test_twilio_call(phone_number, contact_name="Test Contact"):
    """
    Test function to make a test call using Twilio
    """
    test_alarm = {
        'server_name': 'test-server',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    
    message = create_call_message(test_alarm)
    result = make_twilio_call(
        to_number=phone_number,
        message=message,
        contact_name=contact_name,
        contact_type='Test'
    )
    
    return result

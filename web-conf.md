Nginx conf

```
server {
    listen 80;
    server_name domain.com your.domain.name;  # Change this to your actual domain or IP address

    location / {
        proxy_pass http://localhost:<port>;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

To avoid 504 gateway error, when object uploading not succeed

```
server {
        root /var/www/poc_node/poc_node_backend;
        server_name poc-node-api.taskgrids.com;
        client_max_body_size 0;
        location / {

                proxy_pass http://127.0.0.1:8004;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;

                # Increase timeouts
                proxy_read_timeout 3600;
                proxy_connect_timeout 3600;
                proxy_send_timeout 3600;

                # Buffer adjustments to avoid temporary file warnings
                proxy_buffers 8 16k;
                proxy_buffer_size 32k;
                proxy_busy_buffers_size 64k;

                # Optionally disable buffering for large responses
                proxy_buffering off;

        }

}
```


```
server {

        root /path/to/project/website;            # /var/www/project

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name your.domain.com;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri /index.html;
        }


        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/<your domain name>/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/<your domain name>/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        }

        server {
            if ($host = example.com.com) {
                return 301 https://$host$request_uri;
                }     # managed by Certbot        



        server_name bou.appdemoserver.com;

        listen 80;
        return 404; # managed by Certbot


}
```

```
sudo ln -s /etc/nginx/sites-available/app.conf sites-enabled/app.conf

sudo systemctl restart nginx
```


Apache Conf

```
<VirtualHost *:80>
    ServerAdmin webmaster@your-project.com
    ServerName your-project.com

    DocumentRoot /var/www/your-project/public

    ErrorLog ${APACHE_LOG_DIR}/your-project_error.log
    CustomLog ${APACHE_LOG_DIR}/your-project_access.log combined

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</VirtualHost>

<VirtualHost *:443>
    ServerAdmin webmaster@your-project.com
    ServerName your-project.com

    DocumentRoot /var/www/your-project/public

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/your-project.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/your-project.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/your-project.com/chain.pem

    <Directory /var/www/your-project/public>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/your-project_error.log
    CustomLog ${APACHE_LOG_DIR}/your-project_access.log combined
</VirtualHost>
```

```
sudo a2ensite your-project.conf

sudo systemctl restart apache2
```



SSL with let's encrypt

https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-22-04


```
sudo apt update
sudo apt install certbot python3-certbot-apache
```

```
cd /etc/apache2/sites-available
sudo certbot --apache
```

>select your domain

```
Output
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/your_domain/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/your_domain/privkey.pem
This certificate expires on 2022-07-10.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for your_domain to /etc/apache2/sites-available/your_domain-le-ssl.conf
Successfully deployed certificate for www.your_domain.com to /etc/apache2/sites-available/your_domain-le-ssl.conf
Congratulations! You have successfully enabled HTTPS on https:/your_domain and https://www.your_domain.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

To check the status of this service and make sure it’s active, run the following:

```
sudo systemctl status certbot.timer
```

To set the auto renewal process of SSL with certbot:
```
crontab -e

0 */12 * * * /usr/bin/certbot renew --quiet
```


To renew the certificate;

```
sudo certbot

>select domain for renewal
```



To delete certificate of any domain:

```
sudo certbot delete
```

> select your domain

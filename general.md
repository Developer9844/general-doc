https://www.inmotionhosting.com/support/website/ssl/lets-encrypt-ssl-ubuntu-with-certbot/

Nginx conf

```
# This is for backend to serve service
server {
    listen 80;
    server_name your.domain.name;  # Change this to your actual domain or IP address

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

```
# This is for frontend/static data serving
server {

        root /path/to/project/website;            # /var/www/project

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name example.com;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri /index.html;
        }


}
```

```
#If you want to redirect traffic directly from port 80 and dont want to add server name
server {

        listen 80;
        root /path/to/project;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;
        client_max_body_size 550M;

        location / {
                proxy_pass http://localhost:7000;
                proxy_http_version 1.1;
                proxy_connect_timeout 600s;
                proxy_read_timeout 600s;
                proxy_send_timeout 600s;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }
}
```

```
cd /etc/nginx
sudo ln -s /etc/nginx/sites-available/app.conf sites-enabled/app.conf

sudo systemctl restart nginx
```


Apache Conf

```
# This serves static pages
<VirtualHost *:80>
        ServerName app.example.com
        ServerAlias app.example.com
        #ServerAdmin webmaster@localhost
        DocumentRoot /var/www/project
        DirectoryIndex index.html index.htm
        <Directory /var/www/project/>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride All
                Order allow,deny
                allow from all
        </Directory>
        
        # Main location block
        <Location />
            # Try to serve the requested file, or fall back to index.html
            RewriteEngine On
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteCond %{REQUEST_FILENAME} !-d
            RewriteRule ^ /index.html [L]
        </Location>


        ErrorLog /path/to/log/app-error.log
        CustomLog /path/to/log/app-access.log combined

</VirtualHost>
```

```
<VirtualHost *:80>

    ServerName xyz.com
    ServerAdmin webmaster@localhost

    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/

    ErrorLog ${APACHE_LOG_DIR}/xyz.com.error.log
    CustomLog ${APACHE_LOG_DIR}/xyz.com.access.log combined

</VirtualHost>
```

```
sudo a2ensite app.conf

sudo systemctl restart apache2
```




At the time of this error in S&S backend project


```
npm install --save-dev typescript@^4.5.4
npx tsc
```


Sudo Permission issue
```
https://www.baeldung.com/linux/permissions-issues
```


To extract logs from index.txt file from 2024-04-10 00:00:00 to 2024-04-11 05:34:53 and store them in logs.txt, you can use the sed command. Here's how you can do it:

```
sed -n '/^2024-04-10 00:00:00/,/^2024-04-11 05:34:53/p' pm2-pet-dev-access.log > /home/ec2/pm2-dev-logs.txt
```

Start your Node.js project with PM2
```
pm2 start npm --name "your-app-name" -- start
```


To check the cron job
```
grep CRON /var/log/syslog | grep < string >
```


List the resources under VPC
```
aws ec2 describe-network-interfaces --filters Name=vpc-id,Values='vpc-0e4fd0830c9d94340' --query  'NetworkInterfaces[*].[AvailabilityZone, OwnerId, Attachment.InstanceId, PrivateIpAddresses[*].Association.PublicIp]'
```


Find Command
```
sudo find / -type f -size +10M -size -50M -exec ls -lah {} \; | awk '{print $1 " " $5 " - " $9}'
```

```
-rw-r--r-- 17M - /root/.cache/composer/files/laravel-frontend-presets/argon/e0d1a4ad6d042b61db124e2c353178e8350e7f9c.zip
-rw-r--r-- 16M - /root/.cache/composer/files/tecnickcom/tcpdf/4c717a74977c5a9cefdf65d4bf209327157fdf01.zip
-rw-r--r-- 39M - /boot/initrd.img-6.8.0-1017-aws
-rw------- 14M - /boot/vmlinuz-6.2.0-1012-aws
-rw------- 15M - /boot/vmlinuz-6.8.0-1017-aws
-rw-r--r-- 38M - /boot/initrd.img-6.2.0-1012-aws
-rw------- 15M - /boot/vmlinuz-6.8.0-1016-aws
-rw-r--r-- 39M - /boot/initrd.img-6.8.0-1016-aws
-rw------- 26M - /var/lib/snapd/snaps/amazon-ssm-agent_9565.snap
-rw------- 45M - /var/lib/snapd/snaps/snapd_22991.snap
-rw------- 39M - /var/lib/snapd/snaps/snapd_21759.snap
-rw------- 27M - /var/lib/snapd/snaps/amazon-ssm-agent_9881.snap
```



1. Font Detection in Images

To detect fonts in images, you can use:
- Adobe Photoshop & Illustrator: "Match Font" feature helps identify similar fonts.
- WhatTheFont (by MyFonts): Upload an image, and it suggests matching fonts.
- Font Squirrel Matcherator: Similar to WhatTheFont, used for font identification.
- DeepFont (by Adobe): Uses AI for font recognition.

2. Font Detection in PDFs

PDFs can have embedded fonts, which you can extract:
- Adobe Acrobat Pro: Go to File → Properties → Fonts to see embedded fonts.
- pdffonts (part of Poppler utilities): A command-line tool to list fonts used in a PDF.
- Extracting Text and OCR: If fonts are rasterized, tools like Tesseract OCR and font classifiers can help detect them.

3. AI-Based Font Recognition

For complex cases, machine learning models trained on font datasets can classify fonts. Open-source libraries like Tesseract, FontMatcher, or Adobe Sensei can assist.
Do you have a specific image or PDF you want to analyze?





docker buildx create --name multiarch --use || docker buildx use multiarch
docker buildx inspect --bootstrap
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t developer9844/custom-grafana-pgwatch:v11.4.8 \
  --push .
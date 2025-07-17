Reference:
https://psujit775.medium.com/how-to-install-multiple-php-versions-with-apache-on-ubuntu-b37cd23d3019#:~:text=To%20run%20multiple%20versions%20of%20PHP%20simultaneously%20on%20Apache%2C%20you,for%20a%20particular%20virtual%20host.


1. Install Apache2
```
sudo apt update

sudo apt install apache2 -y

sudo systemctl status apache2

sudo systemctl start apache2
```


2. Install PHP 8.x, PHP 7.x, 

```
sudo apt install software-properties-common -y

sudo add-apt-repository ppa:ondrej/php -y

sudo apt update -y

sudo apt install libapache2-mod-fcgid
```


To Install PHP 7.4
```
sudo apt install php7.4 php7.4-fpm php7.4-mysql libapache2-mod-php7.4 -y
```

To Install PHP 8.1
```
sudo apt install php8.1 php8.1-fpm php8.1-mysql libapache2-mod-php8.1 -y
```

To Install PHP 8.2
```
sudo apt install php8.2 php8.2-fpm php8.2-mysql libapache2-mod-php8.2 -y
```


Verify versions:
```
ls -la /var/run/php/
```


Some common extensions used by PHP applications.(Optional)
Make sure to replace 8.1 with the version you require.

```
sudo apt install php8.1-common php8.1-mysql php8.1-xml php8.1-xmlrpc php8.1-curl php8.1-gd php8.1-imagick php8.1-cli php8.1-dev php8.1-imap php8.1-mbstring php8.1-opcache php8.1-soap php8.1-zip php8.1-intl -y
```




3. Start PHP-FPM Services

PHP-FPM (FastCGI Process Manager) is an implementation of FastCGI, 
a protocol for interacting with a web server, which is designed to 
handle high loads and reduce the overhead of executing PHP scripts. 
It is typically used to improve the performance of PHP applications 
by allowing them to run as a separate process, rather than being run 
within the web server process itself.



```
sudo systemctl start php8.1-fpm

sudo systemctl status php8.1-fpm

sudo systemctl start php7.4-fpm

sudo systemctl status php7.4-fpm
```


4. Configure Apache2

```
sudo a2enmod actions fcgid alias proxy_fcgi

sudo systemctl restart apache2
```


Create apache conf file for your application

```
sudo vim /etc/apache2/sites-available/app.conf


<VirtualHost *:80>

    
    ServerName  demo.com
    ServerAlias www.demo.com
    DocumentRoot /var/www/app
    <Directory /var/www/app/>
            Options FollowSymLinks MultiViews
            AllowOverride All
            Order allow,deny
            allow from all
            Require all granted
    </Directory>
        <FilesMatch \.php>
            SetHandler "proxy:unix:/var/run/php/php8.1-fpm.sock|fcgi://localhost/"
        </FilesMatch>

    ErrorLog ${APACHE_LOG_DIR}/err-demo.com.log
    CustomLog ${APACHE_LOG_DIR}/demo.com.log combined
</VirtualHost>
```




Enable site using below command

```
sudo a2ensite app.conf
```


/var/www/demo-app >>

```
vim /var/www/app/info.php 

<?php
phpinfo();
?>
```


To remove PHP 7.4 and related packages from your system, you can use the following commands:

```
sudo apt purge php7.4 php7.4-fpm php7.4-mysql libapache2-mod-php7.4
sudo apt autoremove
```



========================================================================================================

<?php phpinfo(); ?>

User php-version setup

ln -s /usr/bin/php7.4 php

export PATH="$HOME"/<dir>:"$PATH"

php -v

"This method allows you to use different PHP versions for different projects without conflicts. 
Each project can have its own PHP version specified through the symbolic link and PATH modification, 
and this won't interfere with the default PHP version or other projects."


.htaccess

<<<

```
<FilesMatch "\.php$">
    SetHandler application/x-httpd-php74
</FilesMatch>

Header always set Access-Control-Allow-Origin "*"    
Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"    
Header always set Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type,Authorization, Accept"    
Header always set Access-Control-Allow-Credentials "true"
```

>>>

========================================================================================================

To set the PHP version 
```
sudo update-alternatives --list php

sudo update-alternatives --config php
```

---

Project running commands for php & Laravel
```
chmod -R 777 storage public bootstrap
chmod 777 storage/logs/laravel.log
```

Note:    
1. 
2. If the project was migrated then make sure their storage and existing media files are also uploaded in new server. 
3. Also, check the .htaccess file in the directory after code uploaded in the server.
4. Ensure the git branch with developer.
5. Make sure, all the files which we have given full permission 777 accessible my webapplication, so check each directory and files should have full permission.

```
composer install
php artisan config:cache
php artisan storage:link
npm install
```

```
npm run build
```

```
php artisan passport:install
```

The requested URL was not found on this server error in Angular(404 on refresh)

```
https://www.tektutorialshub.com/angular/the-requested-url-was-not-found-on-this-server-error-in-angular/
```

```
	RewriteEngine On
	# If an existing asset or directory is requested go to it as it is
	RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} -f [OR]
	RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} -d
	RewriteRule ^ - [L]
	 
	# If the requested resource doesn't exist, use index.html
	RewriteRule ^ /index.html
```


If you configure php.ini for php8.*-fpm, then you should restart the php-fpm service. Ex-
```
sudo systemctl restart php8.1-fpm
```


Some Common Error in PHP

ErrorException: fopen(/var/www/starwood/api/storage/app/public/signdoc/roller_shade_doc/signed_roller_shade_contract_1367.pdf): Failed to open stream: Permission deniedin /var/www/starwood/api/vendor/league/flysystem/src/Adapter/Local.php:157
 
ErrorException: chmod(): Operation not permittedin /var/www/starwood/api/vendor/league/flysystem/src/Adapter/Local.php:368
Solution: 
```
sudo chown -R www-data:www-data /var/www/php-project/storage
sudo chmod -R 777 /var/www/php-project/storage
sudo chmod -R 777 /var/www/php-project/bootstrap
```

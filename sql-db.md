For Root User Access MySQL(LOCALHOST);

```
SELECT user, host, authentication_string, plugin FROM mysql.user WHERE user = 'root';

ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'root123';

SHOW GRANTS FOR 'root'@'localhost';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;

FLUSH PRIVILEGES;
```

```
CREATE USER 'ankush'@'localhost' IDENTIFIED BY 'Anku$h9844.';
GRANT ALL PRIVILEGES ON demo.* TO 'ankush'@'localhost';
GRANT SELECT ON demo.* TO 'ankush'@'localhost';
FLUSH PRIVILEGES;
```

mysql -u user1 -p
mysql password localhost: ankush-katkurwar / Anku$h9844.

####################################################################################

CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON db_name.* TO 'username'@'%';


Note:  '%' it means, user can connect from any host/server



```
CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'%';
GRANT SELECT ON db_name.* TO 'user'@'%';
FLUSH PRIVILEGES;
```

#####################################################################################


Grant Permissions for Database Creation:
Grant the CREATE privilege to allow user2 to create databases:

~ GRANT CREATE ON *.* TO 'user2'@'localhost';


Grant Read-only Access to All Databases:
Grant read-only access (SELECT) to all existing databases:

~ GRANT SELECT ON *.* TO 'user2'@'localhost';

This grants SELECT privileges on all databases (*.*). 
If you want to restrict read-only access to a specific database (e.g., 'demo'), you can replace *.* with the specific database name:

~ GRANT SELECT ON demo.* TO 'user2'@'localhost';


~ FLUSH PRIVILEGES;

---
For Postgres User Access;
```
CREATE DATABASE <database_name>;

#you have to run this command for each database to protect the access from users other than authorized user
REVOKE CONNECT ON DATABASE <database_name> FROM PUBLIC;                

CREATE USER <username> WITH ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <username>;

postgres=>\c <database_name>
# You are now connected to database "<database_name>" as user "<username>".

GRANT ALL ON SCHEMA public TO <username>;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <username>;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO <username>;
```


Kill a postgresql session/connection

```
SELECT 
    pg_terminate_backend(pid) 
FROM 
    pg_stat_activity 
WHERE 
    -- don't kill my own connection!
    pid <> pg_backend_pid()
    -- don't kill the connections to other databases
    AND datname = 'database_name'
    ;
```

Before executing this query, you have to REVOKE the CONNECT privileges to avoid new connections:
```
REVOKE CONNECT ON DATABASE dbname FROM PUBLIC, username;
```

---

Notes:

- Database dump

Go to your directory where you want to save the dump file, and run below command;
```
mysqldump -h <hostname> -u username -p db_name > db_name.sql
```

- If below error occures, while importing db

ERROR 1227 (42000) at line 18: Access denied; you need (at least one of) the SUPER, SYSTEM_VARIABLES_ADMIN or SESSION_VARIABLES_ADMIN privilege(s) for this operation

Solution:
Remove the 3 lines below if they're there, or comment them out with -- :

At the start:
```
-- SET @@SESSION.SQL_LOG_BIN= 0;
-- SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

```

At the end:
```
-- SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;

```
Note that the comment characters are "dash dash space" including the space.





- How to import dump file?

```
mysql> create database db_name;
mysql> use db_name;
mysql> source dump_file.sql;   #in that case, we have connected the host from that directory which has dump_file.sql e.g. Downloads
```

```
pg_dump -h hostname -U username -d dbname -f dumpfile.sql
pg_restore -h hostname -U username -d dbname dumpfile.sql




#### -x or --no-privileges: Excludes access privileges (including ownership information) from the dump #####

pg_dump -h hostname -U username -d dbname -x -f dumpfile.sql

pg_restore -h hostname -U username -d dbname --no-owner dumpfile.sql
```
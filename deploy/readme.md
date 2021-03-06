IDEAS:
https://github.com/fiee/generic_django_project
https://gist.github.com/fiee/158177


Set server:
https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04

Deploy Django:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

# Following tutorial

## Create EC2 ubuntu instance

```
ssh -i "~/.ssh/aws-eb2" ubuntu@ec2-54-171-253-25.eu-west-1.compute.amazonaws.com

```

## Deploy with fabfile
```
source activate fabric # (python2 env with fabric)
# First time
fab initial_deploy:host=ubuntu@ec2-54-171-253-25.eu-west-1.compute.amazonaws.com
# Then
fab deploy:host=ubuntu@ec2-54-171-253-25.eu-west-1.compute.amazonaws.com

```

## Firewall
```
sudo ufw allow 8000
```


## Launch webserver
```
source sncf_env/bin/activate
source us_election/us_election/bin/activate

/home/ubuntu/sites/us_election/virtualenv/bin/python3 /home/ubuntu/sites/us_election/source/manage.py runserver 0.0.0.0:8000
gunicorn --bind 0.0.0.0:8000 sncfweb.wsgi:application
```

## Create a Gunicorn systemd Service File
```
sudo nano /etc/systemd/system/gunicorn_sncf.service
```

```
sudo systemctl start gunicorn_sncf
sudo systemctl enable gunicorn_sncf
sudo systemctl status gunicorn_sncf.service


sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn.service
```

## Configure Nginx to Proxy Pass to Gunicorn

```
sudo nano /etc/nginx/sites-available/us_election
```

```
#sudo ln -s /home/webapp/app/nginx.conf /etc/nginx/sites-enable/webapp.org
sudo ln -s /etc/nginx/sites-available/sncf_web_project /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```


## If error:
to see logs:
```
sudo tail -f /var/log/nginx/error.log
sudo systemctl status gunicorn_us_election.service
less /var/log/syslog


```
http://stackoverflow.com/questions/28689445/nginx-django-and-gunicorn-gunicorn-sock-file-is-missing
```
ps auxf | grep gunicorn
grep init: /var/log/syslog

```

To restart
```
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx
```

```
sudo chown -R ubuntu:www-data run
sudo chown -R ubuntu:www-data /home/ubuntu/run/
```

```
    rewrite ^/api/(.*) /$1  break;
```

## Postgres:
```
sudo -u postgres psql

CREATE DATABASE api_transilien;
CREATE USER api_transilien_user WITH PASSWORD 'password';

ALTER ROLE api_transilien_user SET client_encoding TO 'utf8';
ALTER ROLE api_transilien_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE api_transilien_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE api_transilien TO api_transilien_user;
```

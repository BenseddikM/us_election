
# MONGODB
Do not forget to create index so that it is not to slow.
```
collection.create_index("vote_result")
```

# Cassandra:
```
ssh -i ubuntu@"canssandraKey.pem" 54.153.45.133
sudo ufw allow 9042

```
# Gunicorn
```
sudo nano /etc/systemd/system/gunicorn.service
```
In file:
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/us_election
ExecStart=/home/ubuntu/us_election/us_election/bin/gunicorn --workers 3 --bind 127.0.0.1:8888 us_election.wsgi:application

[Install]
WantedBy=multi-user.target

#ExecStart=/home/ubuntu/us_election/us_election/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/run/sncfweb.sock sncfweb.wsgi:application

# ExecStart=/home/ubuntu/sncf_web_project/sncf_env/bin/gunicorn --workers 3 --bind 127.0.0.1:8888 sncfweb.wsgi:application

```

Enable
```
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn.service

```

# Nginx
```
sudo nano /etc/nginx/sites-available/us_election
```

```
server {
    listen 80;
    server_name 54.194.138.195;

    access_log /home/ubuntu/access.log;
    error_log /home/ubuntu/error.log;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/ubuntu/us_election/us_election;
    }

    location / {
        proxy_pass http://127.0.0.1:8888;
    }

}
or at the end:

location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/run/sncfweb.sock;
    }

```

Enable:
```
sudo ln -s /etc/nginx/sites-available/us_election /etc/nginx/sites-enabled
# check if conf is ok
sudo nginx -t
sudo systemctl restart nginx

sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

To restart
```
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx
```

# Secrets
Send secrets (from folder where it is located):
```
scp -i "~/.ssh/aws-eb2" secret.json ubuntu@ec2-54-194-138-195.eu-west-1.compute.amazonaws.com:

ssh -i "~/.ssh/aws-eb2" ubuntu@ec2-54-194-138-195.eu-west-1.compute.amazonaws.com

mv secret.json sncf_web_project/sncfweb/settings/secret.json
mv secret.json us_election/us_election/secret.json

```

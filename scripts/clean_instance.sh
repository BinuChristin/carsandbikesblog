#!/usr/bin/env bash
sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/carsandbikesblog/nginx/nginx.conf /etc/nginx/sites-available/carsandbikesblog
sudo ln -s /etc/nginx/sites-available/carsandbikesblog /etc/nginx/sites-enabled/

# sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
# sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart ngin
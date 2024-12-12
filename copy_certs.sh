#!/bin/sh

# Create directory for certificates with the right permissions
mkdir -p /etc/nginx/certs/gwdoodles.com
cp /etc/letsencrypt/live/gwdoodles.com/fullchain.pem /etc/nginx/certs/gwdoodles.com/
cp /etc/letsencrypt/live/gwdoodles.com/privkey.pem /etc/nginx/certs/gwdoodles.com/
# mkdir -p /etc/nginx/certs/kitsu.gwdoodles.com
# cp /etc/letsencrypt/live/kitsu.gwdoodles.com/fullchain.pem /etc/nginx/certs/gwdoodles.com/
# cp /etc/letsencrypt/live/kitsu.gwdoodles.com/privkey.pem /etc/nginx/certs/gwdoodles.com/
ls -la /etc/nginx/certs/gwdoodles.com
# ls -la /etc/nginx/certs/kitsu.gwdoodles.com
chown -R nginx:nginx /etc/nginx/certs
chmod -R 600 /etc/nginx/certs

# Start Nginx
nginx -g 'daemon off;'

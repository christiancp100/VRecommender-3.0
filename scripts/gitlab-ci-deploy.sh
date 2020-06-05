#!/bin/bash
set -e

# Run ssh-agent (inside the build environment)
eval $(ssh-agent -s)

# To proceed with host key authentication
# Create the SSH directory and give it the right permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add the SSH key stored in SSH_PRIVATE_USI_KEY_DEPLOY variable to the agent store
echo "$SSH_PRIVATE_USI_KEY_DEPLOY" | tr -d '\r' | ssh-add - > /dev/null
# echo "$SSH_PRIVATE_USI_KEY_DEPLOY" > ~/.ssh/id_rsa
# chmod 600 ~/.ssh/id_rsa
# ssh-add ~/.ssh/id_rsa


# Add SSH_KNOWN_HOSTS
echo "$SSH_KNOWN_HOSTS" > ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts

ssh $DEPLOY_USER@$DEPLOY_HOST "cd ~/visual-recommender \
&& export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/adm:/home/13026022@unisi.ch/.local/bin:/home/13026022@unisi.ch/bin \
&& git stash \
&& git checkout master \
&& git pull origin master \
&& /home/13026022@unisi.ch/.local/bin/docker-compose stop \
&& docker-compose down \
&& docker-compose build \
&& docker-compose up -d elasticsearch \
&& docker-compose run -p 8000:8000 django-backend bash -c 'python3 manage.py check --deploy --settings=djangobackend.production_settings' & \
&& docker-compose run -p 8080:8080 vuejs-frontend bash -c 'npm run build && npx serve -l 8080 dist' & \
&& docker-compose-wait"
echo "Deployment completed!"
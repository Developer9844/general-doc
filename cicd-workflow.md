https://spacelift.io/blog/terraform-kubernetes-deployment

```
name: Deploy nodejs to EC2
on:
  push:
    branches:
     - main

jobs:
  build:
  name: Build
    runs-on: ubuntu-latest
    steps:
    - name: executing remote ssh commands using password
        uses: appleboy/ssh-action@v1.0.1
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          port: ${{ secrets.PORT }}

          script: |
            cd /var/www/project || exit
            git pull https://${{ secrets.GIH_USERNAME }}:${{ secrets.GIH_TOKEN }}@github.com/project/project.git main || exit 1
            npm run build || exit 1
            npm run build:tsc || exit 1
            pm2 restart ecosystem.config.js || exit 1
```

Private
```
name: Beta-Deployment

on:
  push:
    branches:
      - beta
      
jobs:
  deploy:
    name: Deploy via Bastion
    runs-on: ubuntu-latest
    env:
      AWS_INSTANCE_SG_ID: ${{ secrets.BASTION_SG_ID }}

    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4.1.0
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Get GitHub runner public IP
        id: ip
        run: |
          echo "ipv4=$(curl -s https://api.ipify.org)" >> $GITHUB_ENV

      - name: Print Public IP
        run: |
          echo "Runner IP is ${{ env.ipv4 }}"

      - name: Whitelist runner IP to Bastion SG
        run: |
          aws ec2 authorize-security-group-ingress \
            --group-id $AWS_INSTANCE_SG_ID \
            --protocol tcp \
            --port 22 \
            --cidr ${{ env.ipv4 }}/32

      - name: SSH to Bastion and deploy to private EC2
        uses: appleboy/ssh-action@v1.2.2
        with:
          host: ${{ secrets.BASTION_HOST }}
          username: ubuntu
          key: ${{ secrets.BASTION_KEY }}
          script: |
            ssh -o StrictHostKeyChecking=no beta << 'EOF'
              echo "Connected to private EC2"
              export NVM_DIR="$HOME/.nvm"
              [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  
              [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" 
              cd /var/www/backend || exit 1
              git pull https://${{ secrets.GIT_USER }}:${{ secrets.GIT_TOKEN }}@github.com/matteo-mil/proleven-backend beta || exit 1
              npm install || exit 1
              export NODE_OPTIONS=--max_old_space_size=8192
              npm run build || exit 1
              pm2 restart ecosystem.config.js --update-env
            EOF

      - name: Revoke runner IP from Bastion SG
        if: always()
        run: |
          aws ec2 revoke-security-group-ingress \
            --group-id $AWS_INSTANCE_SG_ID \
            --protocol tcp \
            --port 22 \
            --cidr ${{ env.ipv4 }}/32
```

Public
```
name: Dev-Deployment

on:
  push:
    branches:
      - development
      
jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    env:
      AWS_INSTANCE_SG_ID: ${{ secrets.DEV_SG_ID }}

    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4.1.0
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Get GitHub runner public IP
        id: ip
        run: |
          echo "ipv4=$(curl -s https://api.ipify.org)" >> $GITHUB_ENV

      - name: Print Public IP
        run: |
          echo "Runner IP is ${{ env.ipv4 }}"

      - name: Whitelist runner IP to Bastion SG
        run: |
          aws ec2 authorize-security-group-ingress \
            --group-id $AWS_INSTANCE_SG_ID \
            --protocol tcp \
            --port 22 \
            --cidr ${{ env.ipv4 }}/32

      - name: SSH to Bastion and deploy to private EC2
        uses: appleboy/ssh-action@v1.2.2
        with:
          host: ${{ secrets.DEV_EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.DEV_EC2_PRIVATE_KEY }}
          script: |
            export NVM_DIR="$HOME/.nvm"
            [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  
            [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
            export NODE_OPTIONS=--max_old_space_size=4096
            cd /var/www/dev/proleven-backend || exit
            git pull https://${{ secrets.GIT_USER }}:${{ secrets.GIT_TOKEN }}@github.com/matteo-mil/proleven-backend.git development || exit 1
            npm i || exit 1
            npm run build || exit 1
            pm2 restart ecosystem.config.js --update-env || exit 1

      - name: Revoke runner IP from Bastion SG
        if: always()
        run: |
          aws ec2 revoke-security-group-ingress \
            --group-id $AWS_INSTANCE_SG_ID \
            --protocol tcp \
            --port 22 \
            --cidr ${{ env.ipv4 }}/32
```


```
name: Deploy Next.js to EC2
  
 on:
   push:
     branches:
       - development
       - sonar-test
  
 jobs:
   build:
     name: Build
     runs-on: ubuntu-latest
     steps:
       - name: executing remote ssh commands using password
         uses: appleboy/ssh-action@v1.0.1
         with:
           host: ${{ secrets.HOST }}
           username: ${{ secrets.USERNAME }}
           key: ${{ secrets.KEY }}
           port: ${{ secrets.PORT }}
           passphrase: ${{ secrets.PASSPHRASE }}
           command_timeout: 200m
           script: |
             export NVM_DIR="$HOME/.nvm"
             source "$NVM_DIR/nvm.sh"
             nvm install 22.15.0 && nvm use 22.15.0
             echo "NodeJS Version 22.15.0"
             sudo rm -rf /var/www/temp_DyshezWeb || exit 1
             cd /var/www/DyshezWeb || exit 1
             git pull https://${{ secrets.GH_USERNAME }}:${{ secrets.GH_TOKEN }}@github.com/Dyshez/DyshezWeb.git development || exit 1
             cd ../ || exit 1
             sudo mkdir temp_DyshezWeb || exit 1
             sudo cp -rf DyshezWeb/. temp_DyshezWeb || exit 1
             sudo chown -R ubuntu:ubuntu temp_DyshezWeb || exit 1
             cd temp_DyshezWeb || exit 1
             npm i -f|| exit 1
             doppler run -- npm run build || exit 1
             rsync -arzh --delete /var/www/temp_DyshezWeb/node_modules /var/www/temp_DyshezWeb/.next /var/www/DyshezWeb  || exit 1
             sudo rm -rf /var/www/temp_DyshezWeb || exit 1
             cd /var/www/DyshezWeb || exit 1
             pm2 delete ecosystem.config.js || exit 1
             doppler run -- pm2 restart ecosystem.config.js --update-env || exit 1
```

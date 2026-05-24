# Deployment Guide

This guide covers deploying the N8tive AI Agent Framework to AWS EC2 with Nginx, SSL, and production-ready configuration.

## Prerequisites

- AWS EC2 instance (Ubuntu 22.04 LTS recommended)
- Domain name (optional, for SSL)
- SSH access to EC2 instance
- OpenAI API key

## Step 1: Initial Server Setup

### 1.1 Connect to EC2 Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 1.2 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.3 Install Dependencies

```bash
# Python and pip
sudo apt install -y python3.10 python3-pip python3-venv

# Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Nginx
sudo apt install -y nginx

# Certbot for SSL
sudo apt install -y certbot python3-certbot-nginx
```

## Step 2: Backend Deployment

### 2.1 Clone Repository

```bash
cd /home/ubuntu
git clone <your-repo-url> "N8tive AI"
cd "N8tive AI"/backend
```

### 2.2 Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.3 Configure Environment Variables

```bash
nano .env
```

Add:
```env
OPENAI_API_KEY=your_openai_api_key_here
ALLOWED_ORIGINS=https://yourdomain.com,http://localhost:5173
USE_DATABASE=true
```

### 2.4 Create Data Directory

```bash
mkdir -p data
```

### 2.5 Test Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Test with: `curl http://localhost:8000/health`

## Step 3: Frontend Deployment

### 3.1 Build Frontend

```bash
cd /home/ubuntu/"N8tive AI"/frontend
npm install
npm run build
```

### 3.2 Configure Environment

Create `.env.production`:
```env
VITE_API_URL=https://api.yourdomain.com
```

Rebuild:
```bash
npm run build
```

## Step 4: Nginx Configuration

### 4.1 Create Nginx Config

```bash
sudo nano /etc/nginx/sites-available/n8tive-ai
```

Add:
```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com;

    root /home/ubuntu/"N8tive AI"/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.2 Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/n8tive-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 5: SSL Setup

### 5.1 Get SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

Follow the prompts to complete SSL setup.

### 5.2 Auto-renewal

Certbot sets up auto-renewal automatically. Test with:
```bash
sudo certbot renew --dry-run
```

## Step 6: Systemd Service for Backend

### 6.1 Create Service File

```bash
sudo nano /etc/systemd/system/n8tive-ai-backend.service
```

Add:
```ini
[Unit]
Description=N8tive AI Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/"N8tive AI"/backend
Environment="PATH=/home/ubuntu/"N8tive AI"/backend/venv/bin"
ExecStart=/home/ubuntu/"N8tive AI"/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 6.2 Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable n8tive-ai-backend
sudo systemctl start n8tive-ai-backend
sudo systemctl status n8tive-ai-backend
```

## Step 7: Firewall Configuration

### 7.1 Configure UFW

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Step 8: Security Hardening

### 8.1 Rate Limiting (Optional)

Add to Nginx config:
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api {
    limit_req zone=api_limit burst=20;
    # ... existing proxy settings
}
```

### 8.2 Security Headers

Add to Nginx config:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

## Step 9: Monitoring and Logs

### 9.1 Backend Logs

```bash
# View logs
sudo journalctl -u n8tive-ai-backend -f

# View recent logs
sudo journalctl -u n8tive-ai-backend -n 100
```

### 9.2 Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

## Step 10: Updates and Maintenance

### 10.1 Update Backend

```bash
cd /home/ubuntu/"N8tive AI"/backend
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart n8tive-ai-backend
```

### 10.2 Update Frontend

```bash
cd /home/ubuntu/"N8tive AI"/frontend
git pull
npm install
npm run build
sudo systemctl reload nginx
```

## Troubleshooting

### Backend Not Starting

1. Check logs: `sudo journalctl -u n8tive-ai-backend`
2. Verify `.env` file exists and has correct values
3. Check port 8000 is not in use: `sudo netstat -tulpn | grep 8000`

### Nginx Errors

1. Test config: `sudo nginx -t`
2. Check error logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify permissions on files

### SSL Issues

1. Check certificate: `sudo certbot certificates`
2. Test renewal: `sudo certbot renew --dry-run`
3. Verify DNS records point to your server

## Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed and auto-renewing
- [ ] Systemd service running and enabled
- [ ] Nginx configured and tested
- [ ] Firewall configured
- [ ] Backups configured (database, files)
- [ ] Monitoring set up (optional)
- [ ] Rate limiting configured (optional)
- [ ] Security headers added
- [ ] Domain DNS configured correctly

## Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Certbot Documentation](https://certbot.eff.org/docs/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)








# AI Digital Workforce - Deployment Guide

## 📋 Prerequisites

Before deploying the AI Digital Workforce application, ensure you have:

1. **Docker** (version 20.10 or higher)
   - Installation: https://docs.docker.com/get-docker/

2. **Docker Compose** (version 2.0 or higher)
   - Installation: https://docs.docker.com/compose/install/

3. **API Keys**
   - OpenAI API Key: https://platform.openai.com/api-keys
   - Tavily API Key: https://tavily.com/

4. **System Requirements**
   - Minimum 4GB RAM
   - 10GB free disk space
   - Ports 80, 3306, 8000, 8080 available

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/ai-digital-workforce.git
cd ai-digital-workforce
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Required configurations in `.env`:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `TAVILY_API_KEY`: Your Tavily search API key
- `MYSQL_PASSWORD`: Set a secure MySQL password
- `SECRET_KEY`: Generate with `openssl rand -hex 32`

### 3. Deploy Using Script (Recommended)
```bash
# Make the script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### 4. Manual Deployment (Alternative)
```bash
# Build and start all services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

## 📦 Services

The application consists of the following services:

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 80 | React-based web interface |
| Backend | 8000 | FastAPI REST API & WebSocket server |
| MySQL | 3306 | Database server |
| Adminer | 8080 | Database management interface |

## 🔧 Configuration

### Environment Variables

Key environment variables you can customize:

```bash
# Database
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=ai_workforce
MYSQL_USER=ai_user
MYSQL_PASSWORD=your_password

# Application
DEBUG=false  # Set to true for development
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Ports
FRONTEND_PORT=80
BACKEND_PORT=8000
MYSQL_PORT=3306
ADMINER_PORT=8080
```

### Updating Configuration

After changing `.env` file:
```bash
docker-compose down
docker-compose up -d
```

## 🌐 Deployment on EC2

### 1. Launch EC2 Instance
- Use Ubuntu 22.04 LTS AMI
- Instance type: t3.medium or larger
- Security group ports: 22, 80, 443, 8000, 8080

### 2. Connect and Setup
```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login for group changes
exit
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 3. Deploy Application
```bash
# Clone repository
git clone https://github.com/your-repo/ai-digital-workforce.git
cd ai-digital-workforce

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Deploy
./deploy.sh
```

### 4. Configure Domain (Optional)
```bash
# Install nginx for reverse proxy
sudo apt install nginx -y

# Configure nginx
sudo nano /etc/nginx/sites-available/ai-workforce

# Add configuration:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/ai-workforce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Security Considerations

### Production Deployment

1. **Use HTTPS**: Install SSL certificate using Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

2. **Secure Database**: Change default passwords in `.env`

3. **Firewall**: Configure UFW
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

4. **Environment Variables**: Never commit `.env` to version control

## 🛠️ Maintenance

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Backup Database
```bash
# Create backup
docker exec ai_workforce_mysql mysqldump -u root -p ai_workforce > backup.sql

# Restore backup
docker exec -i ai_workforce_mysql mysql -u root -p ai_workforce < backup.sql
```

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Clear Data
```bash
# Stop and remove containers, volumes
docker-compose down -v

# Remove all data (CAUTION!)
docker volume rm ai_workforce_mysql_data
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Check what's using the port
sudo lsof -i :80
# Kill the process or change port in .env
```

2. **MySQL Connection Failed**
```bash
# Check MySQL is running
docker-compose ps mysql

# Check logs
docker-compose logs mysql

# Restart MySQL
docker-compose restart mysql
```

3. **Frontend Can't Connect to Backend**
- Check CORS settings in docker-compose.yml
- Verify backend is healthy: `curl http://localhost:8000/health`

4. **Out of Memory**
```bash
# Check memory usage
docker stats

# Increase swap (EC2)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Debug Mode
```bash
# Enable debug in .env
DEBUG=true
LOG_LEVEL=DEBUG

# Restart services
docker-compose restart
```

## 📊 Monitoring

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost/health

# Database health
docker exec ai_workforce_mysql mysqladmin -u root -p ping
```

### Resource Usage
```bash
# Real-time stats
docker stats

# Service status
docker-compose ps
```

## 📧 Support

For issues or questions:
- Check logs: `docker-compose logs`
- GitHub Issues: [your-repo/issues]
- Documentation: [/docs]

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
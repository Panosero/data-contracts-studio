# Data Contracts Studio - Podman Production Deployment Guide

This guide covers deploying Data Contracts Studio using Podman in a production environment with enterprise-grade security and reliability.

## 🚀 Quick Start

### Prerequisites

1. **Install Podman** (version 4.0+ recommended):
   ```bash
   # RHEL/CentOS/Fedora
   sudo dnf install podman podman-compose
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install podman podman-compose
   
   # macOS (for development)
   brew install podman
   ```

2. **Setup Rootless Podman**:
   ```bash
   # Configure user namespaces
   sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
   sudo systemctl enable --now user@$(id -u).service
   ```

### Deployment Steps

1. **Security Setup**:
   ```bash
   ./scripts/setup-podman-security.sh
   ```

2. **Configure Environment**:
   ```bash
   cp .env.podman.template .env
   # Edit .env with your configuration
   ```

3. **Deploy**:
   ```bash
   ./scripts/deploy-podman.sh deploy
   ```

4. **Enable Auto-start**:
   ```bash
   systemctl --user enable data-contracts-studio-pod.service
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_IP` | Server IP or domain | `localhost` |
| `BACKEND_PORT` | Backend API port | `8888` |
| `FRONTEND_PORT` | Frontend port | `80` |
| `POSTGRES_PASSWORD` | Database password | Generated |
| `SECRET_KEY` | Application secret | Generated |
| `DATA_DIR` | Data directory path | `./data` |

### API Keys

Set your API keys in the `.env` file:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here
AZURE_OPENAI_KEY=your_azure_openai_key_here
```

## 🔒 Security Features

### Rootless Containers
- All containers run without root privileges
- Reduced attack surface
- Better isolation

### Security Policies
- Capability dropping
- No-new-privileges flag
- Seccomp profiles
- Resource limits

### Network Security
- Isolated container network
- Custom bridge configuration
- DNS security

### Data Protection
- Encrypted volumes
- Secure file permissions
- Automated backups

## 🏗️ Architecture

### Container Structure
```
data-contracts-studio-pod
├── frontend (nginx:alpine)
├── backend (python:3.11-slim)
└── database (postgres:15-alpine)
```

### Volume Mounts
- `postgres_data`: Database persistent storage
- `backend_data`: Application data and logs
- `config`: Configuration files

### Network
- Custom bridge network: `data-contracts-net`
- Subnet: `172.20.0.0/16`
- Internal communication only

## 📊 Monitoring

### Health Checks
- Backend: `http://localhost:8888/health`
- Frontend: `http://localhost:80/health`
- Database: `pg_isready` command

### Logging
- Centralized logging via journald
- Log rotation (10MB max, 5 files)
- Structured JSON logs

### Metrics
- Container resource usage
- Application performance metrics
- Database connection stats

## 🔄 Maintenance

### Backup
Automated daily backups:
```bash
# Manual backup
~/bin/backup-data-contracts.sh

# Restore from backup
./scripts/restore-backup.sh backup_file.tar.gz
```

### Updates
```bash
# Update images
podman-compose -f podman-compose.yml pull

# Restart services
./scripts/deploy-podman.sh restart
```

### Logs
```bash
# View all logs
./scripts/deploy-podman.sh logs

# View specific service logs
podman logs data-contracts-backend
```

## 🛠️ Commands Reference

### Deployment Commands
```bash
# Full deployment
./scripts/deploy-podman.sh deploy

# Build images only
./scripts/deploy-podman.sh build

# Start services
./scripts/deploy-podman.sh start

# Stop services
./scripts/deploy-podman.sh stop

# Restart services
./scripts/deploy-podman.sh restart

# View logs
./scripts/deploy-podman.sh logs

# Service status
./scripts/deploy-podman.sh status

# Generate systemd services
./scripts/deploy-podman.sh systemd

# Clean up
./scripts/deploy-podman.sh clean
```

### Podman Commands
```bash
# List containers
podman ps

# Container stats
podman stats

# Execute command in container
podman exec -it data-contracts-backend bash

# View container logs
podman logs -f data-contracts-backend

# Inspect container
podman inspect data-contracts-backend
```

## 🔍 Troubleshooting

### Common Issues

1. **Permission Denied**:
   ```bash
   # Check user namespaces
   podman unshare cat /proc/self/uid_map
   
   # Reset permissions
   podman system reset
   ```

2. **Port Already in Use**:
   ```bash
   # Find process using port
   sudo netstat -tulpn | grep :8888
   
   # Change port in .env file
   BACKEND_PORT=8889
   ```

3. **Database Connection**:
   ```bash
   # Check database logs
   podman logs data-contracts-db
   
   # Test connection
   podman exec -it data-contracts-db psql -U postgres -d datacontracts
   ```

4. **Container Won't Start**:
   ```bash
   # Check container status
   podman ps -a
   
   # View detailed logs
   podman logs --details data-contracts-backend
   
   # Check resource usage
   podman system df
   ```

### Log Locations
- Application logs: `journalctl --user -u data-contracts-studio-pod.service`
- Container logs: `podman logs <container_name>`
- System logs: `/var/log/messages` (requires sudo)

## 🌐 Production Considerations

### Reverse Proxy
Use nginx or traefik as reverse proxy:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL/TLS
Configure SSL certificates:
```bash
# Let's Encrypt with certbot
sudo certbot --nginx -d your-domain.com
```

### Firewall
Configure firewall rules:
```bash
# Allow HTTP/HTTPS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Allow specific ports
sudo firewall-cmd --permanent --add-port=8888/tcp
sudo firewall-cmd --reload
```

### Resource Limits
Set resource limits in compose file:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

## 📈 Performance Tuning

### Database Optimization
```sql
-- PostgreSQL performance settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
SELECT pg_reload_conf();
```

### Container Optimization
- Use multi-stage builds
- Minimize image size
- Optimize startup time
- Configure health checks

### Monitoring Setup
```bash
# Enable monitoring
systemctl --user enable data-contracts-monitoring.timer
systemctl --user start data-contracts-monitoring.timer
```

## 🆘 Support

### Logs Collection
```bash
# Collect all logs for support
./scripts/collect-logs.sh
```

### System Information
```bash
# System info
podman system info
podman version
```

For additional support, check the project documentation or open an issue on GitHub.

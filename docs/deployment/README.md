# Deployment Guide

This guide covers various deployment scenarios for the Data Contracts Studio application.

## 🚀 Quick Start - IP-Based Deployment

**Perfect for work/company servers where you don't need a custom domain:**

### Docker Deployment (Recommended) ⭐

```bash
# Clone the repository
git clone https://github.com/your-username/data-contracts-studio.git
cd data-contracts-studio

# Deploy with automatic IP detection
make deploy
# OR
./scripts/deploy.sh
```

**What this does:**
- ✅ Automatically detects your server's IP address
- ✅ Configures CORS for IP-based access
- ✅ Sets up PostgreSQL database with secure credentials
- ✅ Builds and starts Docker containers
- ✅ Provides access instructions

**Requirements:**
- Docker and Docker Compose installed
- Ports 80 and 8888 open in firewall
- Internet connection for IP detection

**Access your app:**
- Website: `http://YOUR_SERVER_IP`
- API: `http://YOUR_SERVER_IP:8888/api/v1`
- Docs: `http://YOUR_SERVER_IP:8888/docs`

---

## 🚀 Deployment Options

### 1. GitHub Pages (Frontend Only) ⭐ **Recommended for Demo**

Perfect for showcasing the frontend with a separate backend API.

**Setup:**
```bash
# Run the GitHub Pages deployment script
make deploy-pages

# Or manually:
./scripts/deploy-github-pages.sh
```

**Requirements:**
- GitHub repository
- Backend API hosted elsewhere (Heroku, Railway, etc.)

**Pros:**
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ CDN distribution
- ✅ Custom domain support

**Cons:**
- ❌ Frontend only (need separate backend)
- ❌ No server-side rendering

---

### 2. Company Server (Full Stack) 🏢

Deploy both frontend and backend to your company's server.

#### With Docker (Recommended):
```bash
# Clone repository on server
git clone https://github.com/your-username/data-contracts-studio.git
cd data-contracts-studio

# Deploy with Docker
make docker-up
```

#### Without Docker:
```bash
# Run the server deployment script
make deploy-server

# Or manually:
sudo ./scripts/deploy-server.sh
```

**Requirements:**
- Ubuntu/Debian server
- Root/sudo access
- Domain name (optional)

**What it installs:**
- Python 3.11 + Node.js 18
- Nginx (reverse proxy)
- Supervisor (process management)
- SSL certificates (optional)

---

### 3. Cloud Platforms

#### Heroku (Full Stack):
```bash
# Install Heroku CLI
# Create Heroku apps
heroku create your-app-backend
heroku create your-app-frontend

# Deploy backend
git subtree push --prefix backend heroku-backend main

# Deploy frontend
git subtree push --prefix frontend heroku-frontend main
```

#### Railway/Render:
- Use the provided Dockerfiles
- Connect your GitHub repository
- Set environment variables

#### Vercel (Frontend) + Railway (Backend):
```bash
# Deploy frontend to Vercel
npx vercel --prod

# Deploy backend to Railway
# Connect GitHub repository to Railway
```

---

## 🔧 CI/CD Setup

### GitHub Actions

Already configured in `.github/workflows/ci-cd.yml`

**Required Secrets:**
```bash
# For server deployment
SERVER_HOST=your-server-ip
SERVER_USER=your-username
SERVER_SSH_KEY=your-private-key

# For frontend
REACT_APP_API_URL=https://your-api-domain.com/api/v1
```

**Setup:**
1. Go to repository Settings → Secrets and variables → Actions
2. Add required secrets
3. Push to main branch to trigger deployment

### GitLab CI

Already configured in `.gitlab-ci.yml`

**Required Variables:**
- `SSH_PRIVATE_KEY`
- `SERVER_HOST`
- `SERVER_USER`

**Setup:**
1. Go to Project → Settings → CI/CD → Variables
2. Add required variables
3. Push to main branch to trigger pipeline

---

## 🌐 Domain and SSL Setup

### Custom Domain with GitHub Pages:
1. Add CNAME file to `frontend/public/`
2. Configure DNS A records:
   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```

### Server SSL Setup:
```bash
# Automatic with Let's Encrypt (included in deploy script)
sudo certbot --nginx -d your-domain.com

# Manual certificate
# Edit nginx configuration to include SSL
```

---

## 📊 Monitoring and Maintenance

### Health Checks:
```bash
# Check application health
make health

# Check server status
systemctl status nginx
supervisorctl status
```

### Log Management:
```bash
# Backend logs
tail -f /var/log/data-contracts-backend.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Updates:
```bash
# Update application on server
sudo -u appuser /opt/data-contracts-studio/update.sh

# Update with CI/CD
git push origin main  # Triggers automatic deployment
```

---

## 🔒 Security Considerations

### Environment Variables:
- ✅ Use `.env` files for configuration
- ✅ Never commit secrets to repository
- ✅ Use CI/CD secrets for deployment

### Server Security:
- ✅ Regular system updates
- ✅ Firewall configuration
- ✅ SSL certificates
- ✅ Security headers in Nginx

### Application Security:
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Rate limiting (optional)
- ✅ Authentication (if needed)

---

## 🔧 Server Configuration

### Firewall Setup (Ubuntu/Debian)

**For Docker deployment:**
```bash
# Allow HTTP traffic
sudo ufw allow 80/tcp
sudo ufw allow 8888/tcp

# Allow SSH (if not already enabled)
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

**For server deployment (without Docker):**
```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow SSH
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable
```

### IP Address Detection

The deployment scripts automatically detect your server's public IP using:
1. `ifconfig.me`
2. `icanhazip.com` 
3. `ipecho.net/plain`
4. Local hostname resolution

If auto-detection fails, you'll be prompted to enter the IP manually.

### Environment Variables

**Key variables for IP-based deployment:**
```bash
SERVER_IP=your.server.ip.address
ALLOWED_ORIGINS=["http://your.server.ip.address"]
REACT_APP_API_URL=http://your.server.ip.address:8888/api/v1
```

---

## 🆘 Troubleshooting

### Common Issues:

**Cannot access application:**
- ✅ Check firewall rules: `sudo ufw status`
- ✅ Verify server IP is correct
- ✅ Ensure ports 80 and 8888 are open
- ✅ Check if services are running: `docker-compose ps`

**CORS errors in browser:**
- ✅ Verify `ALLOWED_ORIGINS` includes your server IP
- ✅ Check browser developer console
- ✅ Ensure API URL is correct in frontend

**Frontend not loading:**
- ✅ Check API URL in environment variables
- ✅ Verify CORS settings in backend
- ✅ Check browser console for errors
- ✅ Test API directly: `curl http://YOUR_IP:8888/health`

**Backend not responding:**
- ✅ Check Docker logs: `docker-compose logs backend`
- ✅ Verify database connection
- ✅ Test health endpoint: `curl http://localhost:8888/health`

**Database connection issues:**
- ✅ Check database container: `docker-compose logs db`
- ✅ Verify credentials in .env file
- ✅ Ensure database container is running

**IP detection problems:**
- ✅ Manually set `SERVER_IP` environment variable
- ✅ Check network connectivity
- ✅ Use local IP if behind NAT: `hostname -I`

### Quick Debug Commands

```bash
# Check Docker containers
docker-compose ps

# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Test API connectivity
curl http://YOUR_SERVER_IP:8888/health
curl http://YOUR_SERVER_IP:8888/api/v1/contracts

# Check environment variables
cat .env

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up -d --build
```

---

## 📞 Support

For deployment issues:
1. Check the troubleshooting section above
2. Review Docker/application logs
3. Verify firewall and network configuration
4. Test API endpoints manually
5. Open an issue on GitHub with logs and error details

**Logs to include in support requests:**
- `docker-compose logs`
- `.env` file (remove sensitive data)
- Firewall status: `sudo ufw status`
- Network info: `ip addr show`

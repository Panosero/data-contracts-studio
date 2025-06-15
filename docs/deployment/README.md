# Deployment Guide

This guide covers various deployment scenarios for the Data Contracts Studio application.

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

## 🆘 Troubleshooting

### Common Issues:

**Frontend not loading:**
- Check API URL in environment variables
- Verify CORS settings in backend
- Check browser console for errors

**Backend not responding:**
- Check supervisor status: `supervisorctl status`
- Check logs: `tail -f /var/log/data-contracts-backend.log`
- Verify database connection

**Nginx errors:**
- Test configuration: `nginx -t`
- Check error logs: `tail -f /var/log/nginx/error.log`
- Verify proxy settings

**CI/CD failures:**
- Check secrets/variables configuration
- Verify SSH key permissions
- Review pipeline logs

---

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Open an issue on GitHub
4. Contact the development team

Remember to customize domain names, API URLs, and server paths according to your specific setup!

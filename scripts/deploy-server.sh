#!/bin/bash

# Data Contracts Studio - Server Deployment Script (No Docker)
# This script deploys the application to a remote server without Docker

set -e

echo "🚀 Deploying Data Contracts Studio to server..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
APP_DIR="/opt/data-contracts-studio"
SERVICE_USER="appuser"
BACKEND_PORT="8000"
FRONTEND_PORT="3000"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

# Check if running as root for system operations
check_permissions() {
    if [[ $EUID -eq 0 ]]; then
        print_status "Running with root privileges ✓"
    else
        print_warning "Some operations may require sudo privileges"
    fi
}

# Install system dependencies
install_system_dependencies() {
    print_status "Installing system dependencies..."

    # Update package list
    sudo apt-get update

    # Install Python 3.11
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get update
    sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

    # Install Node.js 18
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs

    # Install other dependencies
    sudo apt-get install -y nginx supervisor git curl

    print_status "System dependencies installed ✓"
}

# Create application user
create_app_user() {
    if id "$SERVICE_USER" &>/dev/null; then
        print_status "User $SERVICE_USER already exists"
    else
        print_status "Creating application user..."
        sudo useradd --system --create-home --shell /bin/bash $SERVICE_USER
        print_status "User $SERVICE_USER created ✓"
    fi
}

# Setup application directory
setup_app_directory() {
    print_status "Setting up application directory..."

    # Create directory if it doesn't exist
    sudo mkdir -p $APP_DIR
    sudo chown $SERVICE_USER:$SERVICE_USER $APP_DIR

    # Clone or update repository
    if [ -d "$APP_DIR/.git" ]; then
        print_status "Updating existing repository..."
        sudo -u $SERVICE_USER git -C $APP_DIR pull origin main
    else
        print_status "Cloning repository..."
        sudo -u $SERVICE_USER git clone https://github.com/your-username/data-contracts-studio.git $APP_DIR
    fi

    print_status "Application directory setup complete ✓"
}

# Deploy backend
deploy_backend() {
    print_status "Deploying backend..."

    cd $APP_DIR/backend

    # Create virtual environment
    sudo -u $SERVICE_USER python3.11 -m venv venv

    # Install dependencies
    sudo -u $SERVICE_USER ./venv/bin/pip install --upgrade pip
    sudo -u $SERVICE_USER ./venv/bin/pip install -r requirements.txt

    # Install production WSGI server
    sudo -u $SERVICE_USER ./venv/bin/pip install gunicorn uvicorn[standard]

    # Create environment file
    sudo -u $SERVICE_USER tee .env >/dev/null <<EOF
DEBUG=False
DATABASE_URL=sqlite:///$APP_DIR/data/data_contracts.db
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=["http://localhost", "https://your-domain.com"]
EOF

    # Create data directory
    sudo -u $SERVICE_USER mkdir -p $APP_DIR/data

    # Initialize database
    sudo -u $SERVICE_USER ./venv/bin/python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

    print_status "Backend deployed ✓"
}

# Deploy frontend-]
deploy_frontend() {
    print_status "Deploying frontend..."

    cd $APP_DIR/frontend

    # Install dependencies
    sudo -u $SERVICE_USER npm ci --only=production

    # Create production environment file
    sudo -u $SERVICE_USER tee .env.production >/dev/null <<EOF
REACT_APP_API_URL=https://your-domain.com/api/v1
REACT_APP_APP_NAME=Data Contracts Studio
REACT_APP_VERSION=1.0.0
EOF

    # Build frontend
    sudo -u $SERVICE_USER npm run build

    print_status "Frontend deployed ✓"
}

# Configure Supervisor for backend
configure_supervisor() {
    print_status "Configuring Supervisor for backend..."

    sudo tee /etc/supervisor/conf.d/data-contracts-backend.conf >/dev/null <<EOF
[program:data-contracts-backend]
command=$APP_DIR/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:$BACKEND_PORT
directory=$APP_DIR/backend
user=$SERVICE_USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/data-contracts-backend.log
environment=PATH="$APP_DIR/backend/venv/bin"
EOF

    # Reload and start service
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl restart data-contracts-backend

    print_status "Supervisor configured ✓"
}

# Configure Nginx
configure_nginx() {
    print_status "Configuring Nginx..."

    sudo tee $NGINX_AVAILABLE/data-contracts-studio >/dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Frontend (React app)
    location / {
        root $APP_DIR/frontend/build;
        index index.html index.htm;
        try_files \$uri \$uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:$BACKEND_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Backend docs
    location /docs {
        proxy_pass http://127.0.0.1:$BACKEND_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Health check
    location /health {
        proxy_pass http://127.0.0.1:$BACKEND_PORT;
        access_log off;
    }
}
EOF

    # Enable site
    sudo ln -sf $NGINX_AVAILABLE/data-contracts-studio $NGINX_ENABLED/

    # Test and reload Nginx
    sudo nginx -t
    sudo systemctl reload nginx

    print_status "Nginx configured ✓"
}

# Setup SSL with Let's Encrypt (optional)
setup_ssl() {
    read -p "Do you want to setup SSL with Let's Encrypt? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setting up SSL with Let's Encrypt..."

        # Install Certbot
        sudo apt-get install -y certbot python3-certbot-nginx

        # Get certificate
        sudo certbot --nginx -d your-domain.com -d www.your-domain.com

        print_status "SSL setup complete ✓"
    fi
}

# Setup log rotation
setup_log_rotation() {
    print_status "Setting up log rotation..."

    sudo tee /etc/logrotate.d/data-contracts-studio >/dev/null <<EOF
/var/log/data-contracts-*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        supervisorctl restart data-contracts-backend
    endscript
}
EOF

    print_status "Log rotation configured ✓"
}

# Setup monitoring
setup_monitoring() {
    print_status "Setting up basic monitoring..."

    # Create simple health check script
    sudo tee /usr/local/bin/data-contracts-health.sh >/dev/null <<EOF
#!/bin/bash
BACKEND_URL="http://localhost:$BACKEND_PORT/health"
if curl -f -s \$BACKEND_URL > /dev/null; then
    echo "Backend OK"
else
    echo "Backend FAILED"
    supervisorctl restart data-contracts-backend
fi
EOF

    sudo chmod +x /usr/local/bin/data-contracts-health.sh

    # Add to crontab
    (
        sudo crontab -l 2>/dev/null
        echo "*/5 * * * * /usr/local/bin/data-contracts-health.sh"
    ) | sudo crontab -

    print_status "Basic monitoring setup ✓"
}

# Create update script
create_update_script() {
    print_status "Creating update script..."

    sudo tee $APP_DIR/update.sh >/dev/null <<EOF
#!/bin/bash
set -e

echo "🔄 Updating Data Contracts Studio..."

# Pull latest code
git pull origin main

# Update backend
cd backend
./venv/bin/pip install -r requirements.txt
cd ..

# Update frontend
cd frontend
npm ci --only=production
npm run build
cd ..

# Restart services
sudo supervisorctl restart data-contracts-backend
sudo systemctl reload nginx

echo "✅ Update complete!"
EOF

    sudo chmod +x $APP_DIR/update.sh
    sudo chown $SERVICE_USER:$SERVICE_USER $APP_DIR/update.sh

    print_status "Update script created ✓"
}

# Main deployment function
main() {
    print_status "Starting server deployment..."

    check_permissions
    install_system_dependencies
    create_app_user
    setup_app_directory
    deploy_backend
    deploy_frontend
    configure_supervisor
    configure_nginx
    setup_ssl
    setup_log_rotation
    setup_monitoring
    create_update_script

    print_status "Deployment complete! 🎉"
    echo ""
    echo "Your application is now running:"
    echo "  Website: http://your-domain.com"
    echo "  API: http://your-domain.com/api/v1"
    echo "  Docs: http://your-domain.com/docs"
    echo ""
    echo "To update the application:"
    echo "  sudo -u $SERVICE_USER $APP_DIR/update.sh"
    echo ""
    echo "To check status:"
    echo "  sudo supervisorctl status"
    echo "  sudo systemctl status nginx"
}

# Run deployment
main "$@"

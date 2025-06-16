#!/bin/bash

# Data Contracts Studio - Server Deployment Script (IP-based deployment)
# This script deploys the application to a remote server using IP address

set -e

echo "🚀 Deploying Data Contracts Studio to server..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_info() {
    echo -e "${BLUE}[CONFIG]${NC} $1"
}

# Configuration
APP_DIR="/opt/data-contracts-studio"
SERVICE_USER="appuser"
BACKEND_PORT="8000"
FRONTEND_PORT="3000"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

# Get server IP address
get_server_ip() {
    # Try multiple methods to get the server's public IP
    SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || curl -s ipecho.net/plain 2>/dev/null || hostname -I | awk '{print $1}')

    if [ -z "$SERVER_IP" ]; then
        print_warning "Could not automatically detect server IP. Please enter it manually:"
        read -p "Enter your server IP address: " SERVER_IP
    fi

    print_info "Server IP detected/configured: $SERVER_IP"

    # Confirm with user
    read -p "Is this correct? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter the correct server IP address: " SERVER_IP
    fi

    export SERVER_IP
}

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

    # Create environment file with IP-based configuration
    sudo -u $SERVICE_USER tee .env >/dev/null <<EOF
DEBUG=False
DATABASE_URL=sqlite:///$APP_DIR/data/data_contracts.db
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=["http://$SERVER_IP", "http://localhost", "http://127.0.0.1"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS=["*"]
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

    # Create production environment file with IP-based API URL
    sudo -u $SERVICE_USER tee .env.production >/dev/null <<EOF
REACT_APP_API_URL=http://$SERVER_IP:$BACKEND_PORT/api/v1
REACT_APP_APP_NAME=Data Contracts Studio
REACT_APP_VERSION=1.0.0
GENERATE_SOURCEMAP=false
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

# Configure Nginx for IP-based deployment
configure_nginx() {
    print_status "Configuring Nginx for IP-based deployment..."

    sudo tee $NGINX_AVAILABLE/data-contracts-studio >/dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    # Accept requests to server IP and localhost
    server_name $SERVER_IP localhost 127.0.0.1 _;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # CORS headers for API requests
    add_header Access-Control-Allow-Origin "http://$SERVER_IP" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept, Authorization" always;
    
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
    
    # Backend API - proxy to backend server
    location /api/ {
        proxy_pass http://127.0.0.1:$BACKEND_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # CORS preflight
        if (\$request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin "http://$SERVER_IP";
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept, Authorization";
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type 'text/plain charset=UTF-8';
            add_header Content-Length 0;
            return 204;
        }
    }
    
    # Backend docs
    location /docs {
        proxy_pass http://127.0.0.1:$BACKEND_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # OpenAPI JSON
    location /openapi.json {
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

    # Remove default nginx site
    sudo rm -f $NGINX_ENABLED/default

    # Enable our site
    sudo ln -sf $NGINX_AVAILABLE/data-contracts-studio $NGINX_ENABLED/

    # Test and reload Nginx
    sudo nginx -t
    sudo systemctl reload nginx

    print_status "Nginx configured for IP access ✓"
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

    # Get server IP first
    get_server_ip

    check_permissions
    install_system_dependencies
    create_app_user
    setup_app_directory
    deploy_backend
    deploy_frontend
    configure_supervisor
    configure_nginx
    setup_log_rotation
    setup_monitoring
    create_update_script

    print_status "Deployment complete! 🎉"
    echo ""
    echo "Your application is now running:"
    echo "  Website: http://$SERVER_IP"
    echo "  API: http://$SERVER_IP/api/v1"
    echo "  Docs: http://$SERVER_IP/docs"
    echo ""
    echo "To update the application:"
    echo "  sudo -u $SERVICE_USER $APP_DIR/update.sh"
    echo ""
    echo "To check status:"
    echo "  sudo supervisorctl status"
    echo "  sudo systemctl status nginx"
    echo ""
    print_info "Access your application at: http://$SERVER_IP"
    print_warning "Make sure port 80 is open in your server's firewall"
}

# Run deployment
main "$@"

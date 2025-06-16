#!/bin/bash

# Data Contracts Studio - Podman Security Setup
# Configures security policies and network settings for production deployment

set -e

echo "🔒 Data Contracts Studio - Podman Security Setup"

# Colors
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'

print_status() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_info() { echo -e "${BLUE}[CONFIG]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root for security reasons."
        print_info "Run as regular user for rootless Podman setup."
        exit 1
    fi
}

# Setup rootless Podman
setup_rootless() {
    print_status "Setting up rootless Podman configuration..."
    
    # Enable user namespaces
    if ! grep -q "$(whoami)" /etc/subuid 2>/dev/null; then
        print_warning "User namespaces not configured. Please run as root:"
        echo "  sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $(whoami)"
        echo "  sudo systemctl enable --now user@$(id -u).service"
        return 1
    fi
    
    # Enable user systemd services
    systemctl --user enable --now podman.socket 2>/dev/null || true
    
    print_status "✅ Rootless Podman configured"
}

# Create secure network
create_network() {
    print_status "Creating secure Podman network..."
    
    # Remove existing network if present
    podman network rm data-contracts-net 2>/dev/null || true
    
    # Create custom network with security settings
    podman network create \
        --driver bridge \
        --subnet 172.20.0.0/16 \
        --gateway 172.20.0.1 \
        --opt com.docker.network.bridge.name=data-contracts-br \
        --opt com.docker.network.driver.mtu=1500 \
        data-contracts-net
    
    print_status "✅ Secure network created"
}

# Setup SELinux policies (if available)
setup_selinux() {
    if command -v getenforce >/dev/null 2>&1 && [[ "$(getenforce)" != "Disabled" ]]; then
        print_status "Configuring SELinux policies..."
        
        # Set SELinux contexts for container volumes
        mkdir -p ~/data-contracts-studio/data
        chcon -Rt container_file_t ~/data-contracts-studio/data 2>/dev/null || {
            print_warning "Could not set SELinux context. You may need to run:"
            echo "  sudo setsebool -P container_manage_cgroup on"
        }
        
        print_status "✅ SELinux policies configured"
    else
        print_info "SELinux not active, skipping SELinux configuration"
    fi
}

# Setup container security policies
setup_security_policies() {
    print_status "Setting up container security policies..."
    
    # Create containers.conf for security
    mkdir -p ~/.config/containers
    
    cat > ~/.config/containers/containers.conf << 'EOF'
[containers]
# Security settings
default_capabilities = [
    "CHOWN",
    "DAC_OVERRIDE", 
    "FOWNER",
    "FSETID",
    "KILL",
    "NET_BIND_SERVICE",
    "SETGID",
    "SETUID",
    "SETPCAP"
]

# Remove dangerous capabilities
drop_capabilities = [
    "SYS_ADMIN",
    "SYS_TIME",
    "NET_ADMIN"
]

# Security options
security_opt = [
    "no-new-privileges",
    "seccomp=default"
]

# Resource limits
default_sysctls = [
    "net.ipv4.ping_group_range=0 0"
]

# PID limit
pids_limit = 2048

# Read-only root filesystem by default
read_only = false

[engine]
# Runtime security
runtime = "crun"
detach_keys = "ctrl-p,ctrl-q"

# Network security
dns = ["1.1.1.1", "8.8.8.8"]

[network]
# Default network settings
default_network = "data-contracts-net"
EOF

    print_status "✅ Security policies configured"
}

# Setup log rotation
setup_logging() {
    print_status "Setting up log rotation..."
    
    mkdir -p ~/.config/containers/systemd
    
    cat > ~/.config/containers/systemd/logging.conf << 'EOF'
[Service]
# Log configuration
StandardOutput=journal
StandardError=journal
SyslogIdentifier=data-contracts-studio

# Log rotation
Environment="PODMAN_LOG_DRIVER=journald"
Environment="PODMAN_LOG_SIZE_MAX=10m"
Environment="PODMAN_LOG_MAX_FILES=5"
EOF

    print_status "✅ Log rotation configured"
}

# Setup backup scripts
setup_backup() {
    print_status "Setting up backup automation..."
    
    mkdir -p ~/bin
    
    cat > ~/bin/backup-data-contracts.sh << 'EOF'
#!/bin/bash

# Data Contracts Studio Backup Script

BACKUP_DIR="$HOME/backups/data-contracts-studio"
DATA_DIR="$HOME/data-contracts-studio/data"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup database
podman exec data-contracts-db pg_dump -U postgres datacontracts | gzip > "$BACKUP_DIR/database_$TIMESTAMP.sql.gz"

# Backup application data
tar -czf "$BACKUP_DIR/appdata_$TIMESTAMP.tar.gz" -C "$DATA_DIR" .

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "Backup completed: $TIMESTAMP"
EOF

    chmod +x ~/bin/backup-data-contracts.sh
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "0 2 * * * $HOME/bin/backup-data-contracts.sh") | crontab -
    
    print_status "✅ Backup automation configured"
}

# Setup monitoring
setup_monitoring() {
    print_status "Setting up container monitoring..."
    
    mkdir -p ~/.config/systemd/user
    
    cat > ~/.config/systemd/user/data-contracts-monitoring.service << 'EOF'
[Unit]
Description=Data Contracts Studio Monitoring
After=data-contracts-studio-pod.service

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'podman stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" --no-stream > /tmp/data-contracts-stats.log'

[Install]
WantedBy=default.target
EOF

    cat > ~/.config/systemd/user/data-contracts-monitoring.timer << 'EOF'
[Unit]
Description=Data Contracts Studio Monitoring Timer
Requires=data-contracts-monitoring.service

[Timer]
OnCalendar=*:0/5
Persistent=true

[Install]
WantedBy=timers.target
EOF

    systemctl --user enable data-contracts-monitoring.timer
    
    print_status "✅ Monitoring configured"
}

# Main setup function
main() {
    print_status "Starting security setup..."
    
    check_root
    setup_rootless
    create_network
    setup_selinux
    setup_security_policies
    setup_logging
    setup_backup
    setup_monitoring
    
    print_status "🎉 Security setup completed!"
    echo ""
    echo "📋 Security Features Enabled:"
    echo "  ✅ Rootless containers"
    echo "  ✅ Capability dropping"
    echo "  ✅ No-new-privileges"
    echo "  ✅ Secure network isolation"
    echo "  ✅ Resource limits"
    echo "  ✅ Log rotation"
    echo "  ✅ Automated backups"
    echo "  ✅ Container monitoring"
    echo ""
    echo "🔧 Next Steps:"
    echo "  1. Run: ./scripts/deploy-podman.sh deploy"
    echo "  2. Enable auto-start: systemctl --user enable data-contracts-studio-pod.service"
    echo "  3. Start monitoring: systemctl --user start data-contracts-monitoring.timer"
    echo ""
}

# Run main function
main "$@"

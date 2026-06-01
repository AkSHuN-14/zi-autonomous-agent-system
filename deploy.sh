#!/bin/bash

# ZI Agent System - Production Deployment Script

echo "=========================================="
echo "ZI Agent System - Production Deployment"
echo "=========================================="

# Configuration
PROJECT_DIR="/path/to/agent-system"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_VERSION="3.10"

echo ""
echo "Step 1: Environment Setup"
echo "---------------------------"

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

echo ""
echo "Step 2: Install Dependencies"
echo "------------------------------"

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install production dependencies
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-multipart

echo ""
echo "Step 3: Database Setup"
echo "----------------------"

# Initialize database
cd $PROJECT_DIR
python -c "from production.database import initialize_production_database; initialize_production_database()"

echo ""
echo "Step 4: Configuration"
echo "--------------------"

# Create production config file
if [ ! -f "$PROJECT_DIR/config/production.yaml" ]; then
    cat > $PROJECT_DIR/config/production.yaml <<EOF
server:
  host: 0.0.0.0
  port: 8000
  workers: 4

database:
  type: sqlite
  path: data/agent_system.db

security:
  jwt_secret: $(openssl rand -hex 32)
  session_timeout: 3600

monitoring:
  enable_logging: true
  log_level: INFO
EOF
    echo "Created production configuration file"
fi

echo ""
echo "Step 5: Create Systemd Service"
echo "------------------------------"

# Create systemd service file
sudo tee /etc/systemd/system/zi-agent.service > /dev/null <<EOF
[Unit]
Description=ZI Agent System
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/uvicorn production.api_server:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "Step 6: Enable and Start Service"
echo "--------------------------------"

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable zi-agent.service

# Start service
sudo systemctl start zi-agent.service

echo ""
echo "Step 7: Setup Nginx Reverse Proxy (Optional)"
echo "---------------------------------------------"

# Ask if user wants nginx
read -p "Setup Nginx reverse proxy? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo tee /etc/nginx/sites-available/zi-agent > /dev/null <<EOF
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    # Enable site
    sudo ln -s /etc/nginx/sites-available/zi-agent /etc/nginx/sites-enabled/
    
    # Test nginx configuration
    sudo nginx -t
    
    # Restart nginx
    sudo systemctl restart nginx
fi

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Service Status:"
sudo systemctl status zi-agent.service --no-pager

echo ""
echo "Logs:"
sudo journalctl -u zi-agent.service -f --no-pager

echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/api/v1/health"

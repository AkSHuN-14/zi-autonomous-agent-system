# ZI Agent System - Production Deployment Guide

## Overview
This guide covers deploying the ZI Autonomous Agent System to production environments, including database setup, authentication, monitoring, and scaling considerations.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12+ (for production) or SQLite (for development)
- Nginx (for reverse proxy)
- SSL certificate (for HTTPS)
- 4GB RAM minimum, 8GB recommended
- 20GB disk space minimum

## Quick Deployment

### 1. Clone and Setup

```bash
cd agent-system
pip install -r requirements.txt
```

### 2. Production Dependencies

```bash
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-multipart
```

### 3. Database Setup

```bash
# For SQLite (development)
python -c "from production.database import initialize_production_database; initialize_production_database()"

# For PostgreSQL (production)
# Create database and user in PostgreSQL
# Then update config/production.yaml with database credentials
```

### 4. Configuration

Create `config/production.yaml`:

```yaml
server:
  host: 0.0.0.0
  port: 8000
  workers: 4

database:
  type: postgresql
  host: localhost
  port: 5432
  name: zi_agent_prod
  user: zi_agent
  password: your_secure_password

security:
  jwt_secret: your_jwt_secret_here
  session_timeout: 3600

llm:
  provider: openai
  api_key: your_openai_api_key
  model: gpt-3.5-turbo

monitoring:
  enable_logging: true
  log_level: INFO
  log_file: logs/agent_system.log
```

### 5. Start Server

```bash
# Development
uvicorn production.api_server:app --reload

# Production
uvicorn production.api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

## Deployment Options

### Option 1: Systemd Service (Linux)

```bash
# Create systemd service
sudo nano /etc/systemd/system/zi-agent.service
```

Content:
```ini
[Unit]
Description=ZI Agent System
After=network.target

[Service]
Type=notify
User=your_user
WorkingDirectory=/path/to/agent-system
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn production.api_server:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable zi-agent
sudo systemctl start zi-agent
```

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn[standard] psycopg2-binary

COPY . .

EXPOSE 8000

CMD ["uvicorn", "production.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/zi_agent
      - JWT_SECRET=your_secret
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=zi_agent
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
docker-compose up -d
```

### Option 3: Cloud Deployment

#### AWS
- Use EC2 or ECS
- Deploy with Docker
- Use RDS for PostgreSQL
- Use Application Load Balancer

#### Google Cloud
- Use Cloud Run or GKE
- Use Cloud SQL for PostgreSQL
- Use Cloud Load Balancing

#### Azure
- Use Azure App Service or AKS
- Use Azure Database for PostgreSQL
- Use Azure Application Gateway

## Security Setup

### 1. SSL/TLS Configuration

```bash
# Generate self-signed certificate (for testing)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Or use Let's Encrypt for production
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 2. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 3. Authentication

Default users created:
- Admin: `admin / admin123` (change immediately)
- TA'K$HUN: `TA'K$HUN / tak123` (trusted entity)

Change passwords via API or database.

## Monitoring and Logging

### 1. System Monitoring

Access monitoring endpoints:
- Health check: `GET /api/v1/health`
- Metrics: `GET /api/v1/metrics`
- Logs: Available in `logs/agent_system.log`

### 2. Performance Monitoring

Key metrics to monitor:
- Agent execution time
- Token usage
- API response times
- Error rates
- Memory usage

### 3. Log Rotation

Setup logrotate:

```bash
sudo nano /etc/logrotate.d/zi-agent
```

Content:
```
/path/to/agent-system/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload zi-agent > /dev/null 2>&1 || true
    endscript
}
```

## Scaling Considerations

### Horizontal Scaling

1. Deploy multiple instances behind load balancer
2. Use shared PostgreSQL database
3. Use Redis for session storage
4. Implement connection pooling

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_agent_sessions_user_id ON agent_sessions(user_id);
CREATE INDEX idx_agent_sessions_status ON agent_sessions(status);
CREATE INDEX idx_content_history_user_id ON content_history(user_id);
CREATE INDEX idx_content_history_created_at ON content_history(created_at);
```

### Caching Strategy

- Use Redis for caching frequent queries
- Cache content generation results
- Cache user sessions
- Implement cache invalidation strategy

## Backup and Recovery

### Database Backup

```bash
# PostgreSQL
pg_dump -U user -h localhost zi_agent_prod > backup_$(date +%Y%m%d).sql

# SQLite
cp data/agent_system.db backup_$(date +%Y%m%d).db
```

### Automated Backups

Setup cron job:

```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup_script.sh
```

### Disaster Recovery

1. Regular database backups
2. Backup configuration files
3. Document recovery procedures
4. Test recovery process regularly

## Troubleshooting

### Common Issues

**Service won't start:**
```bash
sudo journalctl -u zi-agent.service -f
```

**Database connection issues:**
```bash
# Check database status
sudo systemctl status postgresql

# Test connection
psql -U user -h localhost -d zi_agent_prod
```

**High memory usage:**
```bash
# Check memory usage
free -h
# Reduce worker count in config
```

**Slow API responses:**
```bash
# Check logs for slow queries
# Add database indexes
# Implement caching
```

## Maintenance

### Regular Tasks

1. **Daily:**
   - Check logs for errors
   - Monitor performance metrics
   - Verify backup completion

2. **Weekly:**
   - Review security logs
   - Analyze usage patterns
   - Update dependencies

3. **Monthly:**
   - Review and rotate logs
   - Security audit
   - Performance optimization review

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart zi-agent
```

## Support and Documentation

- **API Documentation**: Available at `/docs` endpoint
- **System Documentation**: `docs/` directory
- **Blueprint Document**: Original `ZI.io_imp_1_2.md`
- **Setup Guide**: `SETUP.md`

## Performance Tuning

### Database Tuning

```ini
# postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB
maintenance_work_mem = 64MB
```

### Application Tuning

- Adjust worker count based on CPU cores
- Optimize connection pool size
- Enable response compression
- Implement rate limiting

## Security Best Practices

1. **Regular Updates:** Keep dependencies updated
2. **Strong Authentication:** Use strong passwords and MFA
3. **Network Security:** Use firewall and VPN
4. **Data Encryption:** Encrypt sensitive data at rest
5. **Regular Audits:** Conduct security audits
6. **Incident Response:** Have incident response plan

## Cost Optimization

1. **Token Usage:** Monitor and optimize LLM token usage
2. **Resource Allocation:** Right-size server resources
3. **Caching:** Reduce database queries with caching
4. **Compression:** Use compression for API responses
5. **Scaling:** Use auto-scaling for variable workloads

## Completion Checklist

- [x] Core agent architecture implemented
- [x] Content generation system (FVCGen) complete
- [x] Advanced UI/UX interface created
- [x] LLM integration with ToT and inverse prompting
- [x] Database models and authentication system
- [x] Monitoring and logging infrastructure
- [x] API server with REST endpoints
- [x] Deployment scripts and documentation
- [x] Security configuration and best practices
- [x] Scaling and backup strategies

The ZI Autonomous Agent System is now **production-ready** with all core components implemented and deployment infrastructure in place.

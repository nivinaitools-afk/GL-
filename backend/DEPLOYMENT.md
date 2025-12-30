# GetLanded Backend Deployment Guide

## Local Development

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Git

### Setup Steps

1. **Clone and navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL database:**
```bash
# Create database
createdb getlanded

# Or using psql
psql -U postgres
CREATE DATABASE getlanded;
\q
```

5. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

Example `.env`:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/getlanded
SECRET_KEY=your-secret-key-here
DEBUG=True
```

6. **Load seed data:**
```bash
python seeds/load_seeds.py
```

Expected output:
```
Creating default tenant...
✓ Created tenant: University of Example (ID: 1)

Loading skills...
✓ Loaded 50 skills

Loading courses...
✓ Loaded 40 courses

Loading role clusters...
✓ Loaded 15 role clusters

✅ Seed data loaded successfully!

Tenant ID: 1
Use this tenant_id when creating students and making API requests.
```

7. **Run tests:**
```bash
pytest -v
```

8. **Start development server:**
```bash
./run.sh
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

9. **Access the API:**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Docker Deployment

### Using Docker Compose

1. **Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: getlanded
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: yourpassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:yourpassword@db:5432/getlanded
      DEBUG: "True"
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
```

2. **Create `Dockerfile`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Create `.dockerignore`:**
```
venv/
__pycache__/
*.pyc
.env
.git/
.pytest_cache/
*.db
*.sqlite
node_modules/
```

4. **Build and run:**
```bash
docker-compose up -d
```

5. **Load seed data:**
```bash
docker-compose exec api python seeds/load_seeds.py
```

6. **View logs:**
```bash
docker-compose logs -f api
```

7. **Run tests:**
```bash
docker-compose exec api pytest -v
```

## Cloud Deployment

### Heroku

1. **Install Heroku CLI and login:**
```bash
heroku login
```

2. **Create Heroku app:**
```bash
heroku create getlanded-api
```

3. **Add PostgreSQL addon:**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Create `Procfile`:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. **Create `runtime.txt`:**
```
python-3.9.18
```

6. **Deploy:**
```bash
git push heroku main
```

7. **Load seed data:**
```bash
heroku run python seeds/load_seeds.py
```

8. **Open app:**
```bash
heroku open
```

### AWS (EC2 + RDS)

1. **Launch RDS PostgreSQL instance:**
- Engine: PostgreSQL 14
- Instance class: db.t3.micro (free tier)
- Storage: 20 GB
- Enable public access (or use VPC)
- Note the endpoint and credentials

2. **Launch EC2 instance:**
- AMI: Ubuntu 22.04 LTS
- Instance type: t2.micro (free tier)
- Security group: Allow ports 22 (SSH), 8000 (API)

3. **SSH into EC2:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

4. **Setup on EC2:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and PostgreSQL client
sudo apt install python3-pip python3-venv postgresql-client -y

# Clone repository
git clone https://github.com/your-org/getlanded.git
cd getlanded/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/getlanded
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False
EOF

# Load seed data
python seeds/load_seeds.py

# Test the application
pytest -v
```

5. **Setup systemd service:**
```bash
sudo nano /etc/systemd/system/getlanded.service
```

Content:
```ini
[Unit]
Description=GetLanded API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/getlanded/backend
Environment="PATH=/home/ubuntu/getlanded/backend/venv/bin"
ExecStart=/home/ubuntu/getlanded/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Start and enable service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start getlanded
sudo systemctl enable getlanded
sudo systemctl status getlanded
```

7. **Setup Nginx reverse proxy (optional):**
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/getlanded
```

Content:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/getlanded /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### DigitalOcean App Platform

1. **Create `app.yaml`:**
```yaml
name: getlanded-api
services:
  - name: api
    github:
      repo: your-org/getlanded
      branch: main
      deploy_on_push: true
    source_dir: /backend
    build_command: pip install -r requirements.txt
    run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
    http_port: 8080
    environment_slug: python
    instance_size_slug: basic-xxs
    instance_count: 1
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}
      - key: SECRET_KEY
        scope: RUN_TIME
        type: SECRET
databases:
  - name: db
    engine: PG
    version: "14"
    production: true
    cluster_name: getlanded-db
```

2. **Deploy:**
```bash
doctl apps create --spec app.yaml
```

## Production Checklist

### Security
- [ ] Use strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Use HTTPS (SSL certificate)
- [ ] Restrict CORS origins
- [ ] Add rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable database SSL connections
- [ ] Add authentication/authorization

### Performance
- [ ] Enable database connection pooling
- [ ] Add caching (Redis)
- [ ] Configure CDN for static assets
- [ ] Set up database indexes
- [ ] Monitor query performance
- [ ] Use async workers (gunicorn + uvicorn)

### Monitoring
- [ ] Setup logging (CloudWatch, Datadog, Sentry)
- [ ] Add health check endpoints
- [ ] Configure alerts for errors
- [ ] Track API response times
- [ ] Monitor database connections
- [ ] Setup uptime monitoring

### Backup & Recovery
- [ ] Automated database backups
- [ ] Test restore procedure
- [ ] Document recovery process
- [ ] Store backups in different region

### CI/CD
- [ ] Automated tests on push
- [ ] Automated deployments
- [ ] Staging environment
- [ ] Rollback strategy

## Environment Variables

### Required
```
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-secret-key-here
```

### Optional
```
DEBUG=False
CORS_ORIGINS=https://app.getlanded.com,https://www.getlanded.com
LOG_LEVEL=INFO
MAX_CONNECTIONS=100
```

## Database Migrations (Future)

When using Alembic for migrations:

```bash
# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Troubleshooting

### Database connection refused
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U postgres -h localhost -d getlanded
```

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Tests failing
```bash
# Make sure using test database
export DATABASE_URL=sqlite:///./test.db
pytest -v
```

## Support

For deployment issues:
- Check logs: `docker-compose logs -f` or `journalctl -u getlanded -f`
- Verify environment variables
- Check database connectivity
- Review firewall rules
- Consult API docs: http://your-domain.com/docs

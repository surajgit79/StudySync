# StudySync - Setup Instructions

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+ & npm** - [Download](https://nodejs.org/)
- **MongoDB 6.0+** - [Download](https://www.mongodb.com/try/download/community)
- **Redis** (for Celery & Channels) - [Download](https://redis.io/download)
- **Git** - [Download](https://git-scm.com/downloads)

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the `backend` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB Configuration
MONGO_DB_NAME=studysync_db
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=
MONGO_PASSWORD=

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=1440  # minutes (24 hours)
JWT_REFRESH_TOKEN_LIFETIME=10080  # minutes (7 days)

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Email Configuration (optional, for email verification)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Machine Learning Settings
ML_MODEL_PATH=../algorithms/models/
ML_ENABLE_TRAINING=True
```

### 5. Initialize Django Project
```bash
# Create Django project
django-admin startproject studysync_backend .

# Create Django apps
python manage.py startapp users
python manage.py startapp groups
python manage.py startapp sessions
python manage.py startapp analytics
python manage.py startapp gamification
python manage.py startapp recommendations
python manage.py startapp messaging
```

### 6. Database Setup
```bash
# Start MongoDB service
# Windows: net start MongoDB
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod

# Verify MongoDB is running
mongosh
# In mongo shell: show dbs
# Exit: exit
```

### 7. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 9. Load Initial Data (Optional)
```bash
python manage.py loaddata initial_achievements.json
python manage.py loaddata sample_users.json
```

### 10. Run Development Server
```bash
python manage.py runserver
```

Backend should now be running at `http://localhost:8000`

### 11. Run Celery Worker (Separate Terminal)
```bash
# Windows
celery -A studysync_backend worker -l info --pool=solo

# macOS/Linux
celery -A studysync_backend worker -l info
```

### 12. Run Celery Beat (Separate Terminal - for scheduled tasks)
```bash
celery -A studysync_backend beat -l info
```

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration
Create a `.env` file in the `frontend` directory:

```env
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENVIRONMENT=development
```

### 4. Run Development Server
```bash
npm start
```

Frontend should now be running at `http://localhost:3000`

## Redis Setup

### Windows
1. Download Redis for Windows from [GitHub](https://github.com/microsoftarchive/redis/releases)
2. Extract and run `redis-server.exe`

### macOS
```bash
brew install redis
brew services start redis
```

### Linux
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

### Verify Redis
```bash
redis-cli ping
# Should return: PONG
```

## Verification

### 1. Check Backend
- Visit `http://localhost:8000/admin` - Django admin panel
- Visit `http://localhost:8000/api/v1/` - API root
- Visit `http://localhost:8000/swagger/` - API documentation

### 2. Check Frontend
- Visit `http://localhost:3000` - React app should load

### 3. Check Services
```bash
# MongoDB
mongosh --eval "db.version()"

# Redis
redis-cli ping

# Celery
celery -A studysync_backend inspect active
```

## Initial Data Population (for Development/Testing)

### Generate Synthetic User Data
```bash
cd algorithms
python generate_synthetic_data.py --users 100 --groups 20 --sessions 500
```

### Train Initial ML Models
```bash
python train_models.py --all
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest
pytest --cov  # With coverage report
```

### Frontend Tests
```bash
cd frontend
npm test
npm test -- --coverage  # With coverage report
```

## Common Issues & Solutions

### Issue: MongoDB Connection Error
**Solution:**
- Verify MongoDB is running: `mongosh`
- Check credentials in `.env`
- Ensure firewall allows port 27017

### Issue: Redis Connection Error
**Solution:**
- Verify Redis is running: `redis-cli ping`
- Check Redis host/port in `.env`

### Issue: Celery Worker Not Starting (Windows)
**Solution:**
- Use `--pool=solo` flag for Windows
- Or use WSL2 for better compatibility

### Issue: Port Already in Use
**Solution:**
```bash
# Backend - use different port
python manage.py runserver 8001

# Frontend - use different port
PORT=3001 npm start
```

### Issue: Module Import Errors
**Solution:**
```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
rm -rf node_modules package-lock.json
npm install
```

## Development Workflow

1. **Start Services** (in order):
   ```bash
   # Terminal 1: MongoDB
   mongod

   # Terminal 2: Redis
   redis-server

   # Terminal 3: Django
   cd backend
   python manage.py runserver

   # Terminal 4: Celery Worker
   cd backend
   celery -A studysync_backend worker -l info

   # Terminal 5: React
   cd frontend
   npm start
   ```

2. **Make Changes** - Edit code in your IDE

3. **Test Changes** - Run tests before committing

4. **Commit** - Use meaningful commit messages

## Project Structure After Setup

```
StudySync/
├── backend/
│   ├── studysync_backend/      # Main Django project
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                  # User management app
│   ├── groups/                 # Study groups app
│   ├── sessions/               # Study sessions app
│   ├── analytics/              # Analytics app
│   ├── gamification/           # Gamification app
│   ├── recommendations/        # Recommendation app
│   ├── messaging/              # Messaging app
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── utils/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env
├── algorithms/
│   ├── matching/
│   ├── clustering/
│   ├── graph/
│   ├── recommendation/
│   ├── prediction/
│   └── utils/
├── docs/
│   ├── README.md
│   ├── PROJECT_PROPOSAL.md
│   └── SETUP_INSTRUCTIONS.md
└── .gitignore
```

## Next Steps

1. Review project documentation in `docs/`
2. Explore API documentation at `/swagger/`
3. Set up your IDE (PyCharm/VS Code)
4. Create a feature branch for development
5. Start implementing features according to the project plan

## Useful Commands

### Django Management
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
python manage.py collectstatic
```

### Database
```bash
# MongoDB shell
mongosh studysync_db

# Export data
mongoexport --db studysync_db --collection users --out users.json

# Import data
mongoimport --db studysync_db --collection users --file users.json
```

### Code Quality
```bash
# Backend
black .
flake8 .
pylint **/*.py

# Frontend
npm run lint
npm run format
```

## Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review API docs at `/swagger/`
3. Check Django logs in console
4. Enable DEBUG mode in `.env` for detailed errors

---

**Happy Coding! 🚀**

Perfect! Here's a comprehensive **README.md** for your SafeSpace project:

```markdown
# 🧠 SafeSpace - AI Mental Health Therapist

SafeSpace is an AI-powered mental health companion built with FastAPI and Streamlit. It provides 24/7 emotional support, stress management guidance, and coping strategies through intelligent conversational AI.

![SafeSpace](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## ✨ Features

- 🔐 **Secure Authentication** - JWT-based user authentication with password hashing
- 💬 **AI-Powered Conversations** - Intelligent responses using LangChain and AI agents
- 📚 **Chat History** - Persistent conversation storage with load last 15 messages feature
- 🗑️ **History Management** - Clear chat history functionality
- 📊 **Usage Tracking** - Monthly message limits and usage statistics
- 🎨 **Modern UI** - Clean, responsive Streamlit interface with professional styling
- 🔒 **Privacy-Focused** - User data encrypted and securely stored
- 🚀 **Production Ready** - SQLite for local, PostgreSQL for deployment

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **LangChain** - Framework for developing AI applications
- **Passlib** - Password hashing library (bcrypt)
- **Python-Jose** - JWT token creation and validation
- **Uvicorn** - ASGI server

### Frontend
- **Streamlit** - Fast way to build data apps
- **Requests** - HTTP library for API calls

### Database
- **SQLite** - Local development database
- **PostgreSQL** - Production database (Render deployment)

### Package Manager
- **uv** - Fast Python package installer and resolver

## 📋 Prerequisites

- Python 3.11 or higher
- uv package manager
- API keys for AI services (OpenAI, Anthropic, etc.)

## 🚀 Installation

### 1. Clone the Repository

```
git clone https://github.com/Aftab073/SAFESPACE-AI-AGENT.git
cd safespace
```

### 2. Install uv (if not already installed)

```
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install Dependencies

```
uv sync
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```
# Backend Configuration
BACKEND_URL=http://localhost:8000

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database (leave empty for SQLite, or add PostgreSQL URL for production)
DATABASE_URL=

# AI Service API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

## ▶️ Running the Application

### Start the Backend Server

```
uv run python main.py
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### Start the Frontend

In a separate terminal:

```
uv run streamlit run frontend.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
safespace/
├── ai_agent.py          # AI agent logic with LangChain
├── auth.py              # Authentication (JWT, password hashing)
├── config.py            # Configuration settings
├── database.py          # Database models and operations
├── frontend.py          # Streamlit UI
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── tools.py             # AI agent tools
├── .env                 # Environment variables (create this)
├── pyproject.toml       # Project dependencies
├── uv.lock              # Dependency lock file
└── README.md            # This file
```

## 🔌 API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile

### Chat

- `POST /ask` - Send message to AI (protected)
- `GET /chat/history?limit=15` - Get chat history (protected)
- `DELETE /chat/history` - Clear chat history (protected)

### Usage

- `GET /usage` - Get usage statistics (protected)

### Health

- `GET /health` - Health check endpoint


### Database Setup

1. Create a **PostgreSQL** database on Render
2. Copy the **Internal Database URL**
3. Add it as `DATABASE_URL` environment variable to your backend service

## 🗄️ Database Schema

### Users Table
- `id` - UUID primary key
- `email` - Unique email address
- `full_name` - Optional full name
- `password_hash` - Bcrypt hashed password
- `created_at` - Registration timestamp
- `is_active` - Account status

### Chat History Table
- `id` - UUID primary key
- `user_id` - Foreign key to users
- `message` - User message
- `response` - AI response
- `tool_used` - AI tool used
- `created_at` - Message timestamp

### User Usage Table
- `user_id` - Primary key, foreign key to users
- `messages_used_this_month` - Message count
- `current_period_start` - Billing period start
- `current_period_end` - Billing period end
- `last_reset_date` - Last reset timestamp

## 🎨 Features Overview

### Welcome Message
Users are greeted with a professional welcome message explaining SafeSpace capabilities:
- Stress management
- Mood tracking
- Coping strategies
- Safe space for expression

### Chat History
- Load last 15 messages for quick context
- Clear all history with one click
- Automatic saving of all conversations

### Usage Tracking
- 50 messages per month (free tier)
- Automatic monthly reset
- Usage statistics display

## 🔒 Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- Environment-based secret keys
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for frontend access

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 👨‍💻 Author

Aftab Tamboli - [GitHub](https://github.com/Aftab073)

## 🙏 Acknowledgments

- OpenAI for AI capabilities
- Streamlit for the amazing UI framework
- FastAPI for the robust backend framework
- LangChain for AI agent orchestration


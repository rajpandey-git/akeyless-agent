# 🔐 Akeyless AI Agent

An intelligent AI-powered assistant for managing Akeyless secrets, built with Google Gemini AI and Streamlit.

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

[![Build and Push Docker Image](https://github.com/rajpandey-git/akeyless-agent/actions/workflows/docker-build-push.yml/badge.svg)](https://github.com/rajpandey-git/akeyless-agent/actions/workflows/docker-build-push.yml)
[![Docker Hub](https://img.shields.io/docker/pulls/rajpandey111/akeyless-ai-agent)](https://hub.docker.com/r/rajpandey111/akeyless-ai-agent)

---

## ✨ Features

- 🤖 **AI-Powered Chat Interface** - Natural language queries using Google Gemini
- 🔐 **Secret Management** - View, retrieve, and manage Akeyless secrets
- 📊 **Analytics Dashboard** - Visual statistics and secret distribution
- 🔍 **Secret Browser** - Browse and search secrets by path and type
- 💬 **Conversational AI** - Ask questions in plain English
- 🎨 **Modern Web UI** - Beautiful, responsive Streamlit interface
- 🐳 **Docker Ready** - Easy deployment with Docker/Docker Compose

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull the image
docker pull rajpandey111/akeyless-ai-agent:latest

# Run the container
docker run -d \
  --name akeyless-agent \
  -p 8501:8501 \
  -e AKEYLESS_ACCESS_ID=your_access_id \
  -e AKEYLESS_ACCESS_KEY=your_access_key \
  -e GEMINI_API_KEY=your_gemini_key \
  rajpandey111/akeyless-ai-agent:latest

# Access the app
open http://localhost:8501
```

### Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/rajpandey-git/akeyless-agent.git
cd akeyless-agent

# Create .env file with your credentials
cp .env.example .env
# Edit .env with your actual credentials

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📋 Prerequisites

- **Akeyless Account** with API access
- **Google Gemini API Key** (Free tier available)
- **Docker** (for containerized deployment)
- **Python 3.11+** (for local development)

---

## 🔧 Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/rajpandey-git/akeyless-agent.git
cd akeyless-agent
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements_web.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
AKEYLESS_ACCESS_ID=your_access_id
AKEYLESS_ACCESS_KEY=your_access_key
AKEYLESS_GATEWAY_URL=https://api.akeyless.io
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Run the application

#### Web UI:
```bash
streamlit run akeyless_web_ui.py
```

#### CLI Agent:
```bash
python akeyless_gemini_agent.py
```

---

## 📖 Usage Examples

### Chat Interface

```
You: List all my secrets
Agent: You have 6 secrets: 3 static, 2 rotated, 1 other

You: Get the secret secrets/MysecondSecret
Agent: Here's the secret:
  Username: rajpandey111
  Password: ****
  
You: How many rotated secrets do I have?
Agent: You have 2 rotated secrets
```

### Secret Browser

1. Navigate to **Secret Browser** tab
2. Enter path (e.g., `/prod`)
3. Filter by type (Static/Rotated/Dynamic)
4. Click **Get Value** to retrieve secret

### Analytics

View comprehensive statistics:
- Total secret count
- Distribution by type
- Visual charts
- Detailed breakdowns

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  Gemini AI Agent    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Akeyless Client    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Akeyless API       │
└─────────────────────┘
```

---

## 🐳 Docker Image

### Supported Platforms

- `linux/amd64` - Intel/AMD processors
- `linux/arm64` - ARM processors (Apple Silicon, ARM servers)

### Available Tags

- `latest` - Latest stable build
- `v1.0.0` - Specific version
- `main-abc1234` - Build from specific commit

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AKEYLESS_ACCESS_ID` | Yes | - | Akeyless access ID |
| `AKEYLESS_ACCESS_KEY` | Yes | - | Akeyless access key |
| `AKEYLESS_GATEWAY_URL` | No | `https://api.akeyless.io` | Akeyless gateway URL |
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |

---

## 🔒 Security

- ✅ Environment variables for sensitive data
- ✅ No hardcoded credentials
- ✅ `.env` file excluded from git
- ✅ Docker secrets support
- ✅ HTTPS for all API calls

**⚠️ Never commit `.env` file or credentials to git!**

---

## 📊 CI/CD Pipeline

Automated Docker builds triggered by:

- ✅ Push to main/master branch
- ✅ Version tags (`v1.0.0`)
- ✅ Pull requests
- ✅ Manual workflow trigger

Pipeline automatically:
1. Builds multi-platform Docker images
2. Pushes to Docker Hub
3. Tags with version/branch/commit info
4. Caches layers for faster builds

---

## 🛠️ Troubleshooting

### Container won't start
```bash
# Check logs
docker logs akeyless-agent

# Verify environment variables
docker exec akeyless-agent env | grep AKEYLESS
```

### Port already in use
```bash
# Use different port
docker run -p 8502:8501 ...
```

### API rate limits
- Gemini free tier: 60 requests/minute
- Switch to paid tier or wait for reset

---

## 📝 Project Structure

```
akeyless-agent/
├── .github/
│   └── workflows/
│       └── docker-build-push.yml   # CI/CD pipeline
├── akeyless_gemini_agent.py        # AI agent logic
├── akeyless_web_ui.py              # Streamlit web interface
├── requirements_web.txt            # Python dependencies
├── Dockerfile                      # Docker image definition
├── docker-compose.yml              # Docker Compose config
├── .dockerignore                   # Docker ignore rules
├── .env.example                    # Environment template
└── README.md                       # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [Akeyless](https://www.akeyless.io/) - Secret management platform
- [Google Gemini](https://ai.google.dev/) - AI language model
- [Streamlit](https://streamlit.io/) - Web framework

---

## 📧 Contact

- **GitHub**: [@rajpandey-git](https://github.com/rajpandey-git)
- **Docker Hub**: [rajpandey111](https://hub.docker.com/u/rajpandey111)

---

⭐ **Star this repo if you find it useful!**

🐛 **Found a bug?** [Open an issue](https://github.com/rajpandey-git/akeyless-agent/issues)

💡 **Have a feature request?** [Start a discussion](https://github.com/rajpandey-git/akeyless-agent/discussions)

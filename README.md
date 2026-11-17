# OmniPost 🚀
### Automated Multi-Platform Posting System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

OmniPost is a high-performance REST API built with **FastAPI** that automatically publishes short promotional and announcement messages across **5 independent third-party platforms** simultaneously via their official APIs.

---

## 🌟 Supported Platforms

| # | Platform | Integration Method | Public Access |
|---|----------|-------------------|:-------------:|
| 1 | **Mastodon** | Official REST API v1 (`/api/v1/statuses`) | ✅ Yes |
| 2 | **Telegram** | Bot API (`sendMessage` to public channel) | ✅ Yes |
| 3 | **GitHub Gist** | GitHub REST API (`/gists`) | ✅ Yes |
| 4 | **Discord** | Channel Webhook API | ✅ Yes |
| 5 | **Dpaste** | Public Code/Snippet API | ✅ Yes |

---

## 🏗️ Architecture & Design Principles

- **Abstract Base Class (`BasePlatform`)**: All platform integrations inherit from a unified base interface ensuring consistent contracts.
- **Fail-Safe Isolation**: Each platform call is isolated inside try/except blocks. If any platform encounters rate limits or errors, remaining platforms continue publishing without interruption.
- **Strict Input Validation**: Pydantic model validators enforce:
  - Message length $\le$ 200 characters.
  - Exactly one valid Call-To-Action (CTA) URL (`http://` or `https://`).
  - RFC-compliant URL pattern validation.
- **12-Factor App Configuration**: Sensitive credentials are read strictly from environment variables via `python-dotenv`.

---

## 📁 Project Structure

```text
omnipost/
├── app/
│   ├── __init__.py
│   ├── config.py              # Environment configuration loader
│   ├── main.py                # FastAPI entry point & routes
│   ├── schemas.py             # Pydantic validation schemas
│   ├── platforms/             # Independent platform drivers
│   │   ├── __init__.py
│   │   ├── base.py            # BasePlatform abstract class
│   │   ├── mastodon.py
│   │   ├── telegram.py
│   │   ├── github_gist.py
│   │   ├── discord.py
│   │   └── dpaste.py
│   └── services/
│       ├── __init__.py
│       └── posting_service.py # Parallel / resilient platform orchestrator
├── tests/
│   └── test_posting.py        # Automated test suite
├── .env.example               # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/danimadhavapuri/omnipost.git
cd omnipost
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your credentials in `.env`.

### 5. Start the Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

Interactive API documentation (Swagger UI) is available at:
👉 **http://localhost:4000/docs**

---

## 📡 API Specification

### Endpoint
```http
POST /posting
Content-Type: application/json
```

### Sample Request
```json
{
  "message": "OmniPost Live Multi-Platform Broadcast Test! https://github.com/danimadhavapuri/omnipost"
}
```

### Sample Response (Verified Live Output)
```json
{
  "success": true,
  "total_platforms": 5,
  "successful": 5,
  "failed": 0,
  "results": [
    {
      "platform": "Mastodon",
      "status": "success",
      "posted_url": "https://mastodon.social/@danim2005/117629990298242765",
      "public_access": true,
      "date": "2026-11-17",
      "time": "10:24:09",
      "error": null
    },
    {
      "platform": "Telegram",
      "status": "success",
      "posted_url": "https://t.me/omnipost_test_channel/6",
      "public_access": true,
      "date": "2026-11-17",
      "time": "10:24:10",
      "error": null
    },
    {
      "platform": "GitHub Gist",
      "status": "success",
      "posted_url": "https://gist.github.com/danimadhavapuri/14ad07d11218a9a4e6762ae5c25c1667",
      "public_access": true,
      "date": "2026-11-17",
      "time": "10:24:11",
      "error": null
    },
    {
      "platform": "Discord",
      "status": "success",
      "posted_url": "https://discord.com/channels/@me/1572102992298246227/1572112436486611076",
      "public_access": true,
      "date": "2026-11-17",
      "time": "10:24:14",
      "error": null
    },
    {
      "platform": "Dpaste",
      "status": "success",
      "posted_url": "https://dpaste.org/XUTz9",
      "public_access": true,
      "date": "2026-11-17",
      "time": "10:24:14",
      "error": null
    }
  ]
}
```

---

## 🧪 Running Automated Tests
```bash
pytest tests/test_posting.py -v
```

---

## 👤 Author
- **Dani Madhavapuri**
- GitHub: [@danimadhavapuri](https://github.com/danimadhavapuri)
- Repository: [omnipost](https://github.com/danimadhavapuri/omnipost)
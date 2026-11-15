# OmniPost 🚀
### Automated Multi-Platform Posting System

Post your message to 5+ platforms with a single API call.

**Built with:** Python 3.x · FastAPI · Uvicorn · Pydantic · HTTPX

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/danimadhavapuri/omnipost.git
cd omnipost
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 5. Run the server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

### 6. Open API docs
Visit: http://localhost:4000/docs

---

## Platforms (Coming Soon — Day 2)
- Reddit
- Mastodon
- Telegram
- Blogger
- Pastebin

---

*Practical Test — Dxora Technologies*
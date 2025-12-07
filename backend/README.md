# AINovel Backend

FastAPI backend for AI Novel collaborative writing platform.

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/ainovel
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
```
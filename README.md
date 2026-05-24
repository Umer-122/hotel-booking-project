# Hotel Booking Form Project

A complete hotel booking system built with FastAPI, HTML, and PostgreSQL.

## Features
- Beautiful responsive booking form
- FastAPI backend with validation
- PostgreSQL database integration
- Deployed on Vercel

## Setup Instructions

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd hotel-booking-project
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/hotel_booking
```

### 5. Run Locally
```bash
python main.py
```
Visit: http://localhost:8000

## Deployment on Vercel
1. Push code to GitHub
2. Connect GitHub repo to Vercel
3. Add environment variables
4. Deploy

## Live URL
[Your Vercel deployment URL here]
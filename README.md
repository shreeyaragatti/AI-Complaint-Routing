# AI Complaint Prioritization & Smart Routing System

An intelligent complaint management system that uses NLP to automatically categorize, prioritize, and route citizen/customer complaints to the appropriate departments with predicted resolution times.

## Features

- **Text Preprocessing**: Normalizes text, removes stopwords, and extracts linguistic features
- **Category Classification**: Classifies complaints into 10+ categories (Water Supply, Electricity, Roads, Sanitation, Healthcare, Education, Public Safety, Environment, Housing, Public Transport)
- **Severity Detection**: Determines CRITICAL, HIGH, MEDIUM, or LOW severity levels
- **Emotion Analysis**: Detects user emotion (Angry, Frustrated, Anxious, Urgent, Neutral) to prioritize sensitive cases
- **Priority Scoring**: Weighted algorithm (0-100) combining severity, emotion, similarity, location, and historical data
- **Duplicate Detection**: Jaccard similarity + TF-IDF based similarity detection
- **Location Analysis**: Identifies priority locations (schools, hospitals, public areas)
- **Historical Data Analysis**: Detects recurring issues and complaint spikes
- **Smart Assignment**: Routes to specific departments and assigns officers based on workload and severity
- **SLA Prediction**: Predicts resolution time ranges based on severity and priority
- **Admin Dashboard**: Real-time analytics with interactive charts and complaint management

## Architecture

```
USER COMPLAINT
     │
     ▼
Text Preprocessing
     │
     ├──────────┼──────────┐
     ▼          ▼          ▼
  Category    Severity    Emotion
  Model       Model       Analysis
     │          │          │
     └──────────┼──────────┘
                ▼
         Priority Engine
                │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
Similarity   Location    Historical
Detection    Analysis      Data
     │          │          │
     └──────────┼──────────┘
                ▼
         Priority Score
                │
                ▼
         Smart Assignment
                │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
  Department  Officer    SLA Prediction
                │
                ▼
          ADMIN DASHBOARD
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask (Python) |
| Frontend | HTML, CSS, JavaScript |
| NLP/ML | Custom keyword-based models, Jaccard/TF-IDF similarity |
| Database | SQLite |
| Visualization | Chart.js |

## Project Structure

```
D:\AI Complaint Routing\
├── app.py                  # Flask REST API server
├── ai_engine.py            # Core AI pipeline (preprocessing, classification, scoring, routing)
├── database.py             # SQLite database layer
├── seed_data.py            # Sample data generator (20 complaints)
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html          # Landing page
│   ├── submit.html         # Complaint submission form
│   └── dashboard.html      # Admin analytics dashboard
├── static/
│   ├── style.css           # Responsive CSS styling
│   └── app.js              # Frontend JavaScript
└── complaints.db           # SQLite database
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd D:\AI Complaint Routing
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database and seed sample data:
```bash
python seed_data.py
```

4. Start the Flask server:
```bash
python app.py 


```

5. Open your browser:
- Home: http://localhost:5000
- Submit Complaint: http://localhost:5000/submit
- Admin Dashboard: http://localhost:5000/dashboard

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/complaint` | Submit a new complaint |
| GET | `/api/complaints` | Get all complaints |
| GET | `/api/complaints/<id>` | Get specific complaint |
| PUT | `/api/complaints/<id>/status` | Update complaint status |
| PUT | `/api/complaints/<id>/resolve` | Mark complaint as resolved |
| GET | `/api/analytics` | Get analytics data |

### Submit Complaint Example

```bash
curl -X POST http://localhost:5000/api/complaint \
  -H "Content-Type: application/json" \
  -d '{
    "text": "There has been a major water pipe leakage near the school since morning. Water is flooding the road.",
    "name": "John Doe",
    "contact": "john@example.com",
    "location": "Main Street"
  }'
```

### Response Example

```json
{
  "success": true,
  "complaint_id": 22,
  "preprocessed_text": "major water pipe leakage near school morning water flooding road",
  "category": "Water Supply",
  "category_confidence": 1.0,
  "severity": "HIGH",
  "severity_confidence": 1.0,
  "emotion": "Urgent",
  "priority_score": 98.0,
  "department": "Water Management Department",
  "officer": "Eng. Ramesh Kumar",
  "urgency": "Within 24 hours",
  "similar_cases": 2,
  "similar_ids": [2, 10],
  "predicted_sla": "2-8 hours",
  "location_analysis": "User specified location: Main Street; Location indicators found: near; Priority location detected: school; Single priority location - moderate visibility",
  "historical_data": "Moderate complaint volume in Water Supply (5 total); High average priority (85.0)",
  "status": "Pending",
  "timestamp": "2026-08-08T19:21:07.361105"
}
```

## Database Schema

```sql
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    preprocessed_text TEXT,
    category TEXT,
    severity TEXT,
    emotion TEXT,
    priority_score REAL,
    department TEXT,
    officer TEXT,
    urgency TEXT,
    similar_cases INTEGER DEFAULT 0,
    predicted_sla TEXT,
    location_analysis TEXT,
    historical_data TEXT,
    status TEXT DEFAULT 'Pending',
    complainant_name TEXT,
    contact TEXT,
    location TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT,
    resolved_at TEXT
);
```

## Priority Score Calculation

The priority score (0-100) is calculated using a weighted combination of:

| Factor | Weight | Description |
|--------|--------|-------------|
| Base Score | 20 | Default baseline |
| Severity | 25 | CRITICAL=25, HIGH=18, MEDIUM=10, LOW=5 |
| Emotion | 10 | Angry=10, Urgent=9, Anxious=8, Frustrated=7, Neutral=3 |
| Similarity | 10 | Number of similar complaints found |
| Location | 10 | Priority locations (schools, hospitals, etc.) |
| Historical | 10 | Category volume and recurring issues |
| Time | 10 | Time-based urgency indicators |
| Text Quality | 5 | Detailed descriptions get bonus |

## Officer Assignment Logic

Officers are assigned based on severity and priority score:
- **CRITICAL or Score ≥ 85**: Primary officer (senior/most experienced)
- **HIGH or Score ≥ 70**: Secondary officer
- **MEDIUM/LOW**: Tertiary officer or general assignment

## SLA Prediction

| Severity | Base SLA | With High Priority (≥90) | With Low Priority (≤40) |
|----------|----------|-------------------------|------------------------|
| CRITICAL | 1-4 hours | 1-3 hours | 1-4 hours |
| HIGH | 2-8 hours | 2-7 hours | 2-10 hours |
| MEDIUM | 4-24 hours | 4-24 hours | 4-30 hours |
| LOW | 8-48 hours | 8-48 hours | 10-48 hours |

## Dashboard Features

- **Stats Cards**: Total complaints, average priority, pending count, resolved count
- **Charts**: Categories (doughnut), Severity (bar), Emotions (pie), Officer workload (horizontal bar), Departments (pie), Status (pie)
- **Complaint Table**: View all complaints with severity, emotion, priority, department, officer, and status
- **Actions**: Update status, mark as resolved

## Sample Complaints

The system comes pre-seeded with 20 sample complaints covering various categories for testing and demonstration purposes.

## License

MIT License

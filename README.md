# Resume Screener Assistant

An AI-powered resume screening application that evaluates candidate resumes against job descriptions and generates structured candidate match reports.

## 1. Project Overview

The Resume Screener Assistant helps recruiters perform an initial comparison between a candidate's resume and a job description.

The application uses Google's Gemini API to generate a structured report containing:

- Candidate name
- Job match score (0–100)
- Five matching skills
- Three skill gaps
- Three suggested interview questions
- Candidate fit summary

The application also maintains an analysis history using SQLite.

**Important:** This application provides decision support only. It must not be used as an automatic hiring or rejection system.

## 2. Features

- Enter job descriptions manually.
- Upload resumes in TXT, PDF and DOCX formats.
- Extract text from uploaded documents.
- Analyse resumes using the Gemini API.
- Generate structured JSON responses.
- Validate AI responses using Pydantic.
- Save analysis reports in SQLite.
- Search analysis history by candidate name.
- Filter candidates by match-score range.
- Handle empty inputs and invalid AI responses.
- Truncate excessively long inputs before analysis.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Programming language | Python |
| AI model | Google Gemini |
| AI integration | google-genai |
| Data validation | Pydantic |
| Database | SQLite |
| PDF processing | pypdf |
| DOCX processing | python-docx |
| Environment configuration | python-dotenv |
| Testing | pytest |

## 4. Project Structure

```text
resume-screener-assistant/
│
├── app.py
├── ai_engine.py
├── schemas.py
├── database.py
├── resume_parser.py
│
├── tests/
│   ├── test_schemas.py
│   ├── test_database.py
│   ├── test_resume_parser.py
│   └── test_ai_engine.py
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
└── AI_USAGE.md
```

The SQLite database file is generated locally when the application initializes.

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or newer
- Google Gemini API key
- Internet connection for Gemini API access

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd resume-screener-assistant
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_available_gemini_model
```

Never commit the `.env` file or expose your API key.

### Step 5: Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 6. Application Architecture

The application follows a modular architecture.

### Frontend — app.py

Responsible for:
- User input
- Resume uploads
- Navigation
- Displaying candidate reports
- Searching and filtering analysis history

### Resume Parser — resume_parser.py

Extracts readable text from TXT, PDF and DOCX files.

Scanned PDFs without an embedded text layer are not supported by the current parser.

### AI Engine — ai_engine.py

Responsible for:
- Gemini API communication
- Prompt construction
- Structured response generation
- Handling API errors
- Validating the returned report

### Schema Validation — schemas.py

Uses Pydantic to validate:
- Candidate name
- Match score boundaries
- Exactly five matching skills
- Exactly three skill gaps
- Exactly three interview questions
- Required report fields

### Database — database.py

Uses SQLite to store validated reports and retrieve them using candidate-name and score filters.

## 7. Data Handling and Privacy

- Resume text is sent to the configured Gemini API for analysis.
- Original resume and job description text are not stored in the local SQLite database.
- Generated analysis reports are stored locally.
- API keys are loaded from environment variables.
- Users should avoid uploading unnecessary personal or sensitive information.
- Production deployment should include appropriate access controls, encryption, retention policies and candidate-data handling procedures.

## 8. Running Tests

Run the automated test suite:

```bash
python -m pytest tests -v
```

The test suite covers schema validation, database operations, document extraction and AI-engine error handling.

## 9. Current Limitations

- Scanned PDFs requiring OCR are not supported.
- Resume parsing currently focuses on document text extraction.
- Gemini API availability and usage limits may affect analysis.
- Match scores are AI-generated estimates, not objective measures of candidate quality.
- The application does not make automatic hiring decisions.
- The current prototype does not implement user authentication or role-based access control.

## 10. Future Improvements

- OCR support for scanned resumes.
- More comprehensive resume parsing.
- Improved candidate comparison and ranking.
- Authentication and access control.
- Database migration and deployment support.
- Enhanced evaluation of AI-generated match scores.

## 11. Responsible Use

The application is intended to assist recruiters in reviewing job-related evidence. Recruiters must independently verify qualifications and experience, avoid discriminatory criteria, and make all hiring decisions through human review.
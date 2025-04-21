# 📄 Cv-To-Job-Description-Matcher

An AI-powered pipeline built using [CrewAI] to analyze candidate resumes, extract structured job descriptions, and compute match scores for better hiring decisions. Whether you're a recruiter or a job-seeker, this tool gives you clear insight into job-candidate compatibility, gaps, and improvements.

---

## 🚀 Features

✅ **CV Extraction**  
Parses PDF, DOCX, or TXT resumes and extracts:
- Professional summary
- Technical skills
- Education history
- Work experience
- Certifications

✅ **Job Parsing**  
Fetches job postings from URLs and extracts:
- Job title
- Required skills
- Key responsibilities
- Education and experience requirements

✅ **Intelligent Matching**  
- Compares CV and job data
- Calculates match percentage (0–100%)
- Ranks jobs by match score
- Highlights qualification gaps
- Provides personalized improvement suggestions

✅ **Modular Agent Design**  
Powered by CrewAI agents:
- `cv_reader_agent`
- `job_parser_agent`
- `matcher_agent`

---

## 📂 Project Structure



---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Robel-GH/Cv-To-Job-Description-Matcher.git
cd Cv-To-Job-Description-Matcher

crewai install
crewai run


# TalentLens AI

> AI-powered CV intelligence platform that transforms unstructured PDF resumes into structured candidate profiles using LLM-based information extraction.

TalentLens AI is an intelligent CV analysis application designed to help recruiters and HR teams extract useful candidate information automatically from PDF resumes.

The system takes a candidate's CV, extracts its text, sends the extracted content to an AI/LLM backend, and converts the unstructured resume into structured candidate information that can be easily reviewed, edited, analyzed, and exported.

---

## ✨ Features

- 📄 Upload candidate CVs in PDF format
- 🔍 Automatically extract text from PDFs
- 🤖 Analyze CV content using an LLM
- 🧠 Extract structured candidate information
- 👤 Candidate profile generation
- 🎓 Education extraction
- 🛠️ Skills extraction
- 💼 Work experience extraction
- 🚀 Project extraction
- 📝 Project summary extraction
- 📊 Structured candidate visualization
- ✏️ Review and edit extracted information
- 📥 Export candidate information to Excel
- ⚡ Run the AI model remotely using Google Colab
- 🌐 Connect the local Streamlit application to the AI server using ngrok
- 🔐 API authentication between the application and AI backend

---

## 🧠 What Does TalentLens Extract?

The AI engine converts a CV into a structured dictionary containing:

```json
{
    "full_name": "Ahmed Amir Ahmed",
    "email": "ahmed.amir.swe@gmail.com",

    "education": [
        {
            "degree": "Bachelor of Science",
            "institution": "Faculty of Computers and Data Science, Alexandria University",
            "year": "Sep 2023 - Jul 2027"
        }
    ],

    "skills": [
        "Python",
        "Machine Learning",
        "SQL",
        "Pandas"
    ],

    "experience": [
        {
            "role": "Applied AI Trainee",
            "company": "Information Technology Institute (ITI)",
            "years": "July 2026 - Present"
        }
    ],

    "projects": [
        {
            "name": "Bank Account Management System",
            "summary": "A software project for managing bank accounts and related operations."
        }
    ]
}

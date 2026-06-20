Resume Reviewer
This resume reviewer is a local LLM powered tool that compares resumes against job descriptions and returns structured feedback. It uses Llama via Ollama to simulate ATS and recruiter style screening, helping bridge the gap between applicants and automated hiring systems by providing actionable improvement suggestions. 

Challenges Solved
-	Designing reliable prompt structure for consistent LLM output.
-	Normalizing skill extraction across different naming conventions.
-	Structuring AI output for frontend rendering.

Key Features
-	Upload and parse resume file.
-	AI-powered resume analysis using Llama.
-	Job description matching.
-	Structured feedback including strengths, weaknesses and missing skills.
-	Local processing with no external API dependency.
-	Applicant tracking system style keyword evaluation.
-	Improvement suggestions.

Stack
	Frontend
-	React
-	Vite
-	JavaScript
-	CSS
Backend
-	Python
-	File parsing
-	Text processing pipeline for resume analysis
AI
-	Ollama
-	Llama3
-	Prompt engineering evaluation logic

Future Improvements
-	Improve applicant tracking system scoring model.
-	Improve UI dashboard.
-	Add a cover letter generator that tailors content to specific job description using extracted resume information.

1.	Download and Install Ollama
https://ollama.com/download 
Terminal Commands
	ollama pull llama3
	ollama serve
2.	Clone the Project
Terminal Commands
	git clone https://github.com/codingcassandra/ResumeReviewer.git
	cd ResumeReviewer
3.	Set up Backend
Terminal Commands
	cd backend
	pip install -r ../requirements.txt
	uvicorn main:app --reload
Backend runs at http://127.0.0.1:8000
4.	Set up Frontend
Terminal Commands
	cd frontend
	npm install
	npm run dev
Frontend runs at http://localhost:5173

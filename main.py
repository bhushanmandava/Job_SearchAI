import os
import smtplib
import sys
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access them
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_API_URL")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Check for missing environment variables
missing_vars = []

if not TAVILY_API_KEY:
    missing_vars.append("TAVILY_API_KEY")
if not LLM_API_KEY:
    missing_vars.append("LLM_API_KEY")
if not LLM_BASE_URL:
    missing_vars.append("LLM_API_URL")
if not GMAIL_USER:
    missing_vars.append("GMAIL_USER")
if not GMAIL_PASSWORD:
    missing_vars.append("GMAIL_APP_PASSWORD")

if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)  # Stops the code
else:
    print("All required environment variables are set.")

USER_PREFERENCES = {
    "job_title": "machine learning engineer",
    "experience_level": "entry level",
    "location": "united states",
    "skills": ["Python", "TensorFlow", "PyTorch", "scikit-learn", "data analysis"],
    "minimum_match_score": 0.5
}

class JobSearchAI:
    def __init__(self, preferences: Dict[str, Any]):
        self.preferences = preferences
        self.seen_jobs = set()

    def search_jobs(self) -> List[Dict[str, Any]]:
        query = f"{self.preferences['job_title']} {self.preferences['experience_level']} jobs in {self.preferences['location']}"
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                headers={"content-type": "application/json"},
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "advanced",
                    "include_answer": True,
                    "include_domains": ["linkedin.com", "indeed.com", "glassdoor.com", "monster.com", "ziprecruiter.com"]
                }
            )
            if response.status_code == 200:
                results = response.json()
                return self._extract_job_listings(results)
            else:
                print(f"Error searching jobs: {response.status_code}, {response.text[:200]}")
                return []
        except Exception as e:
            print(f"Error during job search: {str(e)}")
            return []

    def _extract_job_listings(self, search_results: Dict) -> List[Dict[str, Any]]:
        job_listings = []
        for result in search_results.get("results", []):
            job = {
                "title": result.get("title", "Unknown Position"),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "source": result.get("url", "").split("/")[2] if "url" in result else "Unknown Source"
            }
            job_id = f"{job['title']}_{job['url']}"
            if job_id in self.seen_jobs:
                continue
            self.seen_jobs.add(job_id)
            job_listings.append(job)
        return job_listings

    def evaluate_job_match(self, job: Dict[str, Any]) -> Dict[str, Any]:
        try:
            print(f"Evaluating job: {job['title'][:50]}...")
            job_description = job["content"]
            skills_list = ", ".join(self.preferences["skills"])

            prompt = f"""
            As an AI assistant helping with job matching, analyze this job description for an entry-level machine learning engineer position:

            JOB DESCRIPTION:
            {job_description}

            CANDIDATE PREFERENCES:
            - Job Title: {self.preferences['job_title']}
            - Experience Level: {self.preferences['experience_level']}
            - Location: {self.preferences['location']}
            - Skills: {skills_list}

            Please analyze:
            1. How well does this job match the desired role and experience level? (Score 0-10)
            2. Which of the candidate's skills are mentioned in the job description?
            3. Are there any key requirements missing from the candidate's skill set?
            4. Is this truly an entry-level position?
            5. Overall match score (0.0-1.0 where 1.0 is perfect match)

            Format your response as a JSON object.
            """

            headers = {
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "agentica-org/deepcoder-14b-preview:free",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }

            response = requests.post(
                LLM_BASE_URL,
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if "choices" not in result or len(result["choices"]) == 0:
                    return self._create_default_analysis(job)
                content = result["choices"][0]["message"]["content"]
                try:
                    analysis = json.loads(content)
                    if "match_score" not in analysis:
                        analysis["match_score"] = 0.5
                    job.update({"analysis": analysis, "match_score": analysis["match_score"]})
                    return job
                except json.JSONDecodeError:
                    return self._create_default_analysis(job)
            else:
                return self._create_default_analysis(job)
        except Exception:
            return self._create_default_analysis(job)

    def _create_default_analysis(self, job: Dict[str, Any]) -> Dict[str, Any]:
        default_analysis = {
            "role_match_score": 5,
            "skills_mentioned": [],
            "missing_skills": [],
            "is_entry_level": True,
            "match_score": 0.5,
            "summary": "LLM parsing failed. Manual review suggested."
        }
        content_lower = job.get("content", "").lower()
        for skill in self.preferences["skills"]:
            if skill.lower() in content_lower:
                default_analysis["skills_mentioned"].append(skill)
        job.update({"analysis": default_analysis, "match_score": default_analysis["match_score"]})
        return job

    def send_alert(self, job: Dict[str, Any]) -> bool:
        try:
            subject = f"Job Alert: {job['title']}"
            body = f"""
            <html>
            <body>
            <h2>New Job Match: {job['title']}</h2>
            <p><strong>Match Score:</strong> {job.get('match_score', 0) * 100:.1f}%</p>
            <p><strong>Source:</strong> {job['source']}</p>
            <p><strong>Link:</strong> <a href="{job['url']}">{job['url']}</a></p>

            <h3>Analysis:</h3>
            <p><strong>Summary:</strong> {job.get('analysis', {}).get('summary', 'No summary available')}</p>

            <h4>Skills Mentioned:</h4>
            <ul>
            {''.join([f'<li>{skill}</li>' for skill in job.get('analysis', {}).get('skills_mentioned', [])])}
            </ul>

            <h4>Missing Skills:</h4>
            <ul>
            {''.join([f'<li>{skill}</li>' for skill in job.get('analysis', {}).get('missing_skills', [])])}
            </ul>

            <hr>
            <p><em>This is an automated alert from your Job Search AI.</em></p>
            </body>
            </html>
            """

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = GMAIL_USER
            msg['To'] = GMAIL_USER

            msg.attach(MIMEText(body, 'html'))
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(GMAIL_USER, GMAIL_PASSWORD)
                server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())

            print(f"Alert sent for job: {job['title']}")
            return True
        except Exception as e:
            print(f"Error sending alert: {str(e)}")
            return False

    def run_search_cycle(self):
        print(f"Starting job search at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        jobs = self.search_jobs()
        if not jobs:
            print("No jobs found in this cycle.")
        for job in jobs:
            evaluated_job = self.evaluate_job_match(job)
            if evaluated_job.get("match_score", 0) >= self.preferences["minimum_match_score"]:
                sent = self.send_alert(evaluated_job)
                if sent:
                    print(f" Email sent for: {job['title']}")
                else:
                    print(f" Failed to send email for: {job['title']}")
            else:
                print(f" Skipped (low match score): {job['title']}")


if __name__ == "__main__":
    job_searcher = JobSearchAI(USER_PREFERENCES)
    while True:
        job_searcher.run_search_cycle()
        time.sleep(3600)  # Wait for 1 hour before next search
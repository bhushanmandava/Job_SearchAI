# README for Job Search AI Project

## Project Overview
The **Job Search AI** is a Python application designed to automate job searches, evaluate job descriptions based on user preferences, and send email alerts for matching job opportunities. It leverages APIs, environment variables, and machine learning models to streamline the job-hunting process.

---

## Features
1. **Automated Job Search**:
   - Searches for jobs using the Tavily API.
   - Filters results based on user-defined preferences such as job title, experience level, location, and skills.

2. **Job Evaluation**:
   - Analyzes job descriptions using an AI language model (LLM).
   - Provides insights into role match, skills mentioned, missing skills, and overall match score.

3. **Email Alerts**:
   - Sends detailed email alerts for jobs that meet the minimum match score.
   - Includes job title, source, link, match score, and analysis summary.

4. **Customizable Preferences**:
   - Users can define their preferences (e.g., job title, skills) in the `USER_PREFERENCES` dictionary.

5. **Environment Variable Integration**:
   - Uses `.env` files to securely manage API keys and email credentials.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)
- `.env` file with required environment variables

### Steps
1. Clone the repository:
   ```bash
   git clone 
   cd 
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory with the following variables:
   ```plaintext
   TAVILY_API_KEY=
   LLM_API_KEY=
   LLM_API_URL=
   GMAIL_USER=
   GMAIL_APP_PASSWORD=
   ```

4. Run the application:
   ```bash
   python main.py
   ```

---

## Configuration

### User Preferences
Modify the `USER_PREFERENCES` dictionary in `main.py` to customize your job search:
```python
USER_PREFERENCES = {
    "job_title": "machine learning engineer",
    "experience_level": "entry level",
    "location": "united states",
    "skills": ["Python", "TensorFlow", "PyTorch", "scikit-learn", "data analysis"],
    "minimum_match_score": 0.5
}
```

### Environment Variables
Ensure all required environment variables are set in your `.env` file. Missing variables will cause the program to terminate.

---

## How It Works

1. **Job Search Cycle**:
    - The program runs a search cycle every hour.
    - It queries the Tavily API for jobs matching user preferences.

2. **Job Evaluation**:
    - Each job description is analyzed using an AI model.
    - The model generates a JSON response with match scores and skill analysis.

3. **Email Alerts**:
    - Jobs meeting the minimum match score are emailed to the user.
    - Alerts include detailed analysis and actionable insights.

---

## Error Handling

### Missing Environment Variables
If any required environment variables are missing, the program will print an error message and terminate:
```plaintext
Error: Missing required environment variables: TAVILY_API_KEY, LLM_API_KEY, ...
```

### API Errors
API errors during job search or evaluation are logged with details for troubleshooting.

### Email Sending Issues
Email alerts that fail to send due to SMTP errors are logged but do not interrupt the search cycle.

---

## Dependencies

- **Python Libraries**:
  - `os`, `sys`, `time`: Core Python modules for system operations.
  - `requests`: For API calls.
  - `dotenv`: For loading environment variables.
  - `smtplib`: For sending emails.
  - `email.mime`: For constructing email messages.
  - `json`: For parsing JSON responses.

- **External APIs**:
  - Tavily API: For job search functionality.
  - LLM API: For evaluating job descriptions.

---

## Future Enhancements

1. Add support for more advanced filtering criteria (e.g., salary range).
2. Integrate additional job platforms beyond Tavily's supported domains.
3. Improve error handling and logging mechanisms.
4. Enhance AI evaluation prompts for better accuracy in match scoring.


> Job Search AI
>
> This document outlines a Python script designed to automate the job
> search process for an entry-level machine learning engineer posi\>on.
> The script leverages external APIs to search for job lis\>ngs,
> evaluates the match between the lis\>ngs and user preferences, and
> sends email alerts for suitable job matches. It u\>lizes environment
> variables for sensi\>ve informa\>on and employs a structured approach
> to ensure eﬃcient job searching and no\>ﬁca\>on.
>
> Script Overview
>
> The script begins by impor\>ng necessary libraries and loading
> environment variables from a
>
> .env ﬁle. It checks for any missing variables and ini\>alizes user
> preferences for the job search. The main class, JobSearchAI,
> encapsulates the func\>onality for searching jobs, evalua\>ng matches,
> and sending alerts.
>
> Environment Variable Setup
>
> load_dotenv()
>
> TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
>
> LLM_API_KEY = os.getenv("LLM_API_KEY") LLM_BASE_URL =
> os.getenv("LLM_API_URL") GMAIL_USER = os.getenv("GMAIL_USER")
>
> GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

||
||
||

> User Preferences
>
> User preferences are deﬁned in a dic\>onary, specifying the job \>tle,
> experience level, loca\>on, skills, and minimum match score.

||
||
||

> Job Search Func\>onality
>
> The search_jobs method constructs a query based on user preferences
> and sends a request to the Tavily API to retrieve job lis\>ngs.

||
||
||

> **Job** **Search** **Process**
>
> Retrieve Start User
>
> Preferences

Construct Query

Send Query to Tavily API

Receive Job

Listings End

> Job Evalua\>on
>
> Each job lis\>ng is evaluated for its match with user preferences
> using the evaluate_job_match method, which interacts with a language
> model API to analyze job descrip\>ons.

||
||
||

> EvaluatingJobMatches
>
> **Languag** **e** **Model** **API**
>
> AI processing for match analysis

**Job** **Descriptio** **n**

<img src="./res245sx.png"
style="width:6.53903in;height:6.53903in" />Details of the job role and
requirements

> **Job** **Match** **Evaluation**
>
> **User** **Preference** **s**
>
> Individual'scareer preferences and criteria
>
> Sending Alerts
>
> When a job matches the user's criteria, an email alert is sent using
> the send_alert method.

||
||
||

> JobAlert System: Structure and Functionality
>
> <img src="./m2ksz2ce.png"
> style="width:0.23063in;height:0.23063in" /><img src="./lctzk01k.png"
> style="width:0.24549in;height:0.24411in" /><img src="./vahk4obi.png"
> style="width:0.23063in;height:0.23063in" /><img src="./hxd35sdu.png"
> style="width:0.24979in;height:0.32508in" /><img src="./pagoik4p.png" style="width:0.26455in" /><img src="./jonsnuhk.png"
> style="width:0.41717in;height:0.41717in" />Job Data User Preferences
>
> JobTitle
>
> Company Name
>
> Job Location

JobAlert System

> Preferred Roles

Salary Expectations

LocationPreferences

> send_alert Method
>
> Email Composition Delivery
>
> Mechanism
>
> Execu\>on Cycle
>
> The script runs in a con\>nuous loop, performing job searches every
> hour.

||
||
||

> Conclusion
>
> This automa\>on script provides a comprehensive solu\>on for job
> seekers in the machine learning ﬁeld, allowing them to eﬃciently ﬁnd
> and evaluate job opportuni\>es based on their preferences. By
> leveraging APIs and email no\>ﬁca\>ons, it streamlines the job search
> process and ensures that users are promptly informed about relevant
> job matches.

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)

# Essential configurations for sessions
app.config["SECRET_KEY"] = "zhrzQXplsrZRaaQpFfPPUv25xlRZq24V"  # Required for sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "null"  # In-memory sessions to avoid filesystem issues
app.config["SESSION_COOKIE_NAME"] = "recruiter_session"  # Explicit cookie name

# Initialize Flask-Session
Session(app)

# Debug logging to verify session setup
@app.before_request
def log_session():
    print(f"Session before request: {session}")

skills_data = [
    {"title": "Data Analysis", "description": "Ability to interpret and analyze data for decision-making.", "ai_exposure": 80, "replacement_rank": 100},
    {"title": "Recruitment Automation", "description": "Using tools to automate candidate sourcing and screening.", "ai_exposure": 80, "replacement_rank": 99},
    {"title": "SEO Skills", "description": "Optimizing content for search engine visibility.", "ai_exposure": 70, "replacement_rank": 98},
    {"title": "Recruitment Analytics", "description": "Analyzing recruitment metrics for strategy improvement.", "ai_exposure": 75, "replacement_rank": 97},
    {"title": "Analytical Thinking", "description": "Problem-solving through logical analysis.", "ai_exposure": 70, "replacement_rank": 96},
    {"title": "Sourcing Strategies", "description": "Techniques to find and attract talent.", "ai_exposure": 70, "replacement_rank": 95},
    {"title": "Talent Assessment", "description": "Evaluating candidate fit and potential.", "ai_exposure": 70, "replacement_rank": 94},
    {"title": "Performance Metrics", "description": "Tracking and measuring employee performance.", "ai_exposure": 70, "replacement_rank": 93},
    {"title": "Reporting Skills", "description": "Creating detailed reports for stakeholders.", "ai_exposure": 70, "replacement_rank": 92},
    {"title": "Job Posting", "description": "Crafting and managing job advertisements.", "ai_exposure": 70, "replacement_rank": 91},
    {"title": "Time Management", "description": "Efficiently organizing and prioritizing tasks.", "ai_exposure": 60, "replacement_rank": 90},
    {"title": "Applicant Tracking", "description": "Managing candidate applications and statuses.", "ai_exposure": 70, "replacement_rank": 89},
    {"title": "Recruitment Marketing", "description": "Promoting job openings to attract candidates.", "ai_exposure": 65, "replacement_rank": 88},
    {"title": "Salary Benchmarking", "description": "Comparing salaries to market standards.", "ai_exposure": 65, "replacement_rank": 87},
    {"title": "Video Interviewing", "description": "Conducting interviews via video platforms.", "ai_exposure": 65, "replacement_rank": 86},
    {"title": "Social Media Savvy", "description": "Leveraging social media for recruitment.", "ai_exposure": 60, "replacement_rank": 85},
    {"title": "Remote Hiring", "description": "Recruiting for remote work positions.", "ai_exposure": 65, "replacement_rank": 84},
    {"title": "Boolean Search", "description": "Using Boolean logic to find candidates.", "ai_exposure": 60, "replacement_rank": 83},
    {"title": "Benchmarking", "description": "Comparing processes to industry standards.", "ai_exposure": 60, "replacement_rank": 82},
    {"title": "Global Talent Sourcing", "description": "Recruiting talent from international markets.", "ai_exposure": 60, "replacement_rank": 81},
    {"title": "Legal Compliance", "description": "Ensuring hiring adheres to laws.", "ai_exposure": 60, "replacement_rank": 80},
    {"title": "Market Research", "description": "Studying market trends for recruitment.", "ai_exposure": 60, "replacement_rank": 79},
    {"title": "Process Improvement", "description": "Enhancing recruitment workflows.", "ai_exposure": 60, "replacement_rank": 78},
    {"title": "Quality of Hire", "description": "Assessing the value of hired candidates.", "ai_exposure": 60, "replacement_rank": 77},
    {"title": "Workforce Planning", "description": "Forecasting staffing needs.", "ai_exposure": 60, "replacement_rank": 76},
    {"title": "Employer Branding", "description": "Building a company's reputation as an employer.", "ai_exposure": 55, "replacement_rank": 75},
    {"title": "Risk Assessment", "description": "Identifying risks in hiring decisions.", "ai_exposure": 55, "replacement_rank": 74},
    {"title": "Talent Mapping", "description": "Mapping skills within the talent pool.", "ai_exposure": 55, "replacement_rank": 73},
    {"title": "Data Privacy", "description": "Ensuring candidate data security.", "ai_exposure": 55, "replacement_rank": 72},
    {"title": "Talent Pooling", "description": "Maintaining a database of potential candidates.", "ai_exposure": 55, "replacement_rank": 71},
    {"title": "Technical Proficiency", "description": "Expertise in technical tools and systems.", "ai_exposure": 50, "replacement_rank": 70},
    {"title": "Employee Productivity", "description": "Measuring and boosting employee output.", "ai_exposure": 55, "replacement_rank": 69},
    {"title": "Employee Surveys", "description": "Gathering feedback from employees.", "ai_exposure": 50, "replacement_rank": 68},
    {"title": "Employee Onboarding", "description": "Integrating new hires into the company.", "ai_exposure": 50, "replacement_rank": 67},
    {"title": "Onboarding Knowledge", "description": "Understanding onboarding best practices.", "ai_exposure": 50, "replacement_rank": 66},
    {"title": "Inclusivity", "description": "Promoting diversity in hiring.", "ai_exposure": 50, "replacement_rank": 65},
    {"title": "Talent Retention", "description": "Strategies to retain employees.", "ai_exposure": 50, "replacement_rank": 64},
    {"title": "Candidate Experience", "description": "Enhancing the candidate journey.", "ai_exposure": 50, "replacement_rank": 63},
    {"title": "Candidate Nurturing", "description": "Building relationships with prospects.", "ai_exposure": 50, "replacement_rank": 62},
    {"title": "Budget Management", "description": "Overseeing recruitment budgets.", "ai_exposure": 50, "replacement_rank": 61},
    {"title": "Employee Scheduling", "description": "Planning employee work hours.", "ai_exposure": 50, "replacement_rank": 60},
    {"title": "Employer Value Proposition", "description": "Defining what makes the company attractive.", "ai_exposure": 45, "replacement_rank": 59},
    {"title": "Customer Service", "description": "Supporting candidates and employees.", "ai_exposure": 45, "replacement_rank": 58},
    {"title": "Learning & Development", "description": "Training and skill development.", "ai_exposure": 45, "replacement_rank": 57},
    {"title": "Employee Retention", "description": "Keeping employees engaged long-term.", "ai_exposure": 45, "replacement_rank": 56},
    {"title": "Decision Making", "description": "Making informed hiring choices.", "ai_exposure": 40, "replacement_rank": 55},
    {"title": "Employee Training", "description": "Providing training programs.", "ai_exposure": 45, "replacement_rank": 54},
    {"title": "Business Acumen", "description": "Understanding business operations.", "ai_exposure": 40, "replacement_rank": 53},
    {"title": "Strategic Planning", "description": "Long-term recruitment planning.", "ai_exposure": 40, "replacement_rank": 52},
    {"title": "Campus Recruiting", "description": "Hiring from universities.", "ai_exposure": 40, "replacement_rank": 51},
    {"title": "Resource Allocation", "description": "Distributing resources effectively.", "ai_exposure": 40, "replacement_rank": 50},
    {"title": "Multitasking", "description": "Handling multiple tasks efficiently.", "ai_exposure": 40, "replacement_rank": 49},
    {"title": "Employee Benefits", "description": "Managing benefit packages.", "ai_exposure": 40, "replacement_rank": 48},
    {"title": "Employee Referrals", "description": "Using referrals for hiring.", "ai_exposure": 35, "replacement_rank": 47},
    {"title": "Talent Development", "description": "Fostering employee growth.", "ai_exposure": 40, "replacement_rank": 46},
    {"title": "Change Management", "description": "Adapting to organizational changes.", "ai_exposure": 35, "replacement_rank": 45},
    {"title": "Employee Accountability", "description": "Ensuring employee responsibility.", "ai_exposure": 35, "replacement_rank": 44},
    {"title": "Feedback Management", "description": "Handling feedback effectively.", "ai_exposure": 30, "replacement_rank": 43},
    {"title": "Training & Development", "description": "Designing training programs.", "ai_exposure": 30, "replacement_rank": 42},
    {"title": "Project Management", "description": "Leading recruitment projects.", "ai_exposure": 35, "replacement_rank": 41},
    {"title": "Employee Reviews", "description": "Conducting performance reviews.", "ai_exposure": 35, "replacement_rank": 40},
    {"title": "Attention to Detail", "description": "Focusing on small task details.", "ai_exposure": 30, "replacement_rank": 39},
    {"title": "Employee Offboarding", "description": "Managing employee exits.", "ai_exposure": 35, "replacement_rank": 38},
    {"title": "Event Management", "description": "Organizing recruitment events.", "ai_exposure": 30, "replacement_rank": 37},
    {"title": "Employee Communication", "description": "Effective internal communication.", "ai_exposure": 30, "replacement_rank": 36},
    {"title": "Vendor Management", "description": "Overseeing third-party vendors.", "ai_exposure": 30, "replacement_rank": 35},
    {"title": "Employee Feedback", "description": "Collecting employee input.", "ai_exposure": 30, "replacement_rank": 34},
    {"title": "Content Creation", "description": "Producing recruitment content.", "ai_exposure": 25, "replacement_rank": 33},
    {"title": "Internal Mobility", "description": "Promoting internal career moves.", "ai_exposure": 30, "replacement_rank": 32},
    {"title": "Sales Skills", "description": "Selling the company to candidates.", "ai_exposure": 25, "replacement_rank": 31},
    {"title": "Employee Engagement", "description": "Boosting employee involvement.", "ai_exposure": 25, "replacement_rank": 30},
    {"title": "Interviewing Skills", "description": "Conducting effective interviews.", "ai_exposure": 25, "replacement_rank": 29},
    {"title": "Employee Recognition", "description": "Acknowledging employee achievements.", "ai_exposure": 25, "replacement_rank": 28},
    {"title": "Storytelling", "description": "Using narratives in recruitment.", "ai_exposure": 25, "replacement_rank": 27},
    {"title": "Employee Wellbeing", "description": "Supporting employee health.", "ai_exposure": 25, "replacement_rank": 26},
    {"title": "Relationship Building", "description": "Creating strong professional ties.", "ai_exposure": 20, "replacement_rank": 25},
    {"title": "Employee Satisfaction", "description": "Ensuring employee happiness.", "ai_exposure": 25, "replacement_rank": 24},
    {"title": "Creativity", "description": "Innovative problem-solving.", "ai_exposure": 20, "replacement_rank": 23},
    {"title": "Employee Enrichment", "description": "Enhancing employee skills.", "ai_exposure": 25, "replacement_rank": 22},
    {"title": "Negotiation Skills", "description": "Negotiating offers with candidates.", "ai_exposure": 30, "replacement_rank": 21},
    {"title": "Presentation Skills", "description": "Delivering compelling presentations.", "ai_exposure": 20, "replacement_rank": 20},
    {"title": "Career Counseling", "description": "Guiding employee career paths.", "ai_exposure": 20, "replacement_rank": 19},
    {"title": "Adaptability", "description": "Adjusting to changing needs.", "ai_exposure": 20, "replacement_rank": 18},
    {"title": "Employee Loyalty", "description": "Fostering long-term commitment.", "ai_exposure": 20, "replacement_rank": 17},
    {"title": "Employee Relations", "description": "Managing employee relationships.", "ai_exposure": 20, "replacement_rank": 16},
    {"title": "Employee Empowerment", "description": "Encouraging employee autonomy.", "ai_exposure": 20, "replacement_rank": 15},
    {"title": "Networking", "description": "Building professional connections.", "ai_exposure": 20, "replacement_rank": 14},
    {"title": "Crisis Management", "description": "Handling recruitment crises.", "ai_exposure": 20, "replacement_rank": 13},
    {"title": "Teamwork", "description": "Collaborating effectively.", "ai_exposure": 15, "replacement_rank": 12},
    {"title": "Employee Autonomy", "description": "Supporting independent work.", "ai_exposure": 15, "replacement_rank": 11},
    {"title": "Emotional Intelligence", "description": "Understanding emotions in interactions.", "ai_exposure": 15, "replacement_rank": 10},
    {"title": "Employee Flexibility", "description": "Adapting to employee needs.", "ai_exposure": 15, "replacement_rank": 9},
    {"title": "Resilience", "description": "Bouncing back from challenges.", "ai_exposure": 10, "replacement_rank": 8},
    {"title": "Employee Collaboration", "description": "Promoting team cooperation.", "ai_exposure": 10, "replacement_rank": 7},
    {"title": "Public Speaking", "description": "Delivering speeches effectively.", "ai_exposure": 10, "replacement_rank": 6},
    {"title": "Employee Innovation", "description": "Encouraging new ideas.", "ai_exposure": 10, "replacement_rank": 5},
    {"title": "Communication Skills", "description": "Clear and effective communication.", "ai_exposure": 20, "replacement_rank": 4},
    {"title": "Conflict Resolution", "description": "Resolving workplace disputes.", "ai_exposure": 10, "replacement_rank": 3},
    {"title": "Cultural Awareness", "description": "Understanding diverse cultures.", "ai_exposure": 10, "replacement_rank": 2},
    {"title": "Active Listening", "description": "Listening to understand, not just respond.", "ai_exposure": 10, "replacement_rank": 1},
]

SKILLS_PER_PAGE = 10

@app.route("/", methods=["GET", "POST"])
def index():
    page = int(request.args.get("page", 1))
    total_pages = (len(skills_data) + SKILLS_PER_PAGE - 1) // SKILLS_PER_PAGE

    if page < 1 or page > total_pages:
        return redirect(url_for("index", page=1))

    start_idx = (page - 1) * SKILLS_PER_PAGE
    end_idx = min(start_idx + SKILLS_PER_PAGE, len(skills_data))
    current_skills = skills_data[start_idx:end_idx]

    if request.method == "POST":
        if "ratings" not in session:
            session["ratings"] = {}
        ratings = {key: int(value) for key, value in request.form.items() if key.startswith("skill_")}
        session["ratings"].update(ratings)

        if page == total_pages:
            results = []
            for skill in skills_data:
                proficiency = int(session["ratings"].get(f"skill_{skill['title'].replace(' ', '_')}", 1))  # Default to 1 if not rated
                risk_score = (skill["replacement_rank"] / 100) * (5 - proficiency)
                results.append({
                    "title": skill["title"],
                    "proficiency": proficiency,
                    "risk_score": round(risk_score, 2),
                    "ai_exposure": skill["ai_exposure"]
                })

            results.sort(key=lambda x: x["risk_score"])
            top_strengths = [r for r in results if r["risk_score"] <= 1][:3]
            top_vulnerabilities = [r for r in results if r["risk_score"] > 2][:3]

            total_risk = sum(r["risk_score"] for r in results)
            max_risk = len(skills_data) * 4
            replaceability_percent = round((total_risk / max_risk) * 100, 1)
            focus_skills = [r["title"] for r in results if r["risk_score"] > 2][:5]

            session.clear()
            return render_template(
                "results.html",
                results=results,
                strengths=top_strengths,
                vulnerabilities=top_vulnerabilities,
                replaceability_percent=replaceability_percent,
                focus_skills=focus_skills
            )
        else:
            return redirect(url_for("index", page=page + 1))

    ratings = session.get("ratings", {})
    for skill in current_skills:
        skill["default_rating"] = ratings.get(f"skill_{skill['title'].replace(' ', '_')}", None)

    return render_template("index.html", skills=current_skills, page=page, total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)

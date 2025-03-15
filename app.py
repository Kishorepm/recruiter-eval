from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # Using filesystem for session storage
app.config["SESSION_COOKIE_NAME"] = "recruiter_session"  # Explicitly set cookie name
app.config["SESSION_FILE_DIR"] = "/tmp/flask_session"  # Directory for session files (writable on Render)
Session(app)

skills_data = [
    {"title": "Data Analysis", "description": "Ability to interpret and analyze data for decision-making.", "ai_exposure": 80, "replacement_rank": 100},
    {"title": "Recruitment Automation", "description": "Using tools to automate candidate sourcing and screening.", "ai_exposure": 80, "replacement_rank": 99},
    # ... (rest of the skills_data as in your original code) ...
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

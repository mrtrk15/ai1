import joblib

model = joblib.load("model.pkl")
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict():
    return render_template("predict.html")

@app.route("/advisor")
def advisor():
    return render_template("advisor.html")

@app.route("/planner")
def planner():
    return render_template("planner.html")

@app.route("/result")
def result():
    return render_template("result.html")


# ------------------ PREDICTION API ------------------

@app.route("/predict_api", methods=["POST"])
def predict_api():

    data = request.get_json()

    # Inputs
    prev_cgpa = data["prev_cgpa"]
    attendance = data["attendance"]
    study_hours = data["study_hours"]
    internal = data["internal"]
    backlogs = data["backlogs"]
    screen_time = data["screen_time"]
    revision = data["revision"]
    problem_solving = data["problem_solving"]

    # ------------------ MAIN PREDICTION ------------------

    features = [[
        prev_cgpa,
        study_hours,
        attendance,
        internal,
        backlogs,
        screen_time,
        revision,
        problem_solving
    ]]

    cgpa = model.predict(features)[0]
    cgpa = max(0, min(10, cgpa))

    # ------------------ CATEGORY ------------------

    if cgpa >= 8:
        category = "Excellent"
    elif cgpa >= 6:
        category = "Good"
    elif cgpa >= 4:
        category = "Average"
    else:
        category = "Poor"

    # ------------------ REASONS ------------------

    reasons = []

    if attendance < 75:
        reasons.append("Low attendance affects performance")

    if study_hours < 10:
        reasons.append("Low study hours")

    if backlogs > 0:
        reasons.append("Backlogs impact CGPA")

    if screen_time > 5:
        reasons.append("High screen time reduces focus")

    if revision < 2:
        reasons.append("Low revision frequency")

    if problem_solving < 2:
        reasons.append("Low problem solving practice")

    if not reasons:
        reasons.append("Balanced academic habits")

    # ------------------ SUGGESTIONS ------------------

    suggestions = []

    if study_hours < 10:
        suggestions.append("Increase study hours")

    if attendance < 75:
        suggestions.append("Improve attendance")

    if screen_time > 5:
        suggestions.append("Reduce screen time")

    if revision < 3:
        suggestions.append("Revise regularly")

    if problem_solving < 3:
        suggestions.append("Practice more problems")

    if backlogs > 0:
        suggestions.append("Clear backlogs early")

    if not suggestions:
        suggestions.append("Maintain current strategy")

    # ------------------ LEARNING MODE SCORING ------------------

    online_score = 0
    offline_score = 0

    if screen_time > 5:
        offline_score += 2
    else:
        online_score += 2

    if study_hours >= 10:
        online_score += 2
    else:
        offline_score += 2

    if revision >= 3 and problem_solving >= 3:
        online_score += 1
    else:
        offline_score += 1

    if online_score > offline_score:
        learning_mode = "Online"
    elif offline_score > online_score:
        learning_mode = "Offline"
    else:
        learning_mode = "Hybrid"

    # ------------------ MODE CGPA COMPARISON ------------------

    online_features = [[
        prev_cgpa, study_hours, attendance, internal,
        backlogs, screen_time, revision, problem_solving
    ]]

    offline_features = [[
        prev_cgpa, study_hours, attendance, internal,
        backlogs, max(0, screen_time - 2),
        revision + 1, problem_solving + 1
    ]]

    online_cgpa = model.predict(online_features)[0]
    offline_cgpa = model.predict(offline_features)[0]

    online_cgpa = max(0, min(10, online_cgpa))
    offline_cgpa = max(0, min(10, offline_cgpa))

    # ------------------ RESPONSE ------------------

    return jsonify({
        "predicted_cgpa": round(cgpa, 2),
        "category": category,
        "reasons": reasons,
        "suggestions": suggestions,
        "learning_mode": learning_mode,
        "online_score": online_score,
        "offline_score": offline_score,
        "online_cgpa": round(online_cgpa, 2),
        "offline_cgpa": round(offline_cgpa, 2)
    })
# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
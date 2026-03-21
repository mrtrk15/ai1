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

    # Extract inputs
    prev_cgpa = data["prev_cgpa"]
    attendance = data["attendance"]
    study_hours = data["study_hours"]
    internal = data["internal"]
    backlogs = data["backlogs"]

    # ------------------ NORMALIZATION ------------------

    attendance_score = attendance / 100        # 0–1
    study_score = study_hours / 24             # assuming max 24 hrs/day
    internal_score = internal / 50             # assuming max 50 marks

    # ------------------ CGPA CALCULATION ------------------

    cgpa = (
        (attendance_score * 3) +
        (study_score * 3) +
        (internal_score * 3) -
        (backlogs * 0.5)
    )

    # Include previous CGPA influence
    cgpa = (cgpa * 0.7) + (prev_cgpa * 0.3)

    # Clamp between 0–10
    cgpa = max(0, min(10, cgpa))

    # ------------------ REASONS ------------------

    if attendance < 75:
        reason1 = "Low attendance is affecting your performance"
    else:
        reason1 = "Good attendance contributing positively"

    if study_hours < 10:
        reason2 = "Insufficient study hours"
    else:
        reason2 = "Consistent study habits"

    # ------------------ SUGGESTIONS ------------------

    if study_hours < 10:
        suggestion1 = "Increase study time to at least 2–3 hours daily"
    else:
        suggestion1 = "Maintain your current study routine"

    if attendance < 75:
        suggestion2 = "Improve attendance to above 75%"
    else:
        suggestion2 = "Keep maintaining good attendance"

    # ------------------ RESPONSE ------------------

    return jsonify({
        "predicted_cgpa": round(cgpa, 2),
        "reason1": reason1,
        "reason2": reason2,
        "suggestion1": suggestion1,
        "suggestion2": suggestion2
    })


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
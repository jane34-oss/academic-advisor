"""Academic Advisor - Flask web app that serves the trained model (model/model.pkl)."""
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "model.pkl"

app = Flask(__name__)
model = joblib.load(MODEL_PATH)

FEATURES = ["cgpa", "study_hours", "attendance", "carryovers"]

ADVICE = {
    "On Track": [
        "Great work - keep your current study routine and attendance.",
        "Aim for consistency: review notes weekly instead of cramming.",
        "Consider mentoring a coursemate or taking on a project to deepen your skills.",
    ],
    "Needs Improvement": [
        "Increase weekly self-study hours and set a fixed timetable.",
        "Attend every class and ask lecturers about topics you find difficult.",
        "Form a study group and practise past questions.",
    ],
    "At Risk": [
        "Meet your course adviser as soon as possible.",
        "Prioritise clearing carryovers and avoid adding extra workload.",
        "Build a strict daily study plan and track your attendance.",
    ],
}


def validate(data):
    """Return (values, error). Values are floats in FEATURES order."""
    try:
        cgpa = float(data["cgpa"])
        hours = float(data["study_hours"])
        attendance = float(data["attendance"])
        carryovers = float(data["carryovers"])
    except (KeyError, TypeError, ValueError):
        return None, "Please fill in all fields with valid numbers."
    if not 0 <= cgpa <= 5:
        return None, "CGPA must be between 0 and 5."
    if not 0 <= hours <= 100:
        return None, "Study hours per week must be between 0 and 100."
    if not 0 <= attendance <= 100:
        return None, "Attendance must be between 0 and 100."
    if not 0 <= carryovers <= 20:
        return None, "Carryovers must be between 0 and 20."
    return [cgpa, hours, attendance, carryovers], None


def predict(values):
    frame = pd.DataFrame([values], columns=FEATURES)
    label = model.predict(frame)[0]
    probs = dict(zip(model.classes_, model.predict_proba(frame)[0]))
    return label, {k: round(float(v) * 100, 1) for k, v in probs.items()}


@app.route("/", methods=["GET", "POST"])
def home():
    context = {"form": {}, "error": None, "result": None}
    if request.method == "POST":
        context["form"] = request.form
        values, error = validate(request.form)
        if error:
            context["error"] = error
        else:
            label, probs = predict(values)
            context["result"] = {"label": label, "advice": ADVICE[label], "probs": probs}
    return render_template("index.html", **context)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """JSON endpoint, e.g. for testing with curl or Postman."""
    values, error = validate(request.get_json(silent=True) or {})
    if error:
        return jsonify({"error": error}), 400
    label, probs = predict(values)
    return jsonify({"status": label, "advice": ADVICE[label], "confidence": probs})


if __name__ == "__main__":
    app.run(debug=True)

"""Run with:  python -m pytest   (or)   python test_app.py"""
from app import app


def test_home_page_loads():
    res = app.test_client().get("/")
    assert res.status_code == 200
    assert b"Academic Advisor" in res.data


def test_strong_student_is_on_track():
    res = app.test_client().post("/api/predict", json={
        "cgpa": 4.6, "study_hours": 30, "attendance": 95, "carryovers": 0})
    assert res.status_code == 200
    assert res.get_json()["status"] == "On Track"


def test_weak_student_is_at_risk():
    res = app.test_client().post("/api/predict", json={
        "cgpa": 1.5, "study_hours": 3, "attendance": 40, "carryovers": 5})
    assert res.get_json()["status"] == "At Risk"


def test_invalid_input_rejected():
    res = app.test_client().post("/api/predict", json={
        "cgpa": 9, "study_hours": 3, "attendance": 40, "carryovers": 5})
    assert res.status_code == 400


def test_form_submission_shows_result():
    res = app.test_client().post("/", data={
        "cgpa": "3.8", "study_hours": "20", "attendance": "85", "carryovers": "0"})
    assert b"Status:" in res.data


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)

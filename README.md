# 🎓 Academic Advisor

A personal academic advisor that combines **software engineering practices** (Git, GitHub, VS Code, tests, a web framework) with an **AI technique** (a Random Forest classifier trained on Google Colab and deployed as a `.pkl` file).

Given a student's **CGPA, weekly study hours, attendance %, and number of carryovers**, it predicts a status — **On Track**, **Needs Improvement**, or **At Risk** — and shows tailored advice.

## Project structure

```
academic-advisor/
├── app.py                         Flask app (loads model/model.pkl)
├── templates/index.html           Web page
├── static/style.css               Styling
├── model/model.pkl                Trained model (pickle file)
├── notebooks/train_advisor_model.ipynb   Colab training notebook (includes the training data)
├── data/training_data.csv         Training data used by the notebook
├── test_app.py                    Automated tests
├── requirements.txt
└── .vscode/                       VS Code settings for Python
```

## Setup in VS Code

1. Extract the zip and open the folder in VS Code (**File → Open Folder**).
2. Install the recommended extensions when prompted (Python, Pylance, Jupyter).
3. Open a terminal (**Ctrl + `**) and run:

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

4. Select the interpreter: **Ctrl+Shift+P → Python: Select Interpreter → venv**.

## Run the web app

```bash
python app.py
```

Open http://127.0.0.1:5000, enter your details and click **Get Advice**.

JSON endpoint (optional):

```bash
curl -X POST http://127.0.0.1:5000/api/predict -H "Content-Type: application/json" \
  -d "{\"cgpa\":3.8,\"study_hours\":20,\"attendance\":85,\"carryovers\":0}"
```

## Run the tests

```bash
python -m pytest
```

## Retrain the model on Google Colab

1. Go to https://colab.research.google.com → **File → Upload notebook** → choose `notebooks/train_advisor_model.ipynb`.
2. **Runtime → Run all**. The last cell downloads `model.pkl`.
3. Replace `model/model.pkl` with the downloaded file and restart the app.

> If you see a scikit-learn version warning when starting the app, retrain in Colab (or run the notebook locally) and replace `model.pkl`.

## Git and GitHub

```bash
git init
git add .
git commit -m "Initial commit: academic advisor"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/academic-advisor.git
git push -u origin main
```

## Note on the data

The training data is **synthetic** (600 generated student records). For a real-world advisor, replace it with real academic records.

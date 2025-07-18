from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "exam_portal_secret_key"

# To support 'enumerate' in templates
app.jinja_env.globals.update(enumerate=enumerate)

PASSWORD = "jaishreeram"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("test"))
        else:
            return render_template("login.html", error="❌ Wrong Password")
    return render_template("login.html")

@app.route("/test", methods=["GET"])
def test():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    filepath = "mcqs/today.json"
    if not os.path.exists(filepath):
        return "❌ File not found: mcqs/today.json"

    with open(filepath, encoding="utf-8") as f:
        questions = json.load(f)

    return render_template("index.html", questions=questions)

@app.route("/submit", methods=["POST"])
def submit():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    with open("mcqs/today.json", encoding="utf-8") as f:
        questions = json.load(f)

    correct = []
    wrong = []
    missed = []

    for i, q in enumerate(questions):
        selected = request.form.getlist(f"q{i}")
        selected = list(map(int, selected)) if selected else []

        correct_answers = q["correct"]

        # ✔️ सही चुनें
        correct_chosen = [opt for opt in selected if opt in correct_answers]
        # ❌ गलत चुनें
        wrong_chosen = [opt for opt in selected if opt not in correct_answers]
        # ⚠️ सही जो नहीं चुने गए
        missed_correct = [opt for opt in correct_answers if opt not in selected]

        correct.append(correct_chosen)
        wrong.append(wrong_chosen)
        missed.append(missed_correct)

    return render_template("result.html", questions=questions, correct=correct, wrong=wrong, missed=missed)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

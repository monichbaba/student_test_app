from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Load questions from JSON
def load_questions():
    with open("mcqs/questions.json", encoding='utf-8') as f:
        return json.load(f)

# Home route – shows Start button
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/password")
    return render_template("index.html")

# Password entry route
@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "POST":
        entered = request.form.get("password")
        if entered == "jaishreeram":
            session["authenticated"] = True
            return redirect("/test")
        else:
            return render_template("password.html", error="Wrong password.")
    return render_template("password.html")

# Main test page
@app.route("/test", methods=["GET", "POST"])
def test():
    if not session.get("authenticated"):
        return redirect("/password")

    questions = load_questions()

    if request.method == "POST":
        score = 0
        results = []
        for idx, question in enumerate(questions):
            selected = request.form.getlist(f"q{idx}")
            correct = set(question["answer"])  # expects 'answer': ["A", "C"]
            selected_set = set(selected)
            is_correct = selected_set == correct
            if is_correct:
                score += 1
            # map keys to text for selected and correct
selected_text = [question["options"][k] for k in selected if k in question["options"]]
correct_text = [question["options"][k] for k in question["answer"] if k in question["options"]]

results.append({
    "question": question["question"],
    "selected": selected_text,
    "correct": correct_text,
    "is_correct": is_correct
})

        return render_template("result.html", results=results, score=score, total=len(questions))

    return render_template("test.html", questions=questions)

# Logout to clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

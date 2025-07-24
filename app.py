from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Load questions from JSON file
def load_questions():
    with open("mcqs/questions.json", encoding='utf-8') as f:
        return json.load(f)

# Home route – Start button
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/password")
    return render_template("index.html")

# Password entry
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

# Test page
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
            correct = set(question["answer"])
            selected_set = set(selected)
            is_correct = selected_set == correct

            # Get option texts
            selected_text = [question["options"].get(k, "") for k in selected]
            correct_text = [question["options"].get(k, "") for k in question["answer"]]

            results.append({
                "question": question["question"],
                "selected": selected_text,
                "correct": correct_text,
                "is_correct": is_correct
            })

            if is_correct:
                score += 1

        return render_template("result.html", results=results, score=score, total=len(questions))

    return render_template("test.html", questions=questions)

# Logout and clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

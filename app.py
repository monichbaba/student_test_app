from flask import Flask, render_template, request
import json, os

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)

PASSWORD = "1234"  # Change if needed

@app.route('/', methods=['GET', 'POST'])
def test():
    filepath = 'mcqs/questions.json'
    if not os.path.exists(filepath):
        return "❌ File mcqs/questions.json not found"

    with open(filepath, encoding="utf-8") as f:
        questions = json.load(f)

    if request.method == 'POST':
        password = request.form.get('password')
        if password != PASSWORD:
            return render_template('test.html', questions=[], error="❌ Wrong Password")

        user_answers = []
        score = 0

        for idx, q in enumerate(questions):
            selected = request.form.getlist(str(idx))
            user_answers.append(selected)
            if set(selected) == set(q["answer"]):
                score += 1

        return render_template('test.html', questions=questions, score=score,
                               user_answers=user_answers, submitted=True)

    return render_template('test.html', questions=[])

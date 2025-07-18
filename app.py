from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)

PASSWORD = "jaihind"

@app.route('/', methods=['GET', 'POST'])
def password_check():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == PASSWORD:
            return redirect(url_for('test'))
        else:
            return render_template('password.html', error="❌ Incorrect Password")
    return render_template('password.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    filepath = 'mcqs/questions.json'
    if not os.path.exists(filepath):
        return "❌ File mcqs/questions.json not found"

    with open(filepath, encoding="utf-8") as f:
        questions = json.load(f)

    result = []
    score = 0
    submitted = False

    if request.method == 'POST':
        submitted = True
        for i, q in enumerate(questions):
            selected = request.form.getlist(f'q{i}')
            correct = q['answer']
            is_correct = set(selected) == set(correct)
            score += int(is_correct)
            result.append({
                'question': q['question'],
                'options': q['options'],
                'selected': selected,
                'correct': correct,
                'is_correct': is_correct
            })

    return render_template('test.html', questions=questions, result=result, submitted=submitted, score=score)

if __name__ == '__main__':
    app.run(debug=True)

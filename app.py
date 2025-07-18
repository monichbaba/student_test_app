from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'any-secret-key-you-like'
app.jinja_env.globals.update(enumerate=enumerate)

# Load questions once
with open('mcqs/questions.json'
", encoding="utf-8") as f:
    questions = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == '1234':
            session['authenticated'] = True
            return redirect('/test')
        else:
            error = '❌ Incorrect password'
    return render_template('login.html', error=error)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if not session.get('authenticated'):
        return redirect('/')

    if request.method == 'POST':
        results = []
        score = 0

        for i, q in enumerate(questions):
            selected = request.form.getlist(f'q{i}')
            selected = list(map(int, selected)) if selected else []

            correct = q['answer']
            is_correct = sorted(selected) == sorted(correct)
            if is_correct:
                score += 1

            results.append({
                'question': q['question'],
                'options': q['options'],
                'selected': selected,
                'correct': correct
            })

        return render_template('result.html', results=results, score=score, total=len(questions))

    return render_template('test.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)

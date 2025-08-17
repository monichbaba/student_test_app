from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key_here'

with open('mcqs/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'jaikanhiyalal':
            session['authenticated'] = True
            return redirect(url_for('test'))
        else:
            error = 'Incorrect password. Try again.'
    return render_template('index.html', error=error)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template('test.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    if not session.get('authenticated'):
        return redirect(url_for('index'))

    score = 0
    results = []
    for q in questions:
        qid = str(q['id'])
        selected = request.form.getlist(qid)
        correct = q['answer']
        is_correct = set(selected) == set(correct)
        if is_correct:
            score += 1
        results.append({
            'question': q['question'],
            'options': q['options'],
            'selected': selected,
            'correct': correct,
            'is_correct': is_correct,
            'explanation': q.get('explanation', '')  # ✅ Added explanation
        })

    return render_template('result.html', results=results, score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)

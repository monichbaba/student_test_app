from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate, chr=chr)

PASSWORD = "1234"  # ✅ Change if needed

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            return redirect('/test')
        else:
            return render_template('login.html', error="❌ गलत पासवर्ड")
    return render_template('login.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    filepath = 'mcqs/questions.json'

    if not os.path.exists(filepath):
        return "❌ File not found: mcqs/questions.json"

    with open(filepath, encoding='utf-8') as f:
        questions = json.load(f)

    if request.method == 'POST':
        user_answers = request.form
        results = []

        for q in questions:
            qid = str(q['id'])
            selected = user_answers.getlist(qid)
            correct = q['answer']
            is_correct = set(selected) == set(correct)

            results.append({
                'question': q['question'],
                'options': q['options'],
                'selected': selected,
                'correct': correct,
                'is_correct': is_correct
            })

        return render_template('result.html', results=results)

    return render_template('test.html', questions=questions)
if __name__ == '__main__':
    app.run(debug=True)


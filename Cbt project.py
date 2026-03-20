# ===================== 123456789101112
# FILE: app.py
# =====================
from flask import Flask, render_template, request, redirect, url_for, session
from models import Question, Result, QuestionQueue 

app = Flask(__name__)
app.secret_key = "secret123"  # needed for session

# Initialize Queue
queue = QuestionQueue()

# Add questions to queue
queue.enqueue(Question("2 + 2 = ?", ["2", "4", "6"], "4"))
queue.enqueue(Question("Capital of Nigeria?", ["Abuja", "Lagos", "Kano"], "Abuja"))
queue.enqueue(Question("5 * 3 = ?", ["15", "10", "20"], "15"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = queue.get_all()N

    if request.method == "POST":
        score = 0
        for i, q in enumerate(questions):
            if request.form.get(str(i)) == q.answer:
                score += 1

        percentage = (score / len(questions)) * 100
        result = Result(score, percentage)
        session['result'] = result.display()
        return redirect(url_for('result'))

    return render_template("quiz.html", questions=questions)

@app.route("/result")
def result():
    result = session.get('result', None)
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)


# =====================
# FILE: models.py
# =====================
from datetime import datetime

class Question:
    def __init__(self, text, options, answer):
        self.text = text
        self.options = options
        self.answer = answer

class Result:
    def __init__(self, score, percentage):
        self.score = score
        self.percentage = percentage
        self.timestamp = datetime.now()

    def display(self):
        return f"Score: {self.score} | {self.percentage:.2f}% | Time: {self.timestamp}"

# Queue Implementation (FIFO)
class QuestionQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)

    def get_all(self):
        return self.queue


# =====================
# FILE: templates/index.html
# =====================
"""
<!DOCTYPE html>
<html>
<head>
    <title>CBT App</title>
    <style>
        body { font-family: Arial; text-align: center; background: #111; color: white; }
        a { padding: 15px 25px; background: gold; color: black; text-decoration: none; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>🔥 CBT EXAM SYSTEM</h1>
    <p>Test your knowledge</p>
    <a href="/quiz">Start Test</a>
</body>
</html>
"""


# =====================
# FILE: templates/quiz.html
# =====================
"""
<!DOCTYPE html>
<html>
<head>
    <title>Quiz</title>
    <style>
        body { font-family: Arial; background: #222; color: white; }
        .container { width: 60%; margin: auto; }
        button { padding: 10px; background: gold; border: none; }
    </style>

    <script>
        let timeLeft = 30;
        function startTimer() {
            let timer = setInterval(function() {
                document.getElementById("timer").innerHTML = timeLeft + " seconds";
                timeLeft--;
                if (timeLeft < 0) {
                    clearInterval(timer);
                    document.getElementById("quizForm").submit();
                }
            }, 1000);
        }
    </script>
</head>
<body onload="startTimer()">
    <div class="container">
        <h2>Answer Questions</h2>
        <p>Time left: <span id="timer"></span></p>

        <form method="POST" id="quizForm">
            {% for q in questions %}
                <p>{{ q.text }}</p>
                {% for opt in q.options %}
                    <input type="radio" name="{{ loop.index0 }}" value="{{ opt }}"> {{ opt }}<br>
                {% endfor %}
            {% endfor %}
            <br>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
"""


# =====================
# FILE: templates/result.html
# =====================
"""
<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
    <style>
        body { text-align: center; font-family: Arial; background: black; color: white; }
        a { padding: 10px; background: gold; color: black; text-decoration: none; }
    </style>
</head>
<body>
    <h1>🎉 Result</h1>
    <h2>{{ result }}</h2>
    <a href="/quiz">Retake Test</a>
</body>
</html>
"""


# =====================
# FILE: README.md
# =====================
"""
# CBT Flask Web App

## Description
This is a Computer-Based Test (CBT) web application built using Flask.
Users can take a timed quiz, get their score, percentage, and timestamp.

## Features
- Object-Oriented Programming (Classes)
- Queue Data Structure (FIFO)
- Timer functionality
- Score & Percentage system
- Timestamp using datetime
- Flask Web Interface

## How to Run
1. Install Flask:
   pip install flask

2. Run the app:
   python app.py

3. Open browser:
   http://127.0.0.1:5000/

## GitHub Steps
1. git init
2. git add .
3. git commit -m "initial commit"
4. git branch -M main
5. git remote add origin YOUR_REPO_LINK
6. git push -u origin main

## Author
MAAUN/24/DTS/0007 Rayhaan Abubakar
"""

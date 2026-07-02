from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = 'rahul_secret_key_2026'

# Simple user storage (no database needed for now)
users = {}

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def get_grade(score):
    if score >= 90: return 'A+', '🏆'
    elif score >= 80: return 'A', '🌟'
    elif score >= 70: return 'B', '👍'
    elif score >= 60: return 'C', '📚'
    elif score >= 50: return 'D', '⚠️'
    else: return 'F', '❌'

def get_study_tips(score):
    if score >= 90:
        return [
            "You're doing amazing! Keep the momentum!",
            "Try teaching others — it deepens your knowledge",
            "Challenge yourself with harder practice problems"
        ]
    elif score >= 70:
        return [
            "Great progress! Focus on your weak topics",
            "Review your notes 30 minutes before sleep",
            "Try solving past exam papers for practice"
        ]
    elif score >= 50:
        return [
            "Increase your study hours gradually",
            "Break study sessions into 25-minute chunks",
            "Remove all distractions while studying"
        ]
    else:
        return [
            "Start with basics — build a strong foundation",
            "Study with a friend or join a study group",
            "Ask your teacher for extra help — it's worth it!"
        ]

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password!"
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = "Username already exists!"
        else:
            users[username] = password
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('register.html', error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    prediction = None
    grade = None
    emoji = None
    tips = None
    hours = None

    if request.method == 'POST':
        hours = float(request.form['hours'])
        pred = model.predict(np.array([[hours]]))[0]
        prediction = round(min(pred, 100), 1)
        grade, emoji = get_grade(prediction)
        tips = get_study_tips(prediction)

    return render_template('dashboard.html',
                         username=session['username'],
                         prediction=prediction,
                         grade=grade,
                         emoji=emoji,
                         tips=tips,
                         hours=hours)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
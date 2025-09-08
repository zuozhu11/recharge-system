from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/reg_log', methods=['POST'])
def reg_log():
    id = request.form.get('id')
    password = request.form.get('password')
    with sqlite3.connect('user2.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO account (id, password, money) VALUES (?, ?, ?)', (id, password, 0))
    return render_template('login.html')

@app.route('/face', methods=['POST'])
def face():
    id = request.form.get('id')
    password = request.form.get('password')

    with sqlite3.connect('user2.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT password FROM account WHERE id = (?)', (id,))
        Password = cur.fetchone()
        if Password == None:
            return render_template('login.html', message="the id isn't correct")
        if Password[0] == password:
            session['id'] = id
            return render_template('main.html')
        else:
            return render_template('login.html', message="the password isn't correct")
        
@app.route('/quest')
def quest():
    id = session.get('id')
    with sqlite3.connect('user2.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT money FROM account WHERE id = (?)', (id,))
        money1 = cur.fetchone()
        money = money1[0]
        return render_template('quest.html', money=money)

@app.route('/main', methods=["GET", "POST"])
def main():
    id = session.get('id')
    if not id:
        return redirect(url_for('login'))
    balance = None
    input = None
    if request.method == "POST":
        input = request.form.get('input')
        with sqlite3.connect('user2.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT money FROM account WHERE id = (?)', (id,))
            money1 = cur.fetchone()
            money = money1[0]
            input = int(input)
            balance = money + input
            cur.execute('UPDATE account SET money = ? WHERE id = ?', (balance, id))
    else:
        with sqlite3.connect('user2.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT money FROM account WHERE id = (?)', (id,))
            money1 = cur.fetchone()
            balance = money1[0]
    return render_template('main.html', balance=balance, recharge_amount=input)
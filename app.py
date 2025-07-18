#_____________________BEGIN_____________________#

from flask import *
import os
import random as r
from datetime import datetime

app = Flask(__name__)
ran = r.randint(5,50) * r.randint(20,50)
app.secret_key = os.urandom(ran)

###########Define variable#####
user = {}
messages = []

###__________HOME_____________###
@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for("chat"))
    return redirect(url_for("login"))

###__________LOGIN_____________###
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_name = request.form['username']
        if user_name:
            session['username'] = user_name
            if user_name not in user:
                user[user_name] = {"Joined": datetime.now()}
            return redirect(url_for("chat"))
    return render_template("login.html")


###________LOGOUT_____________###
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



###__________CHAT_____________###
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if "username" not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        message = request.form['text_message']
        if message:
            messages.append({
            "id": len(message),
            "username": session['username'],
            "text": message,
            "time": datetime.now().strftime('%H:%M'),
            "date": datetime.now().strftime('%Y-%m-%d')
            })
        return redirect(url_for('chat'))
    return render_template('chat.html', user_name=session['username'], messages=messages)
            

###_________DELETE_____________###
@app.route('/delete/<int:message_id>')
def delete(message_id):
     if  "username" not in session:
         return redirect(url_for('login'))
     for i, msg in enumerate(messages):
         if msg['id'] == message_id and msg['username'] == session['username']:
             messages.pop(i)
             break
     return redirect(url_for('chat'))
#____________________END______________________#
if __name__ == "__main__":
    app.run(debug=True)

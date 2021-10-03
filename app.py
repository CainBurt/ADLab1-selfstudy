from flask import Flask, render_template, request, session, redirect, url_for, g
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = 'secretkey'

#access user data if they are logged in
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [i for i in users if i.id == session['user_id']][0]
        g.user = user

#create a user object and store some in a list
class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users=[]
users.append(User(id=1, username='Cain', password='password'))
users.append(User(id=2, username='John', password='password1'))

#log users in, refreshes page if details are incorrect
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session.pop('user.id', None)
        username = request.form['username']
        password = request.form['password']

        user = [i for i in users if i.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/profile")
def profile():

    if not g.user:
        return redirect(url_for('login'))
        
    return render_template('profile.html')

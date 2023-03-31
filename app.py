from flask import Flask, render_template, request, redirect, url_for, session
from pyrebase import pyrebase
from dotenv import load_dotenv
import os
import ast

load_dotenv()

config = ast.literal_eval(os.environ['config'])
firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if ('user' in session):
        return redirect(url_for('home'))
    
    if request.method== 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print('Logged in')
            session['user'] = email
            print(session['user'])
        except:
            if email == '':
                error = 'Email is required'
                print('Email is required')
            elif password == '':
                error = 'Password is required'
                print('Password is required')
            else:
                error = 'Invalid Email or Password'
                print('Invalid email or password')
                

            return render_template('login.html', 
                                   email=email,
                                   password=password,
                                   error=error)

        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if ('user' in session):
        return redirect(url_for('home'))
    
    if request.method== 'POST':
        error = ''
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            print('User Successfully Created')
        
        except:
            if email == '':
                error = 'Email is required'
                print('Email is required')
            elif password == '':
                error = 'Password is required'
                print('Password is required')
            else:
                error = 'Email already in use'
                print('Email already in use')

            return render_template('signup.html', 
                                   email=email,
                                   password=password,
                                   error=error)

        return redirect(url_for('home'))
    
    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host ="localhost", port = int("5000"))    
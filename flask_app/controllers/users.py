from flask import Flask, render_template, request, redirect,session
from flask_app import app
from flask_app.models.car import Car
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask import flash

#landing page
@app.route('/')
def index():
    return render_template('index.html')


#register
@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {**request.form, 'password': bcrypt.generate_password_hash(request.form['password'])} 
    query_output = User.create(data)
    print(query_output, '*'*30)
    session['user_id'] = query_output #store then put it inside the session
    return redirect('/dashboard')

#the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    } 
    return render_template('dashboard.html', user=User.get_by_id(data), cars=Car.get_all_cars())


#login
@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email", "error2") #check if email exists
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']): #check the password
        flash("Invalid password", "error2")
        return redirect('/')
    session['user_id'] = user.id #if everything is ok use session to keep track with the user.id
    return redirect('/dashboard')


#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
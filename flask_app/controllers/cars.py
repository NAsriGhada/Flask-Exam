from turtle import update
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.car import Car
from flask_app.models import user


#car landing page
@app.route('/new')
def new_car():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_car.html',user=user.User.get_by_id(data))


#create car
@app.route('/create/car',methods=['POST'])
def create_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/new')
    data = {
        "price": int(request.form["price"]),
        "model": request.form["model"],
        "make": request.form["make"],
        "year": int(request.form["year"]),
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Car.create_car(data)
    return redirect('/dashboard')


#show car
@app.route('/show/<int:id>')
def show_car(id):
    if 'user_id' not in session:
        return redirect('/')
    car_data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template('show.html', cars = Car.get_one_car(car_data), users=user.User.get_by_id(user_data))

#delete car
@app.route('/car/delete/<int:id>')
def delete_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Car.delete(data)
    return redirect('/dashboard')


#show car to edit
@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html", edit=Car.get_one_car(data), user=user.User.get_by_id(user_data))

#updating car
@app.route('/update/car',methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/new')
    updated_data = {**request.form}
    Car.update(updated_data)
    return redirect('/dashboard')



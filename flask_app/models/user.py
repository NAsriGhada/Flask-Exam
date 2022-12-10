from flask_app.config.mysqlconnection import connectToMySQL
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.car import Car

class User:
    db_name = "belt_exam"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cars = []

            #CRUD
        #CREATE
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)
        #READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    

    @classmethod
    def users_have_cars(cls,data):
        query = "INSERT INTO users_has_cars (user_id,car_id) VALUES (%(author_id)s,%(book_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_user_with_cars( cls , data ):
        query = "SELECT * FROM users LEFT JOIN users_has_cars ON users.id = users_has_cars.user_id LEFT JOIN cars ON cars.id = users_has_cars.car_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        user = cls( results[0] )
        for row_from_db in results:
            # Now we parse the burger data to make instances of burgers and add them into our list.
            car_data = {
                "id" : row_from_db["cars.id"],
                "price" : row_from_db["price"],
                "model" : row_from_db["model"],
                "make" : row_from_db["make"],
                "year" : row_from_db["year"],
                "created_at" : row_from_db["burgers..created_at"],
                "updated_at" : row_from_db["burgers.updated_at"]
                
            }
            user.cars.append( Car( car_data ) )
        return user

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","error")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","error")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","error")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","error")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","error")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","error")
        return is_valid
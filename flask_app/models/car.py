from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    db_name = "belt_exam"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owners_with_cars = []



      #CRUD
        #CREATE CAR
    @classmethod
    def create_car(cls,data):
        query = "INSERT INTO cars (user_id, price, model, make, year, description) VALUES (%(user_id)s, %(price)s, %(model)s, %(make)s, %(year)s, %(description)s)"
        print(query)
        return connectToMySQL(cls.db_name).query_db(query, data)

        #READ CAR
    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM cars;"
        results = connectToMySQL(cls.db_name).query_db(query)
        car = []
        for row in results:
            car.append(cls(row))
        return car

    @classmethod
    def get_one_car(cls,data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )


        #UPDATE CAR
    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

        #DELETE CAR
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    def get_by_id(cls,data):
        query = "SELECT * FROM cars LEFT JOIN users_has_cars ON cars.id = users_has_cars.car_id LEFT JOIN users ON users.id = users_has_cars.author_id WHERE cars.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)

        car = cls(results[0])

        for row in results:
            if row['cars.id'] == None:
                break
            data = {
                "id": row['authors.id'],
                "name": row['name'],
                "created_at": row['authors.created_at'],
                "updated_at": row['authors.updated_at']
            }
            car.owners_with_cars.append(user.User(data))
        return car

    @staticmethod
    def validate_car(car):
        is_valid = True
        if int(car['price']) <= 0:
            is_valid = False
            flash("price must be greater than 0","car_error")
        if len(car['model']) == "":
            is_valid = False
            flash("field must not be empty","car_error")
        if len(car['make']) == "":
            is_valid = False
            flash("field must not be empty","car_error")
        if int(car['year']) <= 0:
            is_valid = False
            flash("year must be greater than 0","car_error")
        if car['description'] == "":
            is_valid = False
            flash("field must not be empty","car_error")
        return is_valid
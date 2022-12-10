from flask_app import app
#import controllers here, don't FORGET
from flask_app.controllers import users
from flask_app.controllers import cars









if __name__ == '__main__':
    app.run(debug=True, port=5001)
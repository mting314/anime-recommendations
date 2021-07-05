import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    
    load_dotenv()
    app = Flask(__name__)

    CORS(app)
    ENV = 'prod'

    LOCAL_DB_URL = os.getenv("LOCAL_DB_URL")
    REMOTE_DB_URL = os.getenv("REMOTE_DB_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Setting database configs
    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB_URL
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = REMOTE_DB_URL


    print(app.config['SQLALCHEMY_DATABASE_URI'])

    app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    create_app().run(threaded=True,debug=True, port=int(os.environ.get("PORT"), 5000))
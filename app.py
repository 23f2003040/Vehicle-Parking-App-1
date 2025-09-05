from flask import Flask,render_template
from backend.models import*
import os

app=None

def init_app():
    my_app=Flask(__name__)
    my_app.debug=True
    my_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///my_app.sqlite3"
    my_app.app_context().push()
    db.init_app(my_app)
    print("my_app started...")
    return my_app

app=init_app()
from backend.controllers import *

if __name__=="__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

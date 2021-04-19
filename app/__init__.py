from flask import Flask
from app.database import Database
from flask_login import LoginManager

db = Database("sd")


app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)



login_manager = LoginManager()
login_manager.init_app(app)




from app.controllers import default


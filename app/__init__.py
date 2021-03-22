from flask import Flask
from app.database import Database

db = Database("sd")


app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

from app.controllers import default


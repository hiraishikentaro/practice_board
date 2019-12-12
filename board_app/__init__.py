from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('board_app.config')

db = SQLAlchemy(app)

import board_app.views

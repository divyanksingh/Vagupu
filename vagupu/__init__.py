from flask import Flask

SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
from vagupu import views

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dell/vagupu/test'

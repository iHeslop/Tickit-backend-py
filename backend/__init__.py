from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from backend import db_config 
from backend import routes
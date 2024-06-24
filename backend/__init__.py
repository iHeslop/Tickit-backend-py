from flask import Flask

app = Flask(__name__)

from backend import db_config 
from backend import routes
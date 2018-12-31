from flask import Flask
import os

app = Flask(__name__)

from app import routes, models
# import app

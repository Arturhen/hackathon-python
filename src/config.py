from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
from pathlib import Path
import os

 
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
 
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URI = os.getenv("DATABASE_URI")
DEV_DATABASE_URI = os.getenv("DEV_DATABASE_URI")


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DATABASE_URI
CORS(app)

db = SQLAlchemy(app)

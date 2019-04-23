#!/usr/bin/env python3
##
## EPITECH PROJECT, 2019
## EpyTodo
## File description:
## Init
##

from flask import Flask
from flask import session
from app.models import *
import os

app = Flask(__name__)
app.config.from_object('config')
if app.config['DEBUG_MODE'] == True:
    os.environ['FLASK_ENV'] = "development"
else:
    os.environ['FLASK_ENV'] = "production"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
con = ConnectionManager(app)
app.conn = con.getconnection()
from app import views

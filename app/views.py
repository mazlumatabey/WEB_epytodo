#!/usr/bin/env python3
##
## EPITECH PROJECT, 2019
## EpyTodo
## File description:
## Views
##

from flask import *
import pymysql as sql
from app import *
from app.controller import my_user

@app.route('/' , methods = ['GET'])
def root():
    if 'username' in session:
        return render_template("my_user.html", title="Dashboard")
    else:
        return render_template("my_login.html", title="Login")
@app.route('/my_register', methods = ['GET'])
def my_register():
    if 'username' in session:
        return render_template("my_user.html", title="Dashboard")
    else:
        return render_template("my_register.html", title="Register")
@app.route('/my_user', methods = ['GET'])
def my_user_dash():
    return render_template("my_user.html", title="Dashboard", user=session['username'])
@app.route('/my_user/my_get_tasks', methods = ['GET'])
def my_get_tasks():
    controller = my_user(app, app.conn)
    return controller.list_all_taks_easy()
@app.route('/register' , methods = ['POST'])
def register():
    controller = my_user(app, app.conn)
    return controller.create_my_user(request)
@app.route('/signin' , methods = ['POST'])
def signin():
    controller = my_user(app, app.conn)
    return controller.connect(request)
@app.route('/signout' , methods = ['POST'])
def signout():
    controller = my_user(app, app.conn)
    return controller.signout()
@app.route('/user' , methods = ['GET'])
def user():
    controller = my_user(app, app.conn)
    return controller.user()
@app.route('/user/task' , methods = ['GET'])
def user_task():
    controller = my_user(app, app.conn)
    return controller.show_all_task()
@app.route('/user/task/<id>' , methods = ['POST', 'GET'])
def user_task_id(id):
    if request.method == 'POST':
        controller = my_user(app, app.conn)
        return controller.update_task_id(request, id)
    elif request.method == 'GET':
        controller = my_user(app, app.conn)
        return controller.show_task_by_id(id)
@app.route('/user/task/add' , methods = ['POST'])
def user_task_add():
    controller = my_user(app, app.conn)
    return controller.user_task_add(request)
@app.route('/user/task/del/<id>' , methods = ['POST'])
def user_task_del_id(id):
    controller = my_user(app, app.conn)
    return controller.user_task_del_id(id)

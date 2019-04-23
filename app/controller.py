#!/usr/bin/env python3
##
## EPITECH PROJECT, 2019
## EpyTodo
## File description:
## Controller
##

from flask import *
from app.views import *
from app.models import *
import pymysql as sql
import hashlib

REGISTER_RES = "account created"
REGISTER_ERR_ALREAY_EXISTS = "account already exists"
REGISTER_ERR_INTERNAL_ERROR = "internal error"
SIGNIN_ERR_NOT_MATCH = "login or password does not match"
SIGNIN_ERR_INTERNAL_ERROR = "internal error"
SIGNIN_RES = "signin successful"
SIGNOUT_RES = "signout successful"
TASK_ID_ADD_RES = "new task added"
TASK_ID_DEL_RES = "task deleted"
TASK_ID_KO_RES = "task id does not exist"
NOT_CONNECTED = "you must be logged in"
CONNECTED = "you must be logged off"
INTERNAL_ERROR = "internal error"

class my_user(object):
    def __init__(self, app, sqlcon):
        self.app = app
        self.sqlcon = sqlcon

    def create_my_user(self, request):
        api = {}
        models = SQLManagement(app)
        user = request.form['username']
        password = request.form['password']
        if 'username' not in session:
            if user and password:
                result = models.check_user_exists_username(user)
                if result == False:
                    password_hased = hashlib.md5(password.encode('utf-8')).hexdigest()
                    models._create_user(user, password_hased)
                else:
                    api['error'] = REGISTER_ERR_ALREAY_EXISTS
                    response = jsonify(api)
                    response.status_code = 201
                    return response
            else:
                api['error'] = REGISTER_ERR_INTERNAL_ERROR
                response = jsonify(api)
                response.status_code = 202
                return response
        else:
            api['error'] = CONNECTED
            response = jsonify(api)
            response.status_code = 203
            return response
        api['result'] = REGISTER_RES
        session['username'] = user
        response = jsonify(api)
        response.status_code = 200
        return response

    def connect(self, request):
        api = {}
        models = SQLManagement(app)
        user = request.form['username']
        password = request.form['password']
        if 'username' not in session:
            if user and password:
                    password_hased = hashlib.md5(password.encode('utf-8')).hexdigest()
                    if models.connect(user, password_hased) == False:
                        api['error'] = SIGNIN_ERR_NOT_MATCH
                        response = jsonify(api)
                        response.status_code = 201
                        return response
            else:
                api['error'] = REGISTER_ERR_INTERNAL_ERROR
                response = jsonify(api)
                response.status_code = 202
                return response
        else:
            api['error'] = CONNECTED
            response = jsonify(api)
            response.status_code = 203
            return response
        api['result'] = SIGNIN_RES
        session['username'] = user
        response = jsonify(api)
        response.status_code = 200
        return response
    def signout(self):
        api = {}
        if 'username' in session:
            session.clear()
            api['result'] = SIGNOUT_RES
            response = jsonify(api)
            response.status_code = 200
            return response
        else:
            api['error'] = NOT_CONNECTED
            response = jsonify(api)
            response.status_code = 201
            return response
        api['error'] = INTERNAL_ERROR
        response = jsonify(api)
        response.status_code = 201
        return response
    def user(self):
        api = {}
        models = SQLManagement(app)
        if 'username' in session:
            api = {"result":[{"username": session['username'], "id": models.get_id(session['username'])}]}
            response = jsonify(api)
            response.status_code = 200
            return response
        else:
            api['error'] = NOT_CONNECTED
            response = jsonify(api)
            response.status_code = 201
            return response
        api['error'] = INTERNAL_ERROR
        response = jsonify(api)
        response.status_code = 202
        return response
    def user_task_add(self, request):
        api = {}
        models = SQLManagement(app)
        title = request.form['title']
        date_begin = request.form['begin']
        date_end = request.form['end']
        status = request.form['status']
        if 'username' in session:
            if title and status:
                username = session['username']
                id = models.get_id(username)
                if models.add_user_task(id, title, status, date_begin, date_end) == False:
                    api['error'] = SIGNIN_ERR_NOT_MATCH
                    response = jsonify(api)
                    response.status_code = 201
                    return response
            else:
                api['error'] = REGISTER_ERR_INTERNAL_ERROR
                response = jsonify(api)
                response.status_code = 202
                return response
        else:
            api['error'] = NOT_CONNECTED
            response = jsonify(api)
            response.status_code = 203
            return response
        api['result'] = TASK_ID_ADD_RES
        response = jsonify(api)
        response.status_code = 200
        return response
    def user_task_del_id(self, id):
        api = {}
        models = SQLManagement(app)
        if 'username' in session:
            if id.isdigit():
                username = session['username']
                id_username = models.get_id(username)
                if models.get_task_id(id_username, id) == False:
                    api['error'] = TASK_ID_KO_RES
                    response = jsonify(api)
                    response.status_code = 201
                    return response
            else:
                api['error'] = INTERNAL_ERROR
                response = jsonify(api)
                response.status_code = 202
                return response
        else:
            api['error'] = NOT_CONNECTED
            response = jsonify(api)
            response.status_code = 203
            return response
        models.del_task(id)
        api['result'] = TASK_ID_DEL_RES
        response = jsonify(api)
        response.status_code = 200
        return response
    def show_task_by_id(self, id):
        api = {}
        models = SQLManagement(app)
        if 'username' in session:
            if id.isdigit():
                username = session['username']
                id_username = models.get_id(username)
                if models.get_task_id(id_username, id) == False:
                    api['error'] = TASK_ID_KO_RES
                    response = jsonify(api)
                    response.status_code = 201
                    return response
            else:
                api['error'] = INTERNAL_ERROR
                response = jsonify(api)
                response.status_code = 202
                return response
        else:
            api['error'] = NOT_CONNECTED
            response = jsonify(api)
            response.status_code = 203
            return response
        api['result'] = models.show_task_id(id)
        response = jsonify(api)
        response.status_code = 200
        return response
    def show_all_task(self):
        i = 0
        api = {}
        tasks = {}
        my_task_id = []
        result = {}
        models = SQLManagement(app)
        if 'username' in session:
                username = session['username']
                id_username = models.get_id(username)
        else:
            api['error'] = NOT_CONNECTED
            response = jsonify(api)
            response.status_code = 200
            return response
        ok = models.show_all_task_id(id_username)
        for rows in ok:
            idt = (rows['fk_task_id'])
            my_task_id.append(models.show_task_per_id(idt))
            i += 1
        tasks["tasks"] = my_task_id
        result["result"] = tasks
        return jsonify(result)
    def list_all_taks_easy(self):
        i = 0
        api = {}
        my_task_id = []
        models = SQLManagement(app)
        if 'username' in session:
                username = session['username']
                id_username = models.get_id(username)
        else:
            api['error'] = NOT_CONNECTED
            response = jsonify(api)
            response.status_code = 200
            return response
        ok = models.show_all_task_id(id_username)
        for rows in ok:
            idt = (rows['fk_task_id'])
            my_task_id.append(models.show_task_per_id_easy(idt))
            i += 1
        return jsonify(my_task_id)
    def update_task_id(self, request, id_task):
        api = {}
        models = SQLManagement(app)
        title = request.form['title']
        date_begin = request.form['begin']
        date_end = request.form['end']
        status = request.form['status']
        if 'username' in session:
            if title and status:
                username = session['username']
                id = models.get_id(username)
                if models.get_task_id(id, id_task) == False:
                    api['error'] = "Pas ta task frere"
                    response = jsonify(api)
                    response.status_code = 201
                    return response
            else:
                api['error'] = "Il mange title ou status frere"
                response = jsonify(api)
                response.status_code = 202
                return response
        else:
            api['error'] = CONNECTED
            response = jsonify(api)
            response.status_code = 203
            return response
        models.update_task(id, title, status, date_begin, date_end, id_task)
        api['result'] = "Updated"
        response = jsonify(api)
        response.status_code = 200
        return response

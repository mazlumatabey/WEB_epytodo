#!/usr/bin/env python3
##
## EPITECH PROJECT, 2019
## EpyTodo
## File description:
## Models
##

import pymysql as sql
from app import *

class ConnectionManager(object):
    def __init__(self, app):
        self.connection = ""
        self.connect_to_server(app)

    def getconnection(self):
        return self.connection

    def connect_to_server(self, app):
        try:
            self.connection = sql.connect(host=app.config['DATABASE_HOST'],
                            unix_socket=app.config['DATABASE_SOCK'],
                            user=app.config['DATABASE_USER'],
                            passwd=app.config['DATABASE_PASS'],
                            db=app.config['DATABASE_NAME'])
        except Exception as e:
            print("Caught an exception : ", e)

class SQLManagement(object):
    def __init__(self, app):
        self.app = app
        self.sqlcon = app.conn

    def _create_user(self, username, password):
        try:
            cursor = self.sqlcon.cursor()
            sql = "INSERT INTO `user` (`username`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            self.sqlcon.commit()
            cursor.close()
        except Exception as e :
            print("Caught an exception : ", e)
    def connect(self, username, password):
        try:
            cursor = self.sqlcon.cursor()
            query = 'SELECT * FROM user WHERE username = %s AND password = %s'
            cursor.execute(query, (username, password ))
            result = cursor.fetchone()
            cursor.close()
            if not result:
                return False
            else:
                return True
        except Exception as e :
            print("Caught an exception : ", e)

    def check_user_exists_username(self, username):
        try:
            cursor = self.sqlcon.cursor()
            query = 'SELECT * FROM user WHERE username = %s'
            cursor.execute(query, (username, ))
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            if not rows:
                return False
            else:
                return True
        except Exception as e :
            print("Caught an exception : ", e)
    def get_id(self, username):
        try:
            cursor = self.sqlcon.cursor()
            query = 'SELECT * FROM user WHERE username = %s'
            cursor.execute(query, (username, ))
            result = cursor.fetchone()
            return result[0]
        except Exception as e :
            print("Caught an exception : ", e)
    def add_user_task(self, id_username, title, status, date_begin, date_end):
        try:
            cursor = self.sqlcon.cursor()
            sql = "INSERT INTO task (title, begin, end, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (title, date_begin, date_end, status))
            self.sqlcon.commit()
            id_task = cursor.lastrowid
            cursor.close()
            cursor = self.sqlcon.cursor()
            sql = "INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES (%s, %s)"
            cursor.execute(sql, (id_username, id_task))
            self.sqlcon.commit()
        except Exception as e :
            print("Caught an exception : ", e)
    def update_task(self, id_username, title, status, date_begin, date_end, task_id):
        try:
            cursor = self.sqlcon.cursor()
            sql = "UPDATE task SET title = %s, begin = %s, end = %s, status = %s WHERE task_id = %s"
            cursor.execute(sql, (title, date_begin, date_end, status, task_id))
            self.sqlcon.commit()
            cursor.close()
        except Exception as e :
            print("Caught an exception : ", e)
    def get_task_id(self, username_id, task_id):
        try:
            cursor = self.sqlcon.cursor()
            query = 'SELECT * FROM user_has_task WHERE fk_user_id = %s AND fk_task_id = %s'
            cursor.execute(query, (username_id, task_id ))
            result = cursor.fetchone()
            if not result:
                return False
            else:
                return True
        except Exception as e :
            print("Caught an exception : ", e)
    def del_task(self, id_task):
        try:
            cursor = self.sqlcon.cursor()
            sql = "DELETE FROM task where task_id = %s"
            cursor.execute(sql, (id_task))
            self.sqlcon.commit()
            cursor.close()
            cursor = self.sqlcon.cursor()
            sql = "DELETE FROM user_has_task where fk_task_id = %s"
            cursor.execute(sql, (id_task))
            self.sqlcon.commit()
        except Exception as e :
            print("Caught an exception : ", e)
    def show_task_id(self, task_id):
        api = {}
        try:
            cursor = self.sqlcon.cursor(sql.cursors.DictCursor)
            query = 'SELECT * FROM task WHERE task_id = %s'
            cursor.execute(query, (task_id ))
            result = cursor.fetchone()
            api = {
                "title": result['title'],
                "begin": result['begin'],
                "end": result['end'],
                "status": result['status']
            }
            cursor.close()
            return api
        except Exception as e :
            print("Caught an exception : ", e)
    def show_task_per_id(self, task_id):
        api = {}
        api_result = {}
        try:
            cursor = self.sqlcon.cursor(sql.cursors.DictCursor)
            query = 'SELECT * FROM task WHERE task_id = %s'
            cursor.execute(query, (task_id ))
            result = cursor.fetchone()
            api = {
                "title": result['title'],
                "begin": result['begin'],
                "end": result['end'],
                "status": result['status']
            }
            api_result[str(task_id)] = api
            cursor.close()
            return api_result
        except Exception as e :
            print("Caught an exception : ", e)
    def show_all_task_id(self, id):
        try:
            cursor = self.sqlcon.cursor(sql.cursors.DictCursor)
            query = 'SELECT fk_task_id FROM user_has_task WHERE fk_user_id = %s'
            cursor.execute(query, (id ))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e :
            print("Caught an exception XD : ", e)
    def show_task_per_id_easy(self, task_id):
        try:
            cursor = self.sqlcon.cursor(sql.cursors.DictCursor)
            query = 'SELECT * FROM task WHERE task_id = %s'
            cursor.execute(query, (task_id ))
            result = cursor.fetchone()
            cursor.close()
            api = {
                "id": task_id,
                "title": result['title'],
                "begin": result['begin'],
                "end": result['end'],
                "status": result['status']
            }
            return api
        except Exception as e :
            print("Caught an exception : ", e)

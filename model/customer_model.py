import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig

class user_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("connect success")
        except: 
            print('error')

    def user_get_all_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            return make_response({"message": "No data found"}, 204)
        
    def user_add_model(self, data):
        query = "INSERT INTO users(name, email, phone, role, password) VALUES (%s, %s, %s, %s, %s)"
        values = (data['name'], data['email'], data['phone'], data['role'], data['password'])

        self.cur.execute(query, values)
        return make_response({"message": "User successfully created"}, 201)
    
    def user_update_model(self, data):
        query = "UPDATE users SET name=%s, email=%s, phone=%s, role=%s, password=%s WHERE id=%s"
        values = (data['name'], data['email'], data['phone'], data['role'], data['password'], data['id'])

        self.cur.execute(query, values)
        if self.cur.rowcount>0:
            return make_response({"message": "User updated successfully"}, 201)
        else:
            return make_response({"message": "Nothing to update"}, 202)
        
    def user_delete_model(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message": "User deleted successfully"}, 200)
        else:
            return make_response({"message": "Nothing to delete"}, 202)
    
    def user_patch_model(self, data, id):
        query="UPDATE users SET "
        for key in data:
            query += f"{key}='{data[key]}',"

        query = query[:-1] + f" WHERE id = {id}"

        self.cur.execute(query)
        if self.cur.rowcount>0:
            return make_response({"message": "User updated successfully"}, 201)
        else:
            return make_response({"message": "Nothing to update"}, 202)
        
    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit

        query = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload":result ,"page_no":page ,"limit":limit}, 200)
            return res
        else:
            return make_response({"message": "No data found"}, 204)
    
    def user_upload_avatar_model(self, uid, finalpath):
        query = "UPDATE users SET avatar=%s WHERE id=%s"
        values = (finalpath, uid)

        self.cur.execute(query, values)
        if self.cur.rowcount>0:
            return make_response({"message": "FILE_UPLOADED_SUCCESSFULLY"}, 201)
        else:
            return make_response({"message": "Nothing to update"}, 202)
        
    def user_login_model(self, data):
        # print(str(data))
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload": userdata,
            "exp": exp_epoch_time
        }
        jwtoken = jwt.encode(payload, "sagar", algorithm="HS256")
        return make_response({"token":jwtoken}, 200)
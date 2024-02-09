import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
# import jwt
from config.config import dbconfig

class customer_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("connect success")
        except: 
            print('error')

    def customer_get_all_model(self):
        self.cur.execute("SELECT * FROM customers")
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            return make_response({"message": "No data found"}, 204)
        
    def customer_add_model(self, data):
        query = "INSERT INTO customers(name, instagram, fav_color) VALUES (%s, %s, %s)"
        values = (data['name'], data['instagram'], data['fav_color'])

        self.cur.execute(query, values)
        return make_response({"message": "Customer successfully created"}, 201)
    
    def customer_update_model(self, data):
        query = "UPDATE customers SET name=%s, instagram=%s, fav_color=%s"
        values = (data['name'], data['instagram'], data['fav_color'])

        self.cur.execute(query, values)
        if self.cur.rowcount>0:
            return make_response({"message": "Customer updated successfully"}, 201)
        else:
            return make_response({"message": "Nothing to update"}, 202)
        
    def customer_delete_model(self, id):
        self.cur.execute(f"DELETE FROM customers WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message": "Customers deleted successfully"}, 200)
        else:
            return make_response({"message": "Nothing to delete"}, 202)
    
    def customer_patch_model(self, data, id):
        query="UPDATE customers SET "
        for key in data:
            query += f"{key}='{data[key]}',"

        query = query[:-1] + f" WHERE id = {id}"

        self.cur.execute(query)
        if self.cur.rowcount>0:
            return make_response({"message": "Customer updated successfully"}, 201)
        else:
            return make_response({"message": "Nothing to update"}, 202)
        
    # def user_pagination_model(self, limit, page):
    #     limit = int(limit)
    #     page = int(page)
    #     start = (page*limit)-limit

    #     query = f"SELECT * FROM users LIMIT {start}, {limit}"
    #     self.cur.execute(query)
    #     result = self.cur.fetchall()
    #     if len(result)>0:
    #         res = make_response({"payload":result ,"page_no":page ,"limit":limit}, 200)
    #         return res
    #     else:
    #         return make_response({"message": "No data found"}, 204)
    
    # def user_upload_avatar_model(self, uid, finalpath):
    #     query = "UPDATE users SET avatar=%s WHERE id=%s"
    #     values = (finalpath, uid)

    #     self.cur.execute(query, values)
    #     if self.cur.rowcount>0:
    #         return make_response({"message": "FILE_UPLOADED_SUCCESSFULLY"}, 201)
    #     else:
    #         return make_response({"message": "Nothing to update"}, 202)
        
    # def user_login_model(self, data):
    #     # print(str(data))
    #     self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
    #     result = self.cur.fetchall()
    #     userdata = result[0]
    #     exp_time = datetime.now() + timedelta(minutes=15)
    #     exp_epoch_time = int(exp_time.timestamp())
    #     payload = {
    #         "payload": userdata,
    #         "exp": exp_epoch_time
    #     }
    #     jwtoken = jwt.encode(payload, "sagar", algorithm="HS256")
    #     return make_response({"token":jwtoken}, 200)
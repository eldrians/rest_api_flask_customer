from app import app
from model.customer_model import customer_model
# from model.auth_model import auth_model
from flask import request, send_file
from datetime import datetime

obj = customer_model()
# auth = auth_model()

@app.route("/customer")
# @auth.token_auth()
def customer_get_all_controller():
    return obj.customer_get_all_model()

@app.route("/user/add", methods=["POST"])
# @auth.token_auth()
def costumer_add_controller():
    return obj.costumer_add_model(request.form)

@app.route("/user/update", methods=["PUT"])
def costumer_update_controller():
    return obj.costumer_update_model(request.form)

@app.route("/user/delete/<id>", methods=["DELETE"])
def costumer_delete_controller(id):
    return obj.costumer_delete_model(id)

@app.route("/user/patch/<id>", methods=["PATCH"])
def costumer_patch_controller(id):
    return obj.costumer_patch_model(request.form, id)

# @app.route("/user/all/limit/<limit>/page/<page>", methods=["GET"])
# def user_pagination_controller(limit, page):
#     return obj.user_pagination_model(limit, page)

# @app.route("/user/<uid>/upload/avatar", methods=["PUT"])
# def user_upload_avatar_controller(uid):
#     file = request.files['avatar']
#     uniqueFileName = str(datetime.now().timestamp()).replace(".","")
#     fileNameSplit = file.filename.split(".")
#     ext = fileNameSplit[len(fileNameSplit)-1]
#     finalFilePath = f"uploads/{uniqueFileName}.{ext}" 
#     file.save(finalFilePath)
#     return obj.user_upload_avatar_model(uid, finalFilePath)

# @app.route("/uploads/<filename>")
# def user_getavatar_controller(filename):
#     return send_file(f"uploads/{filename}")

# @app.route("/user/login", methods=["POST"])
# def user_login_controller():
#     return obj.user_login_model(request.form)
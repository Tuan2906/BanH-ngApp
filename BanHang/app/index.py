from  flask import render_template,request, redirect
from app import app, login
import  dao
from admin import admin
from flask_login import login_user
@app.route("/")
def Home():
   giatri = request.args.get('keyword')
   return render_template("index.html",categories=dao.load_cat(),product=dao.load_Product(giatri))
@app.route("/admin/login", methods=["post"])
def login_admin():
    u= request.form.get("username")
    p= request.form.get("password")
    laytt= dao.xacThuc_user(username=u,password=p)
    if laytt:
        login_user(user=laytt)
    return redirect("/admin")

@login.user_loader
def load_login(userid):
    return dao.layuser(userid)
if __name__=="__main__":
    app.run(debug=True)
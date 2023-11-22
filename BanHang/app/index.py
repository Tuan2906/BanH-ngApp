from  flask import render_template,request, redirect,jsonify,session
from app import app, login,utils
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

@app.route('/api/cart',methods=['post'])
def add_card():

   data= request.json
   cart=session.get('cart')
   if cart is None:
       cart={}
   id= str(data.get("id"))
   if id in cart:
      cart[id]['quanity']+=1
   else:
       cart[id]={
           'id':id,
           'name': data.get('name'),
           'price': data.get('price'),
           'quanity':1
       }
   session['cart']=cart
   return jsonify(
       utils.count_cart(cart)
   )

if __name__=="__main__":
    app.run(debug=True)
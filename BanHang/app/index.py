from  flask import render_template,request
from app import app
import  dao
from admin import admin
@app.route("/")
def Home():
   giatri = request.args.get('keyword')
   return render_template("index.html",categories=dao.load_cat(),product=dao.load_Product(giatri))

if __name__=="__main__":
    app.run(debug=True)
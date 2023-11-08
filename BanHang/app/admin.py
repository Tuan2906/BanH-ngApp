from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from app import app,db
from app.models import  DanhMuc,SanPham
admin=Admin(app=app,name="Quan tri ban hang",template_mode="bootstrap4")
class View_DanhMuc(ModelView):
    column_list = ['id','name','products']
    can_export = True
    column_filters = ['name']
class View_SanPham(ModelView):
    column_list = ['id','name','price']
    column_searchable_list = ['name','price']
    column_filters = ['name','price']
    column_editable_list = ['name','price']
    details_modal = True

admin.add_view(View_DanhMuc(DanhMuc,db.session))
admin.add_view(View_SanPham(SanPham,db.session))

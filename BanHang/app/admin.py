from app.models import *
from app import app, db, dao
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request

admin = Admin(app=app, name="Quan tri a", template_mode="bootstrap4")


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.admin


class AuthenticatedAdmin_EmpLoyee(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.user_role == UserRoleEnum.admin or current_user.is_authenticated and current_user.user_role == UserRoleEnum.nhanVien:
            return current_user.is_authenticated


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class View_DanhMuc(AuthenticatedAdmin):
    column_list = ['id', 'name', 'products']
    can_export = True
    column_filters = ['name']


class View_SanPham(AuthenticatedAdmin_EmpLoyee):
    column_list = ['id', 'name', 'price', 'mota']
    column_searchable_list = ['name', 'price']
    column_filters = ['name', 'price']
    column_editable_list = ['name', 'price']
    details_modal = True


class View_TaiKhoan(AuthenticatedAdmin):
    column_list = ['id', 'username', 'password', 'user']
    can_export = True
    column_filters = ['username']


class View_User(AuthenticatedAdmin):
    column_list = ['id', 'hoTen', 'diaChi', 'sdt']
    can_export = True
    column_filters = ['hoTen']


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


class statistical(BaseView):
    @expose("/")
    def index(self):
        if request.args.get("month"):
            month = request.args.get("month", datetime.now())
        else:
            month = datetime.now().month
        return self.render('admin/thongke.html', states=dao.stats_revenue_by_month(month=month),
                           sum=dao.tong_doanh_thu(m=month))

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(View_DanhMuc(DanhMuc, db.session))
admin.add_view(View_SanPham(SanPham, db.session))
admin.add_view(View_TaiKhoan(TaiKhoan, db.session))
admin.add_view(View_User(User, db.session))
admin.add_view(statistical(name="Thống kê doanh thu"))
admin.add_view(LogoutView(name='Đăng xuất'))

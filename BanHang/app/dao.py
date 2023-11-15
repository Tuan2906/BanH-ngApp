import hashlib

from app.models import  DanhMuc,SanPham,User
def load_cat():
    return DanhMuc.query.all()
def load_Product(kw=None):
    product=SanPham.query
    if kw:
        product=product.filter(SanPham.name.contains(kw))
    return product.all()
def layuser(user_id):
    return User.query.get(user_id)
def xacThuc_user(username, password):
    password= str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password.strip())).first()


from sqlalchemy import Column,Integer,String,ForeignKey,Float,Enum
from sqlalchemy.orm import relationship
from app import db,app
from flask_login import UserMixin
import enum
class UserRoleEnum(enum.Enum):
    user=1;
    admin=2;
class DanhMuc(db.Model):
    __tablename__="DanhMuc"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50),nullable=False,unique=True)
    products=relationship('SanPham',backref='DanhMuc',lazy=True)
    def __str__(self):
        return self.name

class User(db.Model):
    id= Column(Integer, primary_key= True,autoincrement=True)
    username=Column(String(20), unique=True, nullable=False)
    password= Column(String(20), unique=True, nullable=False)
    user_role=Column(Enum(UserRoleEnum),default=UserRoleEnum.user)

class SanPham(db.Model):
    __tablename__ = "SanPham"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price= Column(Float,default=0)
    image= Column(String(255))
    danhmuc_id=Column(Integer,ForeignKey(DanhMuc.id),nullable=False)
    def __str__(self):
        return self.name

if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        import hashlib
        u= User(username="Admin",password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.admin)
        db.session.add(u)
        # a= DanhMuc(name='IPhone')
        # Sp=SanPham(name='Iphone plus',price=59999,danhmuc_id=1,image='https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg')
        # Sp2=SanPham(name='Iphone plus 8',price=299,danhmuc_id=1,image='https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg')
        # db.session.add_all([a,Sp,Sp2])
        db.session.commit()

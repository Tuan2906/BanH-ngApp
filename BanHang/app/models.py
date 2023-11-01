from sqlalchemy import Column,Integer,String,ForeignKey,Float
from sqlalchemy.orm import relationship
from app import db,app
class DanhMuc(db.Model):
    __tablename__="DanhMuc"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50),nullable=False,unique=True)
    products=relationship('SanPham',backref='DanhMuc',lazy=True)
class SanPham(db.Model):
    __tablename__ = "SanPham"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price= Column(Float,default=0)
    image= Column(String(255))
    danhmuc_id=Column(Integer,ForeignKey(DanhMuc.id),nullable=False)

if __name__ == "__main__":
    with app.app_context():
        a= DanhMuc(name='IPhone')
        Sp=SanPham(name='Iphone plus',price=59999,danhmuc_id=1,image='https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg')
        Sp2=SanPham(name='Iphone plus 8',price=299,danhmuc_id=1,image='https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg')
        db.session.add_all([Sp,Sp2])
        db.session.commit()
        db.create_all()
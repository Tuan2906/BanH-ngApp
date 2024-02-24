from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime, Date
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
from datetime import datetime
import enum


class UserRoleEnum(enum.Enum):
    user = 1
    nhanVien = 3
    shipper = 4
    admin = 2


class DanhMuc(db.Model):
    __tablename__ = "DanhMuc"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('SanPham', backref='DanhMuc', lazy=True)

    def __str__(self):
        return self.name


class TaiKhoan(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), unique=True, nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.user)
    user = relationship('User', backref='tk', lazy=True)
    comment = relationship('Comment', backref='tk', lazy=True)

    def __str__(self):
        return self.username


class BaseUser(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(20), nullable=False)
    diaChi = Column(String(25), nullable=False)
    sdt = Column(String(13), nullable=False)
    # receipts = relationship('HoaDon', backref='user', lazy=True)
    # comments = relationship('Comment', backref='user', lazy=True)
    id_TK = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False, unique=True)


class User(BaseUser):
    receipts = relationship('HoaDon', backref='user', lazy=True)
    # comments = relationship('Comment', backref='user', lazy=True)


class SanPham(db.Model):
    __tablename__ = "SanPham"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(255))
    mota = Column(String(50))
    danhmuc_id = Column(Integer, ForeignKey(DanhMuc.id), nullable=False)
    ChiTietHoaDons = relationship('ChiTietHoaDon', backref='sanpham', lazy=True)

    def __str__(self):
        return self.name


class NhanVien(BaseUser):
    cccd = Column(String(12), unique=True, nullable=False)
    ngaySinh = Column(Date)
    gioiTinh = Column(String(5), nullable=False)
    luong = Column(Integer, nullable=False, default=0)
    anhxacthuc_CCCD = Column(String(50), nullable=False)


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


class HoaDon(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    id_NVshipper = Column(Integer, ForeignKey(NhanVien.id))
    trangThaiGiaoVan = Column(String(10), default='Dang Giao')
    ngayGiao= Column(DateTime, default=datetime.now())
    ChiTietHoaDons = relationship('ChiTietHoaDon', backref='hoadon', lazy=True)


class ChiTietHoaDon(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    product_id = Column(Integer, ForeignKey(SanPham.id), nullable=False)


class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_tk = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)
    product_id = Column(Integer, ForeignKey(SanPham.id), nullable=False)
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        import hashlib

        # u = TaiKhoan(username="Admin", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #              user_role=UserRoleEnum.admin)
        # db.session.add(u)
        # db.session.commit()

        # a= DanhMuc(name='IPhone')
        # Sp = SanPham(name='Iphone plus', price=59999, danhmuc_id=1,
        #              image='https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg')
        # Sp2 = SanPham(name='Iphone plus 8', price=299, danhmuc_id=1,
        #               image='https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg')
        # db.session.add_all([Sp,Sp2])
        db.session.commit()

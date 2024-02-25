import hashlib

from app.models import *
from app import app, db
import hashlib
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime


def load_cat():
    return DanhMuc.query.all()


def load_Product(kw=None):
    product = SanPham.query
    print("Vao Trong san pham")
    print(kw)
    if kw:
        product = product.filter(SanPham.name.contains(kw))
    print(product.all())
    return product.all()


def get_product_by_id(id):
    return SanPham.query.get(id)


def layuser(user_id):
    return TaiKhoan.query.get(user_id)


def lay_ttKH(tk):
    return User.query.filter(User.id_TK.__eq__(tk)).first()


def xacThuc_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                                 TaiKhoan.password.__eq__(password.strip())).first()


a = 0;


def luu_ThongTinKH(hoten, soDienThoai, diaChi):
    print(hoten, soDienThoai, diaChi)
    global a
    checkUser = User.query.filter(User.hoTen.__eq__(hoten), User.diaChi.__eq__(diaChi)).first()
    print(checkUser)
    if checkUser is not None:
        a = checkUser.id
        update_sdt = User.query.filter(User.sdt.__eq__(soDienThoai)).first()
        if update_sdt is None:
            checkUser.sdt = soDienThoai
            db.session.commit()
        return
    checkUser = User.query.filter(User.hoTen.__eq__(hoten), User.sdt.__eq__(soDienThoai)).first()
    if User.query.filter(User.hoTen.__eq__(hoten), User.sdt.__eq__(soDienThoai)).first() is not None:
        a = checkUser.id
        print("ton tai")
        update_diachi = User.query.filter(User.diaChi.__eq__(diaChi)).first()
        if update_diachi is None:
            print("CO")
            checkUser.diaChi = diaChi
            db.session.commit()
        return
    if current_user:
        print("Dang updata")
        update = User.query.filter(User.hoTen.__eq__(hoten)).first()
        update.diaChi = diaChi
        update.sdt = soDienThoai
        a = update.id
        db.session.commit()
        print("Update thanh cong ")
        return
    ht = User(hoTen=hoten, diaChi=diaChi, sdt=soDienThoai, tk=current_user)
    db.session.add(ht)
    db.session.commit()
    print("thong tin kh thanh cong")
    a = ht.id


def add_user(username, password, hoTen):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    check_TaiKhoan = TaiKhoan.query.filter(TaiKhoan.username.__eq__(username),
                                           TaiKhoan.password.__eq__(password)).first()
    if check_TaiKhoan:
        print(check_TaiKhoan.username)
        return
    u = TaiKhoan(username=username, password=password)
    db.session.add(u)
    db.session.commit()
    ht = User(hoTen=hoTen, diaChi="Chua Co", sdt=1, id_TK=u.id)
    db.session.add(ht)
    db.session.commit()
    print("Thanh Cong")


def lay_sanPhamDaDat(tk, month):
    print(tk)
    return ChiTietHoaDon.query \
        .join(SanPham, ChiTietHoaDon.product_id == SanPham.id) \
        .join(HoaDon, ChiTietHoaDon.receipt_id == HoaDon.id).filter(func.extract('month',
                                                                                 ChiTietHoaDon.created_date).__eq__(
        month)) \
        .join(User, HoaDon.user_id == User.id) \
        .filter(User.id_TK == tk) \
        .with_entities(ChiTietHoaDon.quantity, ChiTietHoaDon.price, SanPham.name, ChiTietHoaDon.active,
                       ChiTietHoaDon.created_date)


def add_receipt(cart, active):
    global a
    print("Luu Hoa Don")
    print(a)
    if cart:
        r = HoaDon(user_id=a, active=active)
        db.session.add(r)

        for c in cart.values():
            d = ChiTietHoaDon(quantity=c['quantity'], price=c['price'], hoadon=r, product_id=c['id'], active=active)
            db.session.add(d)

        try:
            print("thanhcong")
            db.session.commit()
            a = 1
        except:
            print("that bai")
            return False
        else:
            return True

    return False


# PHẦN  BÌNH lUẬN
def get_comments(product_id):
    return (Comment.query.join(TaiKhoan, Comment.id_tk == TaiKhoan.id)
            .filter(Comment.product_id.__eq__(product_id)).with_entities(Comment.content, Comment.created_date,
                                                                         TaiKhoan.username))


def add_comment(product_id, content):
    c = Comment(product_id=product_id, content=content, tk=current_user)
    db.session.add(c)
    db.session.commit()

    return c


# Phan Thong Ke Doanh Thu
def stats_revenue(kw=None):
    query = db.session.query(SanPham.id, SanPham.name, func.sum(ChiTietHoaDon.price * ChiTietHoaDon.quantity)) \
        .join(ChiTietHoaDon, ChiTietHoaDon.product_id.__eq__(SanPham.id))
    if kw:
        query = query.filter(SanPham.name.contains(kw))

    return query.group_by(SanPham.id).all()


def stats_revenue_by_month(month):
    print(db.session.query(SanPham.id, SanPham.name,
                           func.sum(ChiTietHoaDon.price * ChiTietHoaDon.quantity)) \
          .join(SanPham, ChiTietHoaDon.product_id.__eq__(SanPham.id)) \
          .filter(func.extract('month', ChiTietHoaDon.created_date).__eq__(month)) \
          .group_by(SanPham.id, SanPham.name).all())
    return db.session.query(SanPham.id, SanPham.name, func.extract('month', HoaDon.created_date),
                            func.sum(ChiTietHoaDon.price * ChiTietHoaDon.quantity)) \
        .join(ChiTietHoaDon, ChiTietHoaDon.receipt_id.__eq__(HoaDon.id)).join(SanPham, ChiTietHoaDon.product_id.__eq__(
        SanPham.id)) \
        .filter(func.extract('month', ChiTietHoaDon.created_date).__eq__(month)) \
        .group_by(SanPham.id, SanPham.name, func.extract('month', HoaDon.created_date)).all()


def tong_doanh_thu(m):
    tong = 0
    for s in stats_revenue_by_month(m):
        tong += s[3]
    return tong


def luu_thongtinNV(hoten, diaChi, sdt, cccd, ngaySinh, gioiTinh, anhxacthuc, diaChiEmail):
    password = str(hashlib.md5(diaChiEmail.encode('utf-8')).hexdigest())
    check_TaiKhoan = TaiKhoan.query.filter(TaiKhoan.username.__eq__(sdt),
                                           TaiKhoan.password.__eq__(password)).first()
    if check_TaiKhoan:
        print(check_TaiKhoan.username)
        return
    u = TaiKhoan(username=sdt, password=password, user_role=UserRoleEnum.shipper)
    db.session.add(u)
    db.session.commit()
    nv = NhanVien(hoTen=hoten, diaChi=diaChi, sdt=sdt, ngaySinh=ngaySinh, gioiTinh=gioiTinh, anhxacthuc_CCCD=anhxacthuc,
                  id_TK=u.id, cccd=cccd)
    db.session.add(nv)
    db.session.commit()


# Phan xu ly lay dia chi cua shipper phuc vu cho viec phan phoi van chuyen don hang phu hop
def truyvan_DiaChiShipper(tk):
    print(tk)
    diaChi = NhanVien.query.filter(NhanVien.id_TK.__eq__(tk)).first()
    print(diaChi)
    return diaChi


# Phan nay xu ly thong tin don hang cua shipper da nhan dc nhung chua giao hang
def layHoaDon():
    orders = db.session.query(
        User.diaChi, User.hoTen, User.sdt,
        db.func.sum(ChiTietHoaDon.quantity * ChiTietHoaDon.price).label('tongtien'),
        HoaDon.id, HoaDon.active
    ).join(HoaDon, HoaDon.id == ChiTietHoaDon.receipt_id) \
        .join(User, HoaDon.user_id == User.id) \
        .filter(HoaDon.trangThaiGiaoVan == 'Dang Giao') \
        .group_by(HoaDon.id, User.diaChi, User.hoTen, User.sdt, HoaDon.active)
    return orders


def truyvan_DonHangDaUpdate(id_shipper):
    orders = db.session.query(
        User.diaChi, User.hoTen, User.sdt,
        db.func.sum(ChiTietHoaDon.quantity * ChiTietHoaDon.price).label('tongtien'),
        HoaDon.id, HoaDon.active
    ).join(HoaDon, HoaDon.id == ChiTietHoaDon.receipt_id) \
        .join(User, HoaDon.user_id == User.id) \
        .filter(HoaDon.trangThaiGiaoVan == 'Dang Giao', HoaDon.id_NVshipper == id_shipper) \
        .group_by(HoaDon.id, User.diaChi, User.hoTen, User.sdt, HoaDon.active)
    return orders


# Phan nay xu ly thong tin ve nhan don hang vao ngay moi cho shipper
def truyvan_DonHang(id_HoaDon):
    # Lấy ngày hiện tại
    print("Kiem don hang moi")
    ngay_hien_tai = datetime.now().date()
    print(ngay_hien_tai)
    query = db.session.query(
        ChiTietHoaDon.id,
        SanPham.name, ChiTietHoaDon.quantity,
        (ChiTietHoaDon.quantity * ChiTietHoaDon.price).label('tongtien'),
    ).join(HoaDon, HoaDon.id == ChiTietHoaDon.receipt_id).filter(HoaDon.id == id_HoaDon) \
        .join(SanPham, SanPham.id == ChiTietHoaDon.product_id)
    print('Vao xem checck')
    print(query.all())
    return query


def update_nvdatHang(id_donhang, id_shipper):
    print("Phan update nv dathang")
    print(id_donhang, id_shipper)

    lay_id = HoaDon.query.filter(HoaDon.id.__eq__(id_donhang)).first()
    print(lay_id.id_NVshipper)
    lay_id.id_NVshipper = id_shipper
    db.session.commit()


def update_DonHang(id):
    lay_id = HoaDon.query.filter(HoaDon.id.__eq__(id)).first()
    lay_id.trangThaiGiaoVan = "Da Giao"
    db.session.commit()


# Phan lich su cac don hang da xu ly cua shipper
def updonhangshipper(id_Shipper):
    return ChiTietHoaDon.query \
        .join(SanPham, ChiTietHoaDon.product_id == SanPham.id) \
        .join(HoaDon, ChiTietHoaDon.receipt_id == HoaDon.id) \
        .join(NhanVien, HoaDon.id_NVshipper == NhanVien.id) \
        .filter(NhanVien.id_TK == id_Shipper) \
        .with_entities(ChiTietHoaDon.quantity, ChiTietHoaDon.price, SanPham.name, HoaDon.trangThaiGiaoVan,
                       HoaDon.ngayGiao)

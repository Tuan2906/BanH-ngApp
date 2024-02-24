import random

import stripe

from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user
from app import dao,admin
from app import app, login, utils

stripe.api_key = "sk_test_51OQW7nEDuGccAkUEVhnnJfvWztoRchurir6oDVg1AWBcag4lw6fvIYsU8FiFc4zPY2rBbmyHyuDNdHObDOl0ei96000SDdfuHI"
public_key = "pk_test_51OQW7nEDuGccAkUEwtUAoxMsf7qoYBGNWEytAWuxxRJt3FwqwP1PjDe0nuJREw9HLdNTtwj7ItvjBRxTj3oKCQJ900ivAUTxhX"

check = False
dem = 0


@app.route("/")
def Home():
    giatri = request.args.get('keyword')
    global dem
    check = False
    dem += 1
    print("Home---")
    print(check)
    return render_template("index.html", categories=dao.load_cat(), product=dao.load_Product(giatri))


@app.route("/admin/login", methods=["post"])
def login_admin():
    u = request.form.get("username")
    p = request.form.get("password")
    user = dao.xacThuc_user(username=u, password=p)
    print(user)
    if user:
        print('dung')
        login_user(user)
        print('loi')
    return redirect("/admin")


@login.user_loader
def load_login(userid):
    return dao.layuser(userid)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route("/api/cart/<product_id>", methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<product_id>", methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


laysp = ""


@app.route("/api/load_sp", methods=['get', 'post'])
def load_sp():
    global laysp
    data = request.json
    print(data.get('name'))
    sp = dao.load_Product(kw=data.get('name'))
    print(sp)
    laysp = sp
    return


@app.route("/uploadsp", methods=['get', 'post'])
def load_spDM():
    print(session.get("load_sp"))
    return render_template("index.html", product=laysp)


@app.route("/api/cart", methods=['post'])
def add_to_cart():
    data = request.json
    print(data)
    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.context_processor
def common_responses():
    return {
        'categories': dao.load_cat(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


# xem chi tiet san pham
@app.route('/products/<id>')
def details(id):
    cms = dao.get_comments(id).all()
    sl_cms = len(cms)
    return render_template('details.html',
                           product=dao.get_product_by_id(id), comments=cms, sl=sl_cms)


# Thông Tin khách hàng
@app.route("/nhapthongtinkhachhang", methods=['get', 'post'])
def nhapThongTinKhachHang():
    demluot = 0
    hoten_KH = dao.lay_ttKH(session.get("id_tk"))
    return render_template("ThongTinKhachHang.html", demluot=demluot, hoten_KH=hoten_KH)


@app.route("/thanhtoan", methods=['get', 'post'])
def laythongtinKH():
    err_msg = None
    if request.method.__eq__('POST'):
        hoten = request.form.get('name')
        sdt = request.form.get('SDT')
        diaChi = request.form.get('diaChi')
        ttkh = {
            'ht': hoten,
            'sdt': sdt,
            'diachi': diaChi
        }
        # if hoten is not None and sdt is not None:
        #     try:
        #         dao.luu_ThongTinKH(hoten=request.form.get('name'),
        #                            soDienThoai=request.form.get('SDT'),
        #                            diaChi=request.form.get('diaChi'))
        #     except Exception as ex:
        #         err_msg = str(ex)
        #     else:
        #         return redirect('/thanhtoan')
        # else:
        #     err_msg = 'Mật khẩu KHÔNG khớp!'
        session["tt_kh"] = ttkh
    return render_template('nhapThongTinThanhToan.html', public_key=public_key)


@app.route("/update_ttKH", methods=['get'])
def load_ttKH():
    thongtin_KH = dao.lay_ttKH(tk=session.get("id_tk"))
    demluot = 1
    print(session.get("id_tk"))

    print(thongtin_KH)
    return render_template("ThongTInKhachHang.html", tt_KH=thongtin_KH, demluot=1)


@app.route("/up_ttsp", methods=['get', 'post'])
def load_ttsp():
    demluot = 2
    if request.method.__eq__("GET"):
        thongtin_sp = dao.lay_sanPhamDaDat(tk=session.get("id_tk"), month=2).all()
        # print(thongtin_sp)
        # print(thongtin_sp[0][3])
    else:
        month = request.form.get('thang')
        thongtin_sp = dao.lay_sanPhamDaDat(tk=session.get("id_tk"), month=int(month)).all()
    sl_sp = len(thongtin_sp)
    tinhtrang = []
    if sl_sp > 0:
        for i in range(sl_sp):
            if thongtin_sp[i][3]:
                tinhtrang.append("Đã thanh toan")
            else:
                tinhtrang.append("Đang Chờ thanh toán")

    return render_template("ThongTInKhachHang.html", soluong_sp=sl_sp, tt_sp=thongtin_sp, demluot=demluot,
                           tinhtrang=tinhtrang)


@app.route("/api/pay", methods=['post'])
def pay():
    cart = session.get('cart')
    if dao.add_receipt(cart):
        del session['cart']
        return jsonify({'status': 200})

    return jsonify({'status': 500, 'err_msg': 'Something wrong!'})


a = 1


@app.route('/payment', methods=['POST', 'get'])
def payment():
    global a
    # CUSTOMER INFO
    # luuThongTinHanhKhach()
    print(request.form.get("loai"))
    loai = request.form.get("loai")
    if request.method.__eq__("POST"):
        if a == 2:
            a = 1
            return redirect("/")
        a += 1;

        if loai is None:
            print("loi")
            customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                              source=request.form['stripeToken'])  # PAYMENT INFO
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=utils.count_cart(session.get('cart')).get('total_amount'),  # 19.99
                currency='vnd',
                description='Trả tiền mua sản phẩm'
            )
        if dao.luu_ThongTinKH(hoten=session.get('tt_kh').get('ht'),
                              soDienThoai=session.get('tt_kh').get('sdt'),
                              diaChi=session.get('tt_kh').get('diachi')):
            del session['tt_kh']
        cart = session.get('cart')
        print(session.get('tt_kh').get('diachi'))
        print(loai)
        if loai is not None:
            print("Dung la Tien Mat")
            if dao.add_receipt(cart, active=False):
                del session['cart']
                laysp = ""
        else:
            print("Dung la chuyen khoan")
            if dao.add_receipt(cart, active=True):
                del session['cart']
                laysp = ""
        print(cart)
        return render_template('index.html')
    else:
        del session['cart']
        return render_template('index.html')


@app.route('/login', methods=['get', 'post'])
def login_view():
    global check
    print(check)
    print('dem:', dem)
    if dem > 0: check = False
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.xacThuc_user(username=username, password=password)
        print("Kiem tra user dang nhap")
        print(user)
        if user:
            session['id_tk'] = user.id
            login_user(user)
            print(str(user.user_role))
            if str(user.user_role).__eq__("UserRoleEnum.nhanVien"):
                print("user rol nv thanh cong")
                return redirect("/")
            if str(user.user_role).__eq__("UserRoleEnum.shipper"):
                ds_shipper = SanLoc_DonHang()
                ds_ChiTietDonHang = chitiet_DH
                print("Phan XU ly truy xuat")
                print(ds_ChiTietDonHang)
                sl_dh_oneShipper = len(ds_shipper)
                sl_chitietDH = len(chitiet_DH)
                return render_template('indexShipper.html', dsshiper=ds_shipper, sl=sl_dh_oneShipper,
                                       ds_ChiTietDonHang=ds_ChiTietDonHang, soluong=sl_chitietDH)
        next = request.args.get('next')
        print(next)
        if next:
            return redirect(next)
        return redirect("/")
    if check:
        return render_template('login.html', check=check)
    else:
        return render_template('login.html', check=check)


def layChiTietDonHang(id_HoaDon):
    print(id_HoaDon)
    chitiet_DH = dao.truyvan_DonHang(id_HoaDon=id_HoaDon)
    sl = len(chitiet_DH.all())
    dsChiTiet_DH = []
    j = 0
    for i in range(sl):
        if chitiet_DH[i][0] != chitiet_DH[j][0] or j == 0:
            dsChiTiet_DH.append(
                {
                    'id': chitiet_DH[i][0],
                    'sp': chitiet_DH[i][1],
                    'sl': chitiet_DH[i][2],
                    'thanhtien': chitiet_DH[i][3]
                }
            )
            j += 1
    print("Chi Tiet Don Hang")
    return dsChiTiet_DH


chitiet_DH = []


def SanLoc_DonHang():
    global chitiet_DH
    don_hangs = dao.layHoaDon()
    print("Text")

    dia_Chi = dao.truyvan_DiaChiShipper(tk=session.get('id_tk'))
    sl_dh = len(don_hangs.all())
    ds_dhshipper = []
    if sl_dh > 0:
        so_ngau_nhien = random.randint(0, sl_dh - 1)
        tam = dem_sl = 0
        print(dia_Chi)
        print(so_ngau_nhien)
        for i in range(sl_dh):
            print(tam)
            try:
                if so_ngau_nhien == 0 and dem_sl == 0:
                    print("Oke")
                    tam = 1
                if tam != so_ngau_nhien:
                    print(don_hangs[so_ngau_nhien][0])
                    if don_hangs[so_ngau_nhien][0] == dia_Chi.diaChi and dem_sl < 2:
                        print("Vao dc")
                        chitiet_DH = layChiTietDonHang(id_HoaDon=don_hangs[so_ngau_nhien][4])
                        if not don_hangs[so_ngau_nhien][5]:
                            ds_dhshipper.append(
                                {
                                    'ma_vaDon': "VTDH" + str(don_hangs[so_ngau_nhien][4]),
                                    'diaChiNha': don_hangs[so_ngau_nhien][0],
                                    'hoten': don_hangs[so_ngau_nhien][1],
                                    'sdt': don_hangs[so_ngau_nhien][2],
                                    'tongtien': don_hangs[so_ngau_nhien][3],

                                    'tinhTrang': 'Tra Tien Mat'
                                }
                            )
                        else:
                            ds_dhshipper.append(
                                {
                                    'ma_vaDon': "VTTH" + str(don_hangs[so_ngau_nhien][4]),
                                    'diaChiNha': don_hangs[so_ngau_nhien][0],
                                    'hoten': don_hangs[i][1],
                                    'sdt': don_hangs[i][2],
                                    'tongtien': don_hangs[i][3],

                                    'tinhTrang': 'Da Thanh Toan'
                                }
                            )
                        dao.update_nvdatHang(id_shipper=dia_Chi.id, id_donhang=don_hangs[so_ngau_nhien][4])
                        dem_sl += 1
                tam = so_ngau_nhien
                so_ngau_nhien = random.randint(0, sl_dh - 1)
            except Exception as ex:
                err_msg = str(ex)
                print(err_msg)
                so_ngau_nhien = random.randint(0, sl_dh - 1)
                print(so_ngau_nhien)

        print("Danh Sach Don Hang cua Shipper")
        print(ds_dhshipper)

    ds = SanLoc_DonHangChuaDuocGiao(id_shipper=dia_Chi.id, dsShipper=ds_dhshipper)
    print("-----")
    print(ds + chitiet_DH)
    print(len(ds))
    for i in range(len(ds) - 1):
        print("vao xoa dc")
        if ds[i].get('ma_vaDon') == ds[len(ds) - i - 1].get('ma_vaDon'):
            print("XOa dc")
            del (ds[i])
        if len(ds) - i == 0:
            break
    return ds


def SanLoc_DonHangChuaDuocGiao(id_shipper, dsShipper=None):
    print("Phan XU ly tt hang chua dc giao")
    print(dsShipper, id_shipper)
    if dsShipper is None:
        dsShipper = []
    lay_ttdh = dao.truyvan_DonHangDaUpdate(id_shipper=id_shipper)
    print("demo")
    print(lay_ttdh.all())
    sl = len(lay_ttdh.all())
    print(dsShipper)
    for i in range(sl):
        if not lay_ttdh[i][5]:
            layChiTietDonHang(id_HoaDon=lay_ttdh[i][4])
            dsShipper.append(
                {
                    'ma_vaDon': "VTDH" + str(lay_ttdh[i][4]),
                    'diaChiNha': lay_ttdh[i][0],
                    'hoten': lay_ttdh[i][1],
                    'sdt': lay_ttdh[i][2],
                    'tongtien': lay_ttdh[i][3],
                    'tinhTrang': 'Tra Tien Mat'

                }
            )
        else:
            dsShipper.append(
                {
                    'ma_vaDon': "VTTH" + str(lay_ttdh[i][4]),
                    'diaChiNha': lay_ttdh[i][0],
                    'hoten': lay_ttdh[i][1],
                    'sdt': lay_ttdh[i][2],
                    'tongtien': lay_ttdh[i][3],
                    'tinhTrang': 'Da Thanh Toan'
                }
            )

    return dsShipper


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            try:
                dao.add_user(
                    username=request.form.get('username'),
                    password=password, hoTen=request.form.get('name'))
                print("CHECK")
                print(request.form.get('name') + "OKE")
            except Exception as ex:
                err_msg = str(ex)
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'
    return render_template('register.html', err_msg=err_msg)


# Phần Bình luận sản phẩm
@app.route('/api/products/<id>/comments', methods=['post'])
def add_comment(id):
    try:
        c = dao.add_comment(product_id=id, content=request.json.get('content'))
    except Exception as ex:
        return jsonify({'status': 500, 'err_msg': str(ex)})
    else:
        return jsonify({'status': 200, 'comment': {
            'content': c.content,
            'created_date': c.created_date,
        }})


# Phần xử lý thông tin nhân viên đăng ký làm shipper
@app.route("/thongtintuyendungnhanvien", methods=['get', 'post'])
def xacThuc_nv():
    global check, dem
    print(check)
    check = True
    dem = 0
    print(dem)
    print(request.form.get("POST"))
    ht = request.form.get('name')
    print(ht)
    if ht:
        ht = request.form.get('name')
        gioiTinh = request.form.get('gioitinh')
        ngaySinh = request.form.get('ngaysinh')
        cccd = request.form.get('cccd')
        print(cccd)
        anhxacthuc = request.files.get('anhxacthuc')
        print(anhxacthuc)
        sdt = request.form.get('SDT')
        diaChiEmail = request.form.get('email')
        diaChiNha = request.form.get('diaChi')
        if gioiTinh.__eq__(1):
            dao.luu_thongtinNV(hoten=ht,
                               diaChi=diaChiNha, sdt=sdt, cccd=cccd, ngaySinh=ngaySinh,
                               gioiTinh='Nam', anhxacthuc=anhxacthuc, diaChiEmail=diaChiEmail)
            print('luu thanh cong gioi tinh Nam')
        else:
            dao.luu_thongtinNV(hoten=ht,
                               diaChi=diaChiNha, sdt=sdt, cccd=cccd, ngaySinh=ngaySinh,
                               gioiTinh='Nữ', anhxacthuc=anhxacthuc, diaChiEmail=diaChiEmail)
            print('luu thanh cong gioi tinh Nu')
        mss = 'Vui lòng check email trong vòng 24h kể từ ngày đăng ký'
        return render_template('indexShipper.html', mss=mss)
    else:
        return render_template("ThongTinNhanVien.html")


@app.route("/ship", methods=['get', 'post'])
def shipment():
    global check, dem
    check = True
    dem = 0

    return render_template('indexShipper.html')


@app.route("/api/xuly_donhang", methods=['post'])
def xuLy_DonHang():
    print("Xu ly don hang da hoan thanh")
    data = request.json
    print(data)
    update_DonHang = dao.update_DonHang(id=int(data.get('id')))
    print(update_DonHang)


# Phan xu ly lich su don hang cuas shipper
@app.route("/lichsudonhang", methods=["get"])
def xuLy_LichSuDonHang():
    lay_donHang = dao.updonhangshipper(id_Shipper=session.get('id_tk'))
    print("Lich Su Don Hang Shipper")
    print(lay_donHang.all())
    sl = len(lay_donHang.all())
    return render_template('ThongTinNhanVien.html', sl=sl, lay_donHang=lay_donHang)


if __name__ == "__main__":
    app.run(debug=True)

from app.models import  DanhMuc,SanPham
def load_cat():
    return DanhMuc.query.all()
def load_Product(kw=None):
    product=SanPham.query
    if kw:
        product=product.filter(SanPham.name.contains(kw))
    return product.all()
def load_cat():
    return[{
        "name": 'mobile',
        "ma": "101"
    },
        {
            "name": 'iphone',
            "ma": "102"
        },
        {
            "name": 'thoat',
            "ma": "102"
        }
    ]
def load_Product(kw=None):
    product= [
        {"name": 'sam sung galaxy',
         "ma": "105",
         "price": "10000",
         "img": "https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg"

         },
        {"name": 'sam sung galaxy',
         "ma": "106",
         "price": "10000",
         "img": "https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg"

         },
        {"name": 'sam sung galaxy',
         "ma": "107",
         "price": "20000",
         "img": "https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg"

         },
        {"name": 'sam sung galaxy',
         "ma": "108",
         "price": "30000",
         "img": "https://cdn.tgdd.vn/Products/Images/42/274018/samsung-galaxy-a24-black-thumb-600x600.jpg"

         }

    ]
    if kw:
      product=[p for p in product if p["name"].find(kw)>=0]
    return product
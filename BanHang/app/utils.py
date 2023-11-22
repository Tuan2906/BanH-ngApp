def count_cart(cart):
    tong_sl, tongten =0,0
    for c in cart.value():
        tong_sl+=c['quanity']
        tongten= c['quanity']*c['price']

    return {

            'total_amount': tongten,
            'toal_quanity': tong_sl
    }
function add_to_cart(name,price,quanity)
{
  fetch('/api/cart',
  {
    method: 'post',
    body: JSON.stringify({
     'id':id,
     'name':name,
     'price':price
    }),
    header:{
      'Content=Type':'application/json'
    }
  }).then(function(res))
  {
     return res.json():

  }).then(function(data))
  {
    console.info(data)
    let items=document.getElementByClassName('cart-counter');
    for(let item of items)
     {
       item.innerText=toal_quanity
     }
  });
}
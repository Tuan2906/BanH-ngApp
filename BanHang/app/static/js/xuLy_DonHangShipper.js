function lay_idDonHang(button)
{
  const row = button.closest('tr'); // Get the closest table row
  layid=row.children[0]
  const ma_vaDon = layid.textContent
 var layma  = ma_vaDon.charAt(4);
var j=5;
 while(j < ma_vaDon.length)
 {
       if (ma_vaDon.charAt(j) >=0)
      {
          layma+=ma_vaDon.charAt(j);
          j++;
      }
 }
   fetch("/api/xuly_donhang", {
            method: "post",
            body: JSON.stringify({
               "id":  layma
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
                console.log(data)
        });
   button.disabled = true;


}
const addressLink = document.getElementById('address-link');
const mapContainer = document.getElementById('map-container');


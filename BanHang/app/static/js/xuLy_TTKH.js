var flag_sdt=true
    function check_TT() {
    // Nếu dữ liệu hợp lệ, thì cho phép gửi biểu mẫu
    if (flag_sdt==true) {
      return true;
     } else {
       alert("Vui lòng kiểm tra lại thông tin nãy thông báo trước và sửa lại")
       event.preventDefault();
      return false;
    }

 }
function checkSDT(obj)
{
  var so = /^[0-9]+$/
   if(obj.value.length <10)
   {
     alert("Vui lòng nhập SĐT đủ 10 số ")
       flag_sdt=false
   }
   else if(obj.value.length > 11)
   {
      alert("Vui lòng kiểm tra lại SĐT")
      flag_sdt= false
   }
   else if(so.test(obj.value)==false)
   {
      alert("Vui lòng kiểm tra lại SĐT không phải là chữ")
      flag_sdt= false
   }
   else
   {
    flag_sdt=true
   }
}
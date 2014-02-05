function submitAddress(){
  var name = $("#full-name").val();
  var address_line1 = $("#address-line1").val();
  var address_line2 = $("#address-line2").val();
  var city = $("#city").val();
  var region = $("#region").val();
  var postal_code = $("#postal-code").val();
  var country = $("#country").val();
  $.post('/submit',
    {
      name:name,
      address_line1:address_line1,
      address_line2:address_line2,
      city:city,
      region:region,
      postal_code:postal_code,
      country:country
    },
    function(data){
      console.log(data)
      $("#status").html(data);
    }
  );
}

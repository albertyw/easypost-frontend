function submitAddress(){
  var name = $("#full-name").val();
  var address_line1 = $("#address-line1").val();
  var address_line2 = $("#address-line2").val();
  var city = $("#city").val();
  var region = $("#region").val();
  var postal_code = $("#postal-code").val();
  var country = $("#country").val();
  var length = $("#length").val();
  var width = $("#width").val();
  var height = $("#height").val();
  var weight = $("#weight").val();
  $.post('/submit',
    {
      name:name,
      address_line1:address_line1,
      address_line2:address_line2,
      city:city,
      region:region,
      postal_code:postal_code,
      country:country,
      length:length,
      width:width,
      height:height,
      weight:weight
    },
    function(data){
      console.log(data)
      $("#status").html(data);
    }
  );
}

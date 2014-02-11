function submitAddress(){
  $("#submitButton").hide();
  $("#submitButtonLoading").show();
  var name = $("#full-name").val();
  var address_line1 = $("#address-line1").val();
  var address_line2 = $("#address-line2").val();
  var city = $("#city").val();
  var region = $("#region").val();
  var postal_code = $("#postal-code").val();
  var country = $("#country").val();
  var phone = $("#phone").val();
  var length = $("#length").val();
  var width = $("#width").val();
  var height = $("#height").val();
  var weight = $("#weight").val();
  var dry_ice = $("#dry-ice").val();
  $.ajax({
    type:'POST',
    url:'/submit',
    data:{
      name:name,
      address_line1:address_line1,
      address_line2:address_line2,
      city:city,
      region:region,
      postal_code:postal_code,
      country:country,
      phone:phone,
      length:length,
      width:width,
      height:height,
      weight:weight,
      dry_ice:dry_ice
    },
    success:function(data){
      if(data['status'] == 'error'){
        showMessage(data['message'], data['status']);
      }else if(data['status'] == 'success'){
        text = 'New label created.  ';
        text = 'Tracking Code: '+data['message']['tracking_code']+' ';
        text += '<a href="'+data['message']['label_url']+'">Get Label</a>';
        showMessage(text, data['status']);
      }
    },
    error:function(){
      showMessage('Unknown Error');
    },
    dataType:'json'
  });
  return false;
}
function showMessage(message, status){
  if(status == 'error'){
    $("#status").addClass('alert-danger');
    $("#status").removeClass('alert-success');
  }else if(status == 'success'){
    $("#status").addClass('alert-success');
    $("#status").removeClass('alert-danger');
  }
  $("#status").html(message);
  $("#status").show('slow');
  $("#submitButton").show();
  $("#submitButtonLoading").hide();
}

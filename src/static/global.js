// Event handler for when a person submits the form
function submitAddress(){
  $("#submitButton").hide();
  $("#submitButtonLoading").show();
  data = {};
  $("input[type!='submit']").each(function(index, input){
      data[input.id] = input.value
  });
  data['country'] = $("#country").val();
  $.ajax({
    type:'POST',
    url:'/submit',
    data:data,
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

// Handler for showing a message from an ajax call to the server
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

// Populate the form with example data
function fillExampleData(){
  $("#name").val('Albert Wang');
  $("#company").val('Test Company');
  $("#street1").val('440 Davis Ct');
  $("#street2").val('Apartment 919');
  $("#city").val('San Francisco');
  $("#state").val('California');
  $("#zip").val('94111');
  $("#country").val('US');
  $("#phone").val('617-575-9658');
  $("#print_custom_1").val('Test custom line 1');
  $("#length").val('4');
  $("#width").val('5');
  $("#height").val('6');
  $("#weight").val('8');
  $("#dry_ice_weight").val('2');
}

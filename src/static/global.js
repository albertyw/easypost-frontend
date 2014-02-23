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

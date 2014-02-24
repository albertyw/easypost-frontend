/**
 * Form Handlers
 **/

// Event handler for when the address form is submitted
function submitAddress(){
  startLoading();
  data = {};
  $("input[type!='submit']").each(function(index, input){
      data[input.id] = input.value
  });
  data['country'] = $("#country").val();
  ajaxAddress(data);
  return false;
}

// Handler for when the csv form is submitted
function readCsvForm(){
  // Check for the various File API support.
  if (!window.File || !window.FileReader) {
    alert('Your browser does not support reading files using javascript');
    return false;
  }
  startLoading();
  var address_file = $("#address_csv")[0].files[0];
  var address_reader = new FileReader();
  address_reader.onload = function(e) {
    var address_contents = e.target.result;
    var shipment_file = $("#shipment_csv")[0].files[0];
    var shipment_reader = new FileReader();
    shipment_reader.onload = function(e) {
      var shipment_contents = e.target.result;
      processCsvData(address_contents, shipment_contents);
    }
    shipment_reader.readAsText(shipment_file);
  }
  address_reader.readAsText(address_file);

  return false;
}


/**
 * Data processing and pushing
 **/

function processCsvData(address_contents, shipment_contents){
  //address_contents = 'Customer Org,Ship Name (Attn:),Address 1,Address 2,City,ST,ZIP,Phone,Email@email.com'
  //shipment_contents = '2/12/2014,Shipment #,Customer Org,Length,Width,Height,Weight,Ice Weight,PO#'
  address_contents = address_contents.split(',');
  shipment_contents = shipment_contents.split(',');
  data = {};
  data.name = address_contents[1];
  data.company = address_contents[0];
  data.street1 = address_contents[2];
  data.street2 = address_contents[3];
  data.city = address_contents[4];
  data.state = address_contents[5];
  data.zip = address_contents[6];
  data.country = 'US'
  data.phone = address_contents[7];
  data.print_custom_1 = shipment_contents[8].trim();
  data.length = shipment_contents[3];
  data.width = shipment_contents[4];
  data.height = shipment_contents[5];
  data.weight = shipment_contents[6];
  data.dry_ice_weight = shipment_contents[7];
  ajaxAddress(data);
  stopLoading();
}

// Function to send data to server using ajax
function ajaxAddress(data){
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
}


/**
 * UI
 **/

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
  stopLoading();
}

// Turn the submit button into loading image
function startLoading(){
  $("#submitButton").hide();
  $("#submitButtonLoading").show();
}

// Turn the loading image back into a submit button
function stopLoading(){
  $("#submitButton").show();
  $("#submitButtonLoading").hide();
}


/**
 * Utils
 **/

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

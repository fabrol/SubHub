$(document).ready(function() {
  //get the current user asynchronously
  var myUser;
  $.ajax({
    dataType: "json",
    url: 'getuser',
    async: false,
    success: function(data){
      myUser = data.email_address;
    }
  });

  //Add the tabs
  $( "#tabs" ).tabs();

  //create the grid elements
  for (var i = 7; i < 24; i++){
    var selector = "<div class='hourItem time"+i+"'></div>";
    $("#grid").append(selector);
    var selector = "<div class='hourItem time"+i+"30'></div>";
    $("#grid").append(selector);
  }

  $('#datepicker').datepicker({
    showOtherMonths:true,
    selectOtherMonths:true,
    onSelect: function() {

  var curUser;
  $.ajax({
    dataType: "json",
    url: 'getuser',
    async: false,
    success: function(data){
      curUser = data.email_address;
    }
  });

  var entered = $('#datepicker').datepicker("getDate");
  var date = new Date(entered);
  var month = date.getMonth();
  var day = date.getDate();
  var year = date.getFullYear();
  $.ajax({
    type:"POST",
    url:"/getshifts",
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({'month':month,'day':day, 'year':year}),
    dataType: "json",
    async: false,
    success: function(response) {
      $('.shift').remove();
      console.log("response is ");
    //parse all the shifts to their locations
    renderShifts(response,curUser);

  }
});
  $('#datepicker').datepicker("hide");

    },
    dateformat: 'yy-mm-dd'
  });

//Check for date in the url
var vars = [], hash;
decoded = decodeURI(document.URL);
var q = decoded.split('?')[1];
if(q != undefined){
  hash = q.split('=');
  vars.push(hash[1]);
}

//get all the shifts and render
$.ajax({
  type :"POST",
  dataType: "json",
  url: 'getshifts',
  async: false,
  data: vars[0],
  success: function(data){
    renderShifts(data,myUser);
  }
});

//popoulate the datepicker with the correct date
if (vars.length != 0){
  params = $.parseJSON(vars[0]);
  $('#datepicker').datepicker("setDate",new Date(params['year'],params['month'],params['day']));
}
else{
  $('#datepicker').datepicker("setDate",new Date());
}
});

//parses duration of shift to height
var duration_to_height = function (duration){
  return (duration * (17.45) / 30.0);
};


//Render all the shifts in data
var renderShifts = function(data, myUser){

  $.each(data.shifts, function(index, shift){
    var user = shift.user;
    var sub = shift.sub;
    var status = shift.status;
    var duration = shift.duration;
    var datetime = new Date(Date.parse(shift.datetime));
    var endtime = new Date(Date.parse(shift.endtime));

    var day = datetime.getDay();
    var day_text;
    switch(day){
      case 0: day_text = "Sun";break;
      case 1: day_text = "Mon";break;
      case 2: day_text = "Tue";break;
      case 3: day_text = "Wed";break;
      case 4: day_text = "Thu";break;
      case 5: day_text = "Fri";break;
      case 6: day_text = "Sat";break;
    }
    var hour = datetime.getHours() + 4;
    var min = datetime.getMinutes();
    var endhour = endtime.getHours() + 4;
    var endmin = endtime.getMinutes();

    if (parseInt(min) == 30) {
      var select = "div.shift." + status + "." + day_text + ".time"+ hour+"30"
      if (parseInt(duration) <= 30) {
        var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "30\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":"+min+ "-"+ endhour + ":" + endmin +"</div>";
      }
      else if (parseInt(duration) > 30 && parseInt(duration) <= 60) {
        var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "30\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":"+min+ "-"+ endhour + ":" + endmin +"<br>"+ user.name+"</div>";
      }
      else {
        var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "30\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":"+min+ "-"+ endhour + ":" + endmin +"<br>"+ user.name+ "<br>"+ "<span style='color:white'> Sub:" + sub.name+ "</span></div>";
      }
    }
    else {
      var select = "div.shift." + status + "." + day_text + ".time"+ hour
      if (parseInt(duration) <= 30) {
        var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":00-"+endhour+":00</div>";
      }
      else if (parseInt(duration) > 30 && parseInt(duration) <= 60) {
        var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":00-"+endhour+":00<br>"+ user.name+"</div>";
      }
      else {
        var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":00-"+endhour+":00<br>"+ user.name+ "<br>"+ "<span style='color:white'> Sub:" + sub.name+ "</span></div>";
      }

    }
      //Add the My Shifts tab
      $("#grid").append(selector);        
      if ((user.email_address == myUser) || (sub.email_address == myUser)){
        $("#timeTable-2").append(selector)
      }
      
      //Create popup dialogs for shifts

      var createDialog = false;

      console.log(myUser);
      //access to asking for sub only if your own shift
      if ((status == 'normal') && (user.email_address == myUser)) {
        createDialog = true;
        var $dialog = $('<div></div>')
        .html('You can ask for a sub here!')
        .dialog({
          autoOpen: false,
          modal: true,
          title: 'Normal Shift',
          buttons: {
            "Request Sub": function() {
                //send request to server
                var that = $(this);
                $.ajax({
                  type:"POST",
                  url:"/requestsub",
                  contentType: 'application/json; charset=utf-8',
                  data: JSON.stringify({'user':myUser,'shift':shift}),
                  dataType: "json",
                  context: that,
                  async: false,
                  success: function(response,text) {
                    alert ("Request for sub sent");
                    $( this ).dialog( "close" );

                    var date = new Date($('#datepicker').datepicker("getDate"));
                    var month = date.getMonth();
                    var day = date.getDate();
                    var year = date.getFullYear();
                    var curChosen = JSON.stringify({'month':month,'day':day, 'year':year});
                    window.location.replace(location.protocol + '//' + location.host + location.pathname + "?cur_date_chosen="+curChosen);
}
});
              }
            }
          });
}
else if (status == 'open') { 
  createDialog = true;        
  var $dialog = $('<div></div>')
  .html('Do you want to cover this shift?')
  .dialog({
    autoOpen: false,
    modal: true,
    title: 'Open Shift',
    buttons: {
      "Cover Shift": function() {
                //send request to server
                var that = $(this);
                $.ajax({
                  type:"POST",
                  url:"/claimsub",
                  contentType: 'application/json; charset=utf-8',
                  data: JSON.stringify({'user':myUser,'shift':shift}),
                  dataType: "json",
                  async: false,
                  context: that,
                  success: function(data) {
                    var result = jQuery.parseJSON(data)
                    if (result.gotshift == 'true'){
                      alert("Congrats! You got the shift!");
                    }
                    else{
                      alert ("Sorry! Some already claimed the shift!");                                          
                    }
                    $( this ).dialog( "close" );


                    var date = new Date($('#datepicker').datepicker("getDate"));
                    var month = date.getMonth();
                    var day = date.getDate();
                    var year = date.getFullYear();
                    var curChosen = JSON.stringify({'month':month,'day':day, 'year':year});
                    window.location.replace(location.protocol + '//' + location.host + location.pathname + "?cur_date_chosen="+curChosen);

                  }
                });
}
}
});
}
else if (status == 'closed') {
  if (sub.email_address == myUser){
          //Sub asking for Sub
          createDialog = true;
          var $dialog = $('<div></div>')
          .html('Do you no longer want to cover this shift?')
          .dialog({
            autoOpen: false,
            modal: true,
            title: "Ask for new Sub!",
            buttons: {
              "Ask for a new Sub": function(){
                //send request to server
                var that = $(this);
                $.ajax({
                  type:"POST",
                  url:"/requestsfsub",
                  contentType: 'application/json; charset=utf-8',
                  data: JSON.stringify({'sub_user':myUser,'shift':shift}),
                  dataType: "json",
                  context: that,
                  async: false,
                  success: function(response,text) {
                    alert ("Request for new sub sent!");
                    $( this ).dialog( "close" );


                    var date = new Date($('#datepicker').datepicker("getDate"));
                    var month = date.getMonth();
                    var day = date.getDate();
                    var year = date.getFullYear();
                    var curChosen = JSON.stringify({'month':month,'day':day, 'year':year});
                    window.location.replace(location.protocol + '//' + location.host + location.pathname + "?cur_date_chosen="+curChosen);


                  }
                });              
              },
              Cancel: function() {
                $(this).dialog("close");
              }
            }
          });
} 
else{  
  createDialog = true;
  var $dialog = $('<div></div>')
  .html('This shift has been covered')
  .dialog({
    autoOpen: false,
    modal: true,
    title: 'Closed Shift',
    buttons: {

      Cancel: function() {
        $(this).dialog("close");
      }
    }
  });
}
}

if (createDialog == true)
  {        $(select).click(function(){
    $.powerTip.hide();
    $dialog.dialog("open");
  });
}
$(select).powerTip({
  mouseOnToPopup: true,
  fadeOutTime:5,
  placement:'e'
});
$(select).data('powertip',function(){

  return user.name +' ' + user.last_name+' <br>Sub: ' + sub.name + '<br>Hours: ' + hour + ':'+ min + '-' + endhour + ':' + endmin + '<br>Status: ' + status;
});
});


};
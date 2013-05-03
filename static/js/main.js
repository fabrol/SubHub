$(document).ready(function() {
  var myUser;
  $.getJSON('getuser', function(data){
    myUser = data.email_address
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

  $.getJSON('getshifts', function(data){
    $.each(data.shifts, function(index, shift){
      var user = shift.user;
      var sub = shift.sub;
      var status = shift.status;
      var duration = shift.duration;

      var datetime = new Date(Date.parse(shift.datetime));
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

      if (parseInt(min) == 30) {
        var select = "div.shift." + status + "." + day_text + ".time"+ hour+"30"
        console.log(select);
        if (parseInt(duration) <= 30) {
          var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "30\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":"+min+"</div>";
        }
        else if (parseInt(duration) > 30 && parseInt(duration) <= 60) {
          var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "30\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + "<br>"+ user.name+"</div>";
        }
        else {
          var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "30\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + "<br>"+ user.name+ "<br>"+ "<span style='color:white'> Sub:" + sub.name+ "</span></div>";
        }
      }
      else {
        var select = "div.shift." + status + "." + day_text + ".time"+ hour
        console.log(select);
        if (parseInt(duration) <= 30) {
          var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":00</div>";
        }
        else if (parseInt(duration) > 30 && parseInt(duration) <= 60) {
          var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":00<br>"+ user.name+"</div>";
        }
        else {
          var selector = "<div id='shift' class=\'shift " + status + " " + day_text + " time"+ hour + "\' style='height: " + duration_to_height(duration) + "px;\'>"+hour + ":00<br>"+ user.name+ "<br>"+ "<span style='color:white'> Sub:" + sub.name+ "</span></div>";
        }

      }
      $("#grid").append(selector);        
      if (user.email_address == myUser){
        $("#timeTable-2").append(selector)
      }
      
      if (status == 'normal') { 
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
                    console.log("CAME BACK");
                    alert ("Request for sub sent");
                     $( this ).dialog( "close" );
                     window.location.reload(true);
                  }
                });
              }
            }
          });
      }
      if (status == 'open') { 
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
                    window.location.reload(true);
                  }
                });
              }
            }
          });
      }
      if (status == 'closed') { 
        var $dialog = $('<div></div>')
          .html('This shift has been covered')
          .dialog({
            autoOpen: false,
            modal: true,
            title: 'Closed Shift',
            var that = $(this);
            buttons: {
              Cancel: function() {
                $(this).dialog("close");
              }
            }
          });
      }
        $(select).click(function(){
          $.powerTip.hide();
          $dialog.dialog("open");
          });

      $(select).powerTip({
        mouseOnToPopup: true,
        fadeOutTime:5,
        placement:'e'
      });
      console.log(user);
      $(select).data('powertip',function(){

        return user.name +' ' + user.last_name+' <br>Sub: ' + sub.name + '<br>Hours: ' + hour + ':'+ min + '<br>Status: ' + status;
      });
    });
});

});

var duration_to_height = function (duration){
  return (duration * (17.45) / 30.0);
};


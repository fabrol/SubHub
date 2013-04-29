$(document).ready(function() {

  //Add the tooltips to the shifts
    $("#RequestShift,#NormalShift,#CoveredShift").powerTip({
				mouseOnToPopup: true,
				smartPlacement:true,
				fadeOutTime:5
			});
	$("#RequestShift,#NormalShift,#CoveredShift").data('powertip',function(){
		return this.id;
	});

  //Add the tabs
    // $( "#tabPanel" ).tabs();
    // $("#timeTable-1").css('.timeTable');

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
        var duration = shift.duration*18;
              
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
        var hour = datetime.getHours();
        console.log(day_text)
        var selector = "<div class=\'shift " + status + " " + day_text + " time"+ hour + "\' style='height: " + duration + "px;\'>"+status+"</div>";
        $("#grid").append(selector);
      });
  });

});
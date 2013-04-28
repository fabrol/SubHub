console.log("haha");
$(document).ready(function() {
	console.log("haha");


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
console.log("haha");


  $.getJSON('getshifts', function(data){
  		for (var shift in data.shifts) {
  			var user = shift.user;
  			var sub = shift.sub;
  			var status = shift.status;
  			var duration = shift.duration*18;
              
  			var datetime = new Date(Date.parse(shift.datetime));
            var day = datetime.getDay();
            var day_text;
            switch(day){
                case 0: day_text = "SUN";break;
                case 1: day_text = "MON";break;
                case 2: day_text = "TUE";break;
                case 3: day_text = "WED";break;
                case 4: day_text = "THU";break;
                case 5: day_text = "FRI";break;
                case 6: day_text = "SAT";break;
            }
            var hour = datetime.getHours();
  			var selector = "<div class='" + day + " time"+ hour + " style='height: " + duration + "px;'></div>";
			$("#grid").append(selector);
  		}
    	
  });
});
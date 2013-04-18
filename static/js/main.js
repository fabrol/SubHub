$(document).ready(function() {
	$("#RequestShift,#NormalShift,#CoveredShift").powerTip({
				mouseOnToPopup: true,
				smartPlacement:true,
				fadeOutTime:5
			});
	$("#RequestShift,#NormalShift,#CoveredShift").data('powertip',function(){
		return this.id;
	});
    $( "#tabPanel" ).tabs();
    $("#timeTable-1").css('.timeTable');
	for (var i = 7; i < 12; i++){
		var selector = "<div class='hourItem time"+i+"AM'></div>";
		$("#grid").append(selector);
		var selector = "<div class='hourItem time"+i+"30AM'></div>";
		$("#grid").append(selector);
	}	
	var selector = "<div class='hourItem time12PM'></div>";
	$("#grid").append(selector);
	var selector = "<div class='hourItem time1230PM'></div>";
	$("#grid").append(selector);
	for (var i = 1; i < 12; i++){
		var selector = "<div class='hourItem time"+i+"PM'></div>";
		$("#grid").append(selector);
		var selector = "<div class='hourItem time"+i+"30PM'></div>";
		$("#grid").append(selector);
	}
	var selector = "<div class='hourItem time12AM'></div>";
	$("#grid").append(selector);
	var selector = "<div class='hourItem time1230AM'></div>";
	$("#grid").append(selector);
});

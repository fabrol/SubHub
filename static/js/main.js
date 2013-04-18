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
		var selector = "<div id='"+i+"AM' class='"+i+"AM'></div>";
		$("#grid").append(selector);
	}
});

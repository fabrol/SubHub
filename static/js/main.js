$(document).ready(function() {
	$("#RequestShift,#NormalShift,#CoveredShift").powerTip({
				mouseOnToPopup: true,
				smartPlacement:true,
				fadeOutTime:5
			});
	$("#RequestShift,#NormalShift,#CoveredShift").data('powertip',function(){
		return this.id;
	});
});
$(function() {
    $( "#tabPanel" ).tabs();
    $("#timeTable-1").css('.timeTable');
  });

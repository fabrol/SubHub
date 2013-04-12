$(document).ready(function() {
	$("#NormalShift,#RequestShift,#CoveredShift").each(
		function() {
			var openTip = new Opentip(this, {hideDelay:0.0});
			openTip.setContent(this.id)
		});
});
$(function() {
    $( "#tabPanel" ).tabs();
    $("#timeTable-1").css('.timeTable');
  });
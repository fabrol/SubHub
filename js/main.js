$(document).ready(function() {
<<<<<<< HEAD
	$("#RequestShift,#NormalShift,#CoveredShift").powerTip({
				mouseOnToPopup: true,
				smartPlacement:true,
				fadeOutTime:5
			});
	$("#RequestShift,#NormalShift,#CoveredShift").data('powertip',function(){
		return this.id;
	});
});
=======
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
>>>>>>> 0ad65cf27124e7c5adb19456312879c87b275d0b

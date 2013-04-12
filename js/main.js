$(document).ready(function() {
	$("#NormalShift,#RequestShift,#CoveredShift").each(
		function() {
			var openTip = new Opentip(this, {hideDelay:0.0});
			openTip.setContent(this.id)
		});
});
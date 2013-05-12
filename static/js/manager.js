$(document).ready(function() {
  //get the current user asynchronously
 
$.ajax({
  type :"POST",
  dataType: "json",
  url: 'getmanagershifts',
  async: false,
  success: function(data){
    render(data);
  }
})
});

var render = function(data){
  for (user in data){
    if (data.hasOwnProperty(user)){
      var insert = "<tr>" + 
                  "<td>" + user  + "</td>" +
                  "<td >" + data[user]['reg_shifts']  + "</td>" +
                  "<td style='background-color:#99FF99;'>" + data[user]['asked_sub_shifts']  + "</td>" +
                  "<td style='background-color:#FF9494;'>" + data[user]['subbing']  + "</td>" +
                  "</tr>"
      $("tbody").append(insert);
      console.log(user);
    }
  }

};
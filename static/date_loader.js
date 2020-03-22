$(document).ready(function() {
  $.get("/date_loader_directional", function(data)
  {
    $("#datepicker").val(data.date_data);
    chart_fn();
  })
  $("#datepicker,:radio").change(function() {
    chart_fn();
  })
})

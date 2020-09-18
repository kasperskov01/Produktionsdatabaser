$("document").ready(function () {
  $("#send").click(function () {
    var message = $("#message").val();
    $.ajax({
      url: "http://127.0.0.1:5000/api/",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ message: message }),
    }).done(function (data) {
      console.log(data);
    });
  });
});

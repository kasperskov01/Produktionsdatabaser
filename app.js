function ajax_request(url_path, data) {
  $.ajax({
    url: "http://127.0.0.1:5000/api" + url_path,
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(data),
    timeout: 2000,
  })
    .done(function (data) {
      return data;
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.log(errorThrown);
      return false;
    });
}

function check_form_login() {
  let valid = true;
  $(".form-field").each(function () {
    if ($(this).val() === "") {
      valid = false;
      return false;
    }
  });
  if (valid) {
    console.log("Valid");
    let username = $("#username").val();
    let password = $("#password").val();
    let data = ajax_request("/login", {
      username: username,
      password: password,
    });
    if (!data) {
      console.log("API ikke tilgængelig");
    } else {
      console.log(data);
    }
  } else {
    console.log("Invalid");
  }
  return false;
}

function check_form_signup() {
  let valid = true;
  $(".form-field").each(function () {
    if ($(this).val() === "") {
      valid = false;
      return false;
    }
  });
  if (valid) {
    console.log("Valid");
    let username = $("#username").val();
    let password = $("#password").val();
    let type = $("#usertype").val();    
    let data = ajax_request("/login", {
      username: username,
      password: password,
      type: type
    });    
    if (!data) {
      console.log("API ikke tilgængelig");
    } else {
      console.log(data);
    }
  } else {
    console.log("Invalid");
  }
  return false;
}

async function ajax_request(url_path, data) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: "http://127.0.0.1:5000/api" + url_path,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      timeout: 2000,
    })
      .done(function (data) {
        resolve(data);
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
        reject();
      });
  });
}

function is_valid() {
  let valid = true;
  $(".form-field").each(function () {
    if ($(this).val() === "") {
      valid = false;
    }
  });
  if (!valid) {
    alert("Venligst udfyld alle felter.")
  } else {
    console.log("Form valid")
  }
  return valid
}

async function isLoggedIn() {
  const token = localStorage.getItem("logged_in");
  if (token == "true") {
    console.log("true");
    return true;
  }
  return false;
}

async function logout() {
  localStorage.setItem("logged_in", false);
  localStorage.setItem("username", undefined);
  localStorage.setItem("user_type", undefined);
  location.replace("/login.html");
}

async function autoRedirect() {
  const validLogin = await isLoggedIn();
  if (
    !validLogin &&
    location.pathname !== "/login.html" &&
    location.pathname !== "/signup.html"
  )
    location.replace("/login.html");
  if (
    validLogin &&
    (location.pathname === "/login.html" ||
      location.pathname === "/signup.html")
  )
    location.replace("/create-order.html");
}

function login(username, password) {
  ajax_request("/user/login", {
    username: username,
    password: password,
  }).then((data) => {
    console.log(data);
    if (data["logged_in"] == true) {
      localStorage.setItem("logged_in", data["logged_in"]);
      localStorage.setItem("username", data["username"]);
      localStorage.setItem("user_type", data["user_type"]);
    } else {
      console.log("Login failed");
      return "login_failed";
    }

    autoRedirect();
  });
}

function check_form_login() {
  if (is_valid()) {
    let username = $("#username").val();
    let password = $("#password").val();
    if (login(username, password) == "login_failed") {
      alert("Bad username/password");
    }
  }
  return false;
}

function check_form_signup() {
  if (is_valid()) {
    let username = $("#username").val();
    let password = $("#password").val();
    let user_type = $("#user_type").val();
    ajax_request("/user/signup", {
      username: username,
      password: password,
      user_type: user_type,
    }).then((data) => {
      console.log(data);
      if (data["user_created"] == true) {
        login(username, password);
      } else if (data["user_exists"] == true) {
        alert("User already exists")
      } else { 
        alert("User could not be created")
      }
    });
  }
  return false;
}

$("#logout").click(function () {
  event.preventDefault();
  logout();
});

// function create_order() {
//   let valid = is_valid() 
  
//   if (valid) {
//     let brick1 = $("#brick1").val();
//     let brick2 = $("#brick2").val();
//     let brick3 = $("#brick3").val();
//     let data = ajax_request("/login", {
//       username: username,
//       password: password,
//       type: type
//     });
//     let data = {};
//     if (!data) {
//       console.log("API ikke tilgængelig");
//     } else {
//       console.log(data);
//     }
//   } else {
//     console.log("Invalid");
//   }
//   return false;
// }

autoRedirect();

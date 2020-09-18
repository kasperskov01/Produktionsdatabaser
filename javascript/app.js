let is_dev = true

let ajax_url = "https://proddb.herokuapp.com/api"
if (is_dev) {
  ajax_url = "http://127.0.0.1:5000/api"
}


async function ajax_request(url_path, data) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: ajax_url + url_path,
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
    alert("Venligst udfyld alle felter.");
  }
  return valid;
}

async function isLoggedIn() {
  const token = localStorage.getItem("logged_in");
  if (token == "true") {
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
    location.replace("/home.html");
}

function login(username, password) {
  ajax_request("/user/login", {
    username: username,
    password: password,
  })
    .then((data) => {
      if (data["logged_in"] == true) {
        localStorage.setItem("logged_in", data["logged_in"]);
        localStorage.setItem("username", data["username"]);
        localStorage.setItem("user_type", data["user_type"]);
      } else {
        alert("Ugyldigt brugernavn / adgangskode");
        return "login_failed";
      }
      autoRedirect();
    })
    .catch((error) => {
      console.log(error);
      alert("Der kunne ikke oprettes forbindelse");
    });
}

function check_form_login() {
  if (is_valid()) {
    let username = $("#username").val();
    let password = $("#password").val();
    login(username, password);
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
    })
      .then((data) => {
        console.log(data);
        if (data["user_created"] == true) {
          login(username, password);
        } else if (data["user_exists"] == true) {
          alert("Brugeren eksisterer allerede");
        } else {
          alert("Brugeren kunne ikke oprettes");
        }
      })
      .catch((error) => {
        console.log(error);
        alert("Der kunne ikke oprettes forbindelse");
      });
  }
  return false;
}

$("#logout").click(function () {
  event.preventDefault();
  logout();
});

function create_order() {
  let valid = is_valid();
  if (valid) {
    let brick1 = $("#brick1").val();
    let brick2 = $("#brick2").val();
    let brick3 = $("#brick3").val();
    console.log(brick1)
    ajax_request("/order/new", {
      username: localStorage.getItem("username"),
      product: [brick1, brick2, brick3],
    })
      .then((data) => {
        console.log(data);
        if (data["order_created"] == true) {
          console.log("Ordre oprettet");
        } else {
          alert("Ordren kunne ikke oprettes");
        }
      })
      .catch((error) => {
        console.log(error);
        alert("Der kunne ikke oprettes forbindelse");
      });
  }
  return false;
}



function load_table_orders(items) {
  console.log(items)
  const table = document.getElementById("my-orders");
  items.forEach((item) => {
    let row = table.insertRow();

    let ordre_id = row.insertCell(0);
    ordre_id.innerHTML = item["order_id"];

    let status = row.insertCell(1);
    status.innerHTML = item["status"];

    let vare = row.insertCell(2);
    vare.classList.add("product-cell")
    let product = JSON.parse(item["vare"])
    product.forEach((brick_color) => {
      var brick = document.createElement("div"); 
      brick.classList.add("brick")
      brick.style.backgroundColor = brick_color;
      brick.style.backgroundImage = "url(assets/brick_inverted.png)"
      // brick.style.backgroundRepeat = "no-repeat";
      // brick.style.backgroundPosition = "center top";

      vare.appendChild(brick)
    })    

    let bestillingsdato = row.insertCell(3);
    bestillingsdato.innerHTML = item["order_date"];
  });
}

function populate_table() {
  console.log("populate_table")
  // load_table_orders([{order_id: "1", status: "ok", vare: "Rød, Grøn, Blå", order_date: "8. september 2020"},
  // {order_id: "2", status: "ok", vare: "Rød, Grøn, Blå", order_date: "8. september 2020"},
  // {order_id: "3", status: "ok", vare: "Rød, Grøn, Blå", order_date: "8. september 2020"}])
  ajax_request("/order/get", {
    username: localStorage.getItem("username"),
  })
    .then((data) => {
      console.log(data);
      if (data["orders"] != undefined) {
        console.log("Ordrer hentet");
        load_table_orders(data["orders"])
      } else {
        console.log("Ordrerne kunne ikke hentes");
      }
    })
    .catch((error) => {
      console.log(error);
      console.log("Der kunne ikke oprettes forbindelse");
    });
};

$( document ).ready(function() {
  populate_table()

  let brick = document.getElementById("brick1-color")
  brick.style.backgroundColor = $("#brick1").val();
  brick.style.backgroundImage = "url(assets/brick_inverted.png)"

  let brick2 = document.getElementById("brick2-color")
  brick2.style.backgroundColor = $("#brick2").val();
  brick2.style.backgroundImage = "url(assets/brick_inverted.png)"

  let brick3 = document.getElementById("brick3-color")
  brick3.style.backgroundColor = $("#brick3").val();
  brick3.style.backgroundImage = "url(assets/brick_inverted.png)"

  // document.getElementById("brick2-color").style.backgroundColor = $("#brick2").val();
  // document.getElementById("brick3-color").style.backgroundColor = $("#brick3").val();
  // brick.style.backgroundColor = brick_color;
  $("#brick1").change(function () {
    console.log("#brick1 change")
    let brick = document.getElementById("brick1-color")
    brick.style.backgroundImage = "url(assets/brick_inverted.png)"
    brick.style.backgroundColor = $("#brick1").val();

  })
  $("#brick2").change(function () {
    console.log("#brick2 change")
    document.getElementById("brick2-color").style.backgroundColor = $("#brick2").val();
  })
  $("#brick3").change(function () {
    console.log("#brick3 change")
    document.getElementById("brick3-color").style.backgroundColor = $("#brick3").val();
  })
});
autoRedirect();

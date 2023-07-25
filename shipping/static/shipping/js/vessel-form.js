let dropdown = document.getElementById("id_vessel_type");

let divs = document.querySelectorAll(".foreign-vessel-fields");

dropdown.addEventListener("change", function () {
  let value = dropdown.value;

  if (value == "FOREIGN") {
    divs.forEach(function (div) {
      div.classList.remove("foreign-vessel-fields");
    });
  } else {
    divs.forEach(function (div) {
      div.classList.add("foreign-vessel-fields");
    });
  }
});

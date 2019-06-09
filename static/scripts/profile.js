function showForm(n) {
  const FORMS = document.querySelectorAll(".change-data");
  const DATAPIECES = document.querySelectorAll(".datapiece");

  FORMS.forEach(function(element){
    element.style.display = "";
  });

  DATAPIECES.forEach(function(element){
    element.style.display = "";
  });

  FORMS[n].style.display = "block";
  DATAPIECES[n].style.display = "none";
}

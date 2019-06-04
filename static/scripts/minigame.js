const ELEMENT = document.body.querySelector("#element");
const SIRINA = parseInt(getComputedStyle(ELEMENT).width);

function pristejMargin(currentMargin) {
  currentMargin += 1;
  currentMargin = currentMargin.toString();
  currentMargin = currentMargin + "px";
  return currentMargin;
}
function odstejMargin(currentMargin) {
  currentMargin -= 1;
  currentMargin = currentMargin.toString();
  currentMargin = currentMargin + "px";
  return currentMargin;
}

var pravaSmer;
function levo() {
  pravaSmer = "levo";
}
function desno() {
  pravaSmer = "desno";
}
function gor() {
  pravaSmer = "gor";
}
function dol() {
  pravaSmer = "dol";
}

setInterval(function() {
  if (pravaSmer == "levo") {
      currentMargin = parseInt(getComputedStyle(ELEMENT).marginLeft);
    if (currentMargin == 0) {}
    else {
      currentMargin = odstejMargin(currentMargin);
      ELEMENT.style.marginLeft = currentMargin;
    }
  }

  if (pravaSmer == "desno") {
    currentMargin = parseInt(getComputedStyle(ELEMENT).marginLeft);
    koncnaSirinaPolja = parseInt(getComputedStyle(document.querySelector("#polje")).width) - SIRINA;
    if (currentMargin == koncnaSirinaPolja) {}
    else if (currentMargin > koncnaSirinaPolja) {
      ELEMENT.style.marginLeft = koncnaSirinaPolja + "px";
    }
    else {
      currentMargin = pristejMargin(currentMargin);
      ELEMENT.style.marginLeft = currentMargin;
    }
  }

  if (pravaSmer == "gor") {
    currentMargin = parseInt(getComputedStyle(ELEMENT).marginTop);
    if (currentMargin == 0) {}
    else {
      currentMargin = odstejMargin(currentMargin);
      ELEMENT.style.marginTop = currentMargin;
    }
  }

  if (pravaSmer == "dol") {
    currentMargin = parseInt(getComputedStyle(ELEMENT).marginTop);
    koncnaVisinaPolja = parseInt(getComputedStyle(document.querySelector("#polje")).height) - SIRINA
    if (currentMargin == koncnaVisinaPolja) {}
    else if (currentMargin > koncnaVisinaPolja) {
      ELEMENT.style.marginTop = koncnaVisinaPolja + "px";
    }
    else {
      currentMargin = pristejMargin(currentMargin);
      ELEMENT.style.marginTop = currentMargin;
    }
  }
}, 3)

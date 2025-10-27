function turnON() {
  fetch('/on')
  document.getElementById("led").src = "./static/on.png"
}

function turnOFF() {
  fetch('/off')
  document.getElementById("led").src = "./static/off.png"
}

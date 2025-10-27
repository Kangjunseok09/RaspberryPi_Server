function Red() {
  fetch('/onred')
  fetch('/offyellow')
  fetch('/offgreen')
  document.getElementById("led").src = "./static/red.png"
}

function Green() {
  fetch('/ongreen')
  fetch('/offred')
  fetch('/offyellow')
  document.getElementById("led").src = "./static/green.png"
}

function Yellow() {
  fetch('/onyellow')
  fetch('/offgreen')
  fetch('/offred')
  document.getElementById("led").src = "./static/yellow.png"
}

function Gray(){
  fetch('/offgreen')
  fetch('/offred')
  fetch('/offyellow')
  document.getElementById("led").src = "./static/gray.png"
}





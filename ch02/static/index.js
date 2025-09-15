let count = 0;
let send = document.querySelector('#send');

function display_counter() {
  count++;
  document.getElementById('count').textContent = count;
}

send.addEventListener('click', async () => {
  let res = await fetch('/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ value: count })
  })
    count = 0;
    document.getElementById('count').textContent = count;
});
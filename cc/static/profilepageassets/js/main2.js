var input = document.getElementsByClassName('search-txt');
var message = document.getElementsByClassName('searchOptions')[0];
input.addEventListener('focus', function () {
  message.style.display = 'block';
});
input.addEventListener('focusout', function () {
  message.style.display = 'none';
});

function host() {
  document.getElementById('host-an-event').style.opacity = '1';
  document.getElementById('host-an-event').style.transition = 'all 0.3s';
  document.getElementById('host-an-event').style.pointerEvents = 'all';
  document.getElementById('host-an-event').style.display = 'block';
}
function hostclose() {
  document.getElementById('host-an-event').style.opacity = '0';
  document.getElementById('host-an-event').style.display = 'none';
}

var events = document.getElementById('host-an-event');
var btn = document.getElementById('host');
var span = document.getElementsByClassName('close')[0];
btn.onclick = function () {
  events.style.display = 'block';
};
span.onclick = function () {
  events.style.display = 'none';
};
window.onclick = function (event) {
  if (event.target == events) {
    events.style.display = 'none';
  }
};

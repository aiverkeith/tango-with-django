$(document).ready(function () {
  alert('hello world');
});

$('p').hover(
  function () {
    $(this).css('color', 'red');
  },
  function () {
    $(this).css('color', 'black');
  },
);

$(document).ready(function () {
  $('#like_button').click(function () {
    const category_id = $(this).attr('data-categoryid');
    $.get(
      '/rango/like_category/',
      { category_id: category_id },
      function (data) {
        $('#like_count').html(data);
        $('#like_button').hide();
      },
    );
  });

  function handleSearch() {
    const query = $(this).val();

    $.get('/rango/suggest/', { suggestion: query }, function (data) {
      $('#categories-listing').html(data);
    });
  }

  let t;
  $('#search-input').keyup(function () {
    clearInterval(t);
    t = setTimeout(handleSearch.bind(this), 300);
  });

  $('.add-page-button').click(function () {
    const categoryId = $(this).attr('data-categoryid');
    const title = $(this).attr('data-title');
    const url = $(this).attr('data-url');
    const clickedButton = $(this);

    $.get(
      '/rango/search_add_page/',
      { category_id: categoryId, title, url },
      function (data) {
      console.log(' --------------------------------------------');
      console.log('file: rango-jquery.js ~ line 38 ~ data', data);
      console.log(' --------------------------------------------');
        clickedButton.hide();
        $('#page-listing').html(data);
      },
    );
  });
});

// const handleLikeEvent = async () => {
//   const likeButtonEl = document.querySelector('#like_button');
//   const categoryId = likeButtonEl.getAttribute('data-categoryid');
//   const response = await fetch(
//     `/rango/like_category/?category_id=${categoryId}`,
//   );
//   const result = await response.json();

//   document.querySelector('#like_count').textContent = result;
//   likeButtonEl.style.display = 'none';
// };

// document.addEventListener('DOMContentLoaded', () => {
//   document
//     .querySelector('#like_button')
//     .addEventListener('click', handleLikeEvent);
// });

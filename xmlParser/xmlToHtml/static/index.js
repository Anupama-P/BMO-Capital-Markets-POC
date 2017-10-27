$(document).ready(function() {
  $('input[name="search"]').keypress(function() {
    if ($('input[name="search"]').val().length >= 2) {
      searchReports();
    }
  })
  $('button.search-button').click(function() {
    searchReports();
  })
  $('#search-filter').on('change', function() {
    var query = encodeURIComponent($('input[name="search"]').val());
    var formPostArr = $(this).serialize();
    var url = '/documents/search_filter/?q=query=' + query + '&';
    url = url + encodeURIComponent(formPostArr);
    if (query !== '') {
      $.ajax({
        url : url,
        type : 'POST',
        dataType: 'json',
        data : {data: formPostArr},
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success : function(data){
          var result = JSON.parse(data.response).hits.hits;
          var filenames = result.map((item) => item._source.filename);
          var html = filenames.map(file => "<a href='/documents/" + file + "' target='_blank'>" + file + "</a><br/>")
          $('div.results')[0].innerHTML = html.join('');
        },
        error : function(err){
          console.log(err.message);
        }
      });
    }
  })
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;

            }
        }
    }
    return cookieValue;
};

function searchReports() {
  var url = '/documents/search/?q=';
  url = url + encodeURIComponent($('input[name="search"]').val());
  $.ajax({
    url : url,
    type : 'POST',
    dataType: 'json',
    data : {},
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    success : function(data){
      var result = JSON.parse(data.response).hits.hits;
      console.log(result)
      var filenames = JSON.parse(data.response).hits.hits.map((item) => item._source.filename);
      var html = filenames.map(file => "<a href='/documents/" + file + "' target='_blank'>" + file + "</a><br/>")
      $('div.results')[0].innerHTML = html.join('');
    },
    error : function(err){
      console.log(err.message);
    }
  });
}

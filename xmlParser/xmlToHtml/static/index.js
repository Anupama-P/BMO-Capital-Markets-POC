$(document).ready(function() {
  $('input[name="search"]').keyup(function() {
    if ($('input[name="search"]').val().length >= 2) {
        delay(function(){
            searchReports();
        }, 500);
    }
  })
  $('button.search-button').click(function() {
    searchReports();
  })
  $('#search-filter').on('change', function() {
      searchReports();
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
  $('.search-text').show();
  var formPostArr = $('#search-filter').serialize();

  $.ajax({
    url : url,
    type : 'POST',
    dataType: 'json',
    data : {data: formPostArr},
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    success : function(data){
      $('.search-text').hide();

      var research_data = data.response.research_data.hits.hits;
      var company_data = data.response.company_data.hits.hits;

      // Research data
      if (research_data.length > 0) {
        $('.search-data, .search-title').show();
          var filenames = research_data.map((item) => item._source.filename);
          var html = filenames.map(file => "<a href='/documents/" + file + "' target='_blank'>" + file + "</a><br/>")
          $('div.research-data-results').html(html.join(''));
      }

      if (company_data.length > 0) {
        $('.search-data, .search-title').show();
          var companies = company_data.map((item) => item._source);
          var html = companies.map(company => "<a href='/company/" + company.investment_vehicleid + "' target='_blank'>" + company.name_en + "</a><br/>")
          $('div.company-data-results').html(html.join(''));
      }

      if (research_data.length == 0 && company_data.length == 0) {
        $('.search-data, .search-title').hide();
        $('div.results').html('<p class="lead">No results found</p>');
      }
    },
    error : function(err){
      $('.search-text').hide();
      $('div.results').html('<p class="lead">' + err.message + '</p>');
      console.log(err.message);
    }
  });
}

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

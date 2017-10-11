$(document).ready(function() {
  $('#search_field').change(function() {
    var url = '/documents/search/?q=';
    url = url + encodeURIComponent($(this).val());
    $.ajax({
      url : url,
      type : 'POST',
      dataType: 'json',
      data : {},
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      },
      success : function(data){
        var filenames = JSON.parse(data.response).hits.hits.map((item) => item._source.filename);
        var html = filenames.map(file => "<a href='/documents/" + file + "' target='_blank'>" + file + "</a><br/>")
        $('div.results')[0].innerHTML = html.join('');
      },
      error : function(err){
        console.log(err.message);
      }
    });
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

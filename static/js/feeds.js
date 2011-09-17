var get_date_string = function(date) {
    d = new Date(date); // javascript's built-in Date object does the heavy lifting
    weeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    fmt = [weeks[d.getDay()], months[d.getMonth()], d.getDate(), d.getFullYear()];
    return fmt.join(" ");
}

var build_list = function(data) {
    var html = '<ol id="results">';
    for(var i=0; i<data.length; i++) {
        html += "<li>";
        html += '<a href="' + data[i].fields.feed[1] + '">' + data[i].fields.feed[0] + '</a><br />';
        html += '<span class="date">Posted on: ' + get_date_string(data[i].fields.posted_on) + '</span><br />';
        html += '<a href="' + data[i].fields.url + '">' + data[i].fields.title; + '</a>';
        html += '<p>' + data[i].fields.content + '</p>';
        html += "</li>";
    }
    html += "</ol>";
    return html;
}

var search_request = function(query, sort_order) {
  if( query != "" ) {
    data = { q:query, so:sort_order };
    $.getJSON('ajax/', data,
    function(data) {
        console.log(data);
        $("#results").hide().replaceWith(build_list(data)).show();
    });
  }
  return false;
};

$(document).ready(function () {
  $("#search").keyup(function(e) {
    if( (e.keyCode >= 48 && e.keyCode <= 90) || e.keyCode == 8 ) {  // 0-9, a-z, 8=backspace
      search_request(this.value, $("input[@name='sort']:checked").val());
    }
  });

  $("input:radio").change(function() {
      search_request($("#search").val(), $("input[@name='sort']:checked").val());
  });

  $("form").submit(function () { return false; }); // so it won't submit
});

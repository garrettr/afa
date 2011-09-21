var get_date_string = function(date) {
    d = new Date(date); // javascript's built-in Date object does the heavy lifting
    weeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    fmt = [weeks[d.getDay()], months[d.getMonth()], d.getDate(), d.getFullYear()];
    return fmt.join(" ");
}

var build_list = function(data) {
    var html = '<ol id="results"><h2>Search results:</h2>';

    for(var i=0; i<data.length; i++) {
        html += "<li>";
        // start feed url
        html += '<a href="' + data[i].fields.feed[1] + '">';
        if( data[i].fields.feed[3] == "" ) {
            source = data[i].fields.feed[2];
            if( source == 'FB' ) {
                // default facebook icon
                html += '<img src="/static/img/facebook_48.png" class="feedpic" />';
            } else if ( source == 'TW' ) {
                // default twitter icon
                html += '<img src="/static/img/twitter_48.png" class="feedpic" />';
            } else if ( source == 'RA' ) {
                // default RSS/Atom icon
                html += '<img src="/static/img/rss_48.png" class="feedpic" />';
            }
        } else {
            html += '<img src="/media/' + data[i].fields.feed[3] + '" class="feedpic" />';
        }
        // feed name
        html += '<span class="feed">' + data[i].fields.feed[0] + '</span></a>';
        html += '<span class="date">Posted on: ' + get_date_string(data[i].fields.posted_on) + '</span><br />';
        // end feed url - wraps around feed name
        
        // print title if NOT a tweet - for tweets, title = content = tweet
        if( data[i].fields.feed[2] != "TW" ) {
          // title url - links to post
          html += '<span class="title"><a href="' + data[i].fields.url + '">' + data[i].fields.title + '</a></span><br />';
        }


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
        $("ol#results").hide().replaceWith(build_list(data)).show();
        // remove old highlighting
        $('li').removeHighlight();
        words = query.toLowerCase().split(" ");
        for( var i=0; i < words.length; i++ ) {
            if( words[i] != '' ) {
                $('li').highlight(words[i]);
            }
        }
    });
  } else {
    // print useful message, clear results
  }
  return false;
};

$(document).ready(function () {

  $('input#search').addClass("blurField");

  $('input#search').focus(function() {
    $(this).removeClass("blurField").addClass("focusField");
    if( this.value == this.defaultValue ) {
      this.value = '';
    }
    if( this.value != this.defaultValue ) {
      this.select();
    }
  });

  $('input#search').blur(function() {
    $(this).removeClass("focusField").addClass("blurField");
    if( $.trim(this.value) == '' ) {
      this.value = (this.defaultValue ? this.defaultValue : '');
    }
  });

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

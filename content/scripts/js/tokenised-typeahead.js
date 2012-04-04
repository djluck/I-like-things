(function() {

  $(function() {
    return $(".tokenised-typeahead input").typeahead({
      source: ["aaa", "aab", "aac"]
    }).focus(function() {
      return $(this).parent(".tokenised-typeahead").addClass("selected");
    }).blur(function() {
      return $(this).parent(".tokenised-typeahead").removeClass("selected");
    }).keypress(function(e) {
      var width;
      width = $(this).width();
      if (e.which === 8) {
        return $(this).width(width - 6);
      } else {
        return $(this).width(width + 6);
      }
    });
  });

}).call(this);

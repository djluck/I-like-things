$(function(){
    $("#tags").keyup(
        function(e){
            if (e.which == 32){ //spacebar
                var searchUrl = "/search?tags=" + encodeURIComponent($("#tags").val());
                jQuery.get(searchUrl, function(data){
                    $("#entries").html(data);
                });
            }
        }
    );
});
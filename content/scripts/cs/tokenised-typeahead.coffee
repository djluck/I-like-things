$ ->
    $(".tokenised-typeahead input")
        .typeahead({source: ["aaa", "aab", "aac"]})
        .focus ->
            $(this).parent(".tokenised-typeahead").addClass("selected")
        .blur ->
            $(this).parent(".tokenised-typeahead").removeClass("selected")
        .keypress (e) ->
            width = $(this).width()
            if e.which is 8
                $(this).width(width - 6)
            else
                $(this).width(width + 6)
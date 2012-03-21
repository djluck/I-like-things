function split( val ) {
	return val.split( / \s*/ );
}
function extractLast( term ) {
	return split( term ).pop();
}

$(function(){
    $( "#date_expires" ).datepicker({
	minDate: "+1d",
	dateFormat: "dd/mm/y"
    });
    $( "#tags" )
	.bind( "keydown", function( event ) {
	    if (event.keyCode === $.ui.keyCode.TAB && $(this).data("autocomplete").menu.active){
		event.preventDefault();
	    }
	})
	.autocomplete({
	    autoFocus: true,
	    source: function( request, response){
		// delegate back to autocomplete, but extract the last term
		response($.ui.autocomplete.filter(
			tagSource, extractLast(request.term)));
	    },
	    focus: function() {
		// prevent value inserted on focus
		return false;
	    },
	    select: function( event, ui){
		var terms = split(this.value);
		terms.pop();
		terms.push(ui.item.value);
		terms.push("");
		this.value = terms.join(" ");
		return false;
	    }
	});
});


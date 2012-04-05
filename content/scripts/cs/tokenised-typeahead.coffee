class TokenisedInput
    defaultInputWidth = 30
    addWidthPerChar = 6
    maxTagLength = 25

    constructor: (@$container, source) ->
        @$container = $(@$container)
        @$input = $("input", @$container)
        @tags = []
        @inputPlaceholder = @$input.attr("placeholder")
        
        #setup typeahead plugin & event handlers
        @$container
            .click =>
                @$input.focus()
        @$input
            .typeahead({
                source: source,
                onSelect: (inputEle, value) =>
                    @addTag value
            })
            .focus =>
                @_onInputFocus()
            .blur =>
                @_onInputBlur()
            .keydown (e) =>
                @_onKeydown(e)
                

    addTag: (value) =>
        #create tag element
        $element = $("<span class='tag'>#{ value } <i class='icon-tag-remove'></i></span>")
        newTag = 
            element: $element
            value: value
            
        #push new tag onto the tags stack
        @tags.push(newTag)
        
        #add tag element to DOM, wire up remove handlers
        $element
            .insertBefore(this.$input)
            .children(".icon-tag-remove")
            .click =>
                @_removeTag(newTag)
          
        @_resetInput()
        
        #return the new tag
        newTag
        
    
    #resets input styles
    _resetInput: (forceEmpty=false) =>
        width = defaultInputWidth
        placeholder = ""
        
        if (@$input.val() is "" and @tags.length == 0) or forceEmpty
            width = "100%"
            placeholder = @inputPlaceholder
        @$input
            .width(width)
            .val("")
            .focus()
            .attr("placeholder", placeholder)
            
            
    _removeTag: (toRemove) =>
        if @tags.length > 0
            if toRemove?
                #find tag to remove
                tagIndex = $.inArray(toRemove, @tags)
                if tagIndex >= 0
                    toRemove = @tags.splice(tagIndex, 1)[0]
            else
                #remove last tag
                toRemove = @tags.pop()
            toRemove.element.remove()
            if @tags.length is 0 and @$input.val() is ""
                @_resetInput()
                
        
        
    _onInputFocus: () =>
        @$container.addClass("selected")
        
        
    _onInputBlur: () =>
        @$container.removeClass("selected")
        
        
    _onKeydown: (e) =>
        rawInputVal = @$input.val()
        inputVal = $.trim(rawInputVal)
        switch e.which
            when 8 #backspace
                if rawInputVal.length is 0
                    @_removeTag()
                    @_resetInput()
                else if rawInputVal.length is 1 and @tags.length is 0
                    #as keydown proceeds the deletion of the last character, must forcefully reset the input style
                    #could do this on keyup but it has a slight delay and looks ugly!
                    @_resetInput(true)
                else
                    @$input.width(@$input.width() - addWidthPerChar)
            when 32 #space
                e.preventDefault()
                if inputVal isnt ""
                    @addTag(inputVal)
                    
            else 
                if rawInputVal.length < maxTagLength
                    @$input.width(defaultInputWidth + (@$input.val().length * addWidthPerChar))#
                else
                    e.preventDefault()
    
$ ->
    charWidth = 6
    defaultInputWidth = 30
    $(".tokenised-typeahead").each ->
        new TokenisedInput(this, ["aaa", "aab", "aac"])
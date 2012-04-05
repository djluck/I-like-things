(function() {
  var TokenisedInput,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  TokenisedInput = (function() {
    var addWidthPerChar, defaultInputWidth, maxTagLength;

    defaultInputWidth = 30;

    addWidthPerChar = 6;

    maxTagLength = 25;

    function TokenisedInput($container, source) {
      var _this = this;
      this.$container = $container;
      this._onKeydown = __bind(this._onKeydown, this);
      this._onInputBlur = __bind(this._onInputBlur, this);
      this._onInputFocus = __bind(this._onInputFocus, this);
      this._removeTag = __bind(this._removeTag, this);
      this._resetInput = __bind(this._resetInput, this);
      this.addTag = __bind(this.addTag, this);
      this.$container = $(this.$container);
      this.$input = $("input", this.$container);
      this.tags = [];
      this.inputPlaceholder = this.$input.attr("placeholder");
      this.$container.click(function() {
        return _this.$input.focus();
      });
      this.$input.typeahead({
        source: source,
        onSelect: function(inputEle, value) {
          return _this.addTag(value);
        }
      }).focus(function() {
        return _this._onInputFocus();
      }).blur(function() {
        return _this._onInputBlur();
      }).keydown(function(e) {
        return _this._onKeydown(e);
      });
    }

    TokenisedInput.prototype.addTag = function(value) {
      var $element, newTag,
        _this = this;
      $element = $("<span class='tag'>" + value + " <i class='icon-tag-remove'></i></span>");
      newTag = {
        element: $element,
        value: value
      };
      this.tags.push(newTag);
      $element.insertBefore(this.$input).children(".icon-tag-remove").click(function() {
        return _this._removeTag(newTag);
      });
      this._resetInput();
      return newTag;
    };

    TokenisedInput.prototype._resetInput = function(forceEmpty) {
      var placeholder, width;
      if (forceEmpty == null) forceEmpty = false;
      width = defaultInputWidth;
      placeholder = "";
      if ((this.$input.val() === "" && this.tags.length === 0) || forceEmpty) {
        width = "100%";
        placeholder = this.inputPlaceholder;
      }
      return this.$input.width(width).val("").focus().attr("placeholder", placeholder);
    };

    TokenisedInput.prototype._removeTag = function(toRemove) {
      var tagIndex;
      if (this.tags.length > 0) {
        if (toRemove != null) {
          tagIndex = $.inArray(toRemove, this.tags);
          if (tagIndex >= 0) toRemove = this.tags.splice(tagIndex, 1)[0];
        } else {
          toRemove = this.tags.pop();
        }
        toRemove.element.remove();
        if (this.tags.length === 0 && this.$input.val() === "") {
          return this._resetInput();
        }
      }
    };

    TokenisedInput.prototype._onInputFocus = function() {
      return this.$container.addClass("selected");
    };

    TokenisedInput.prototype._onInputBlur = function() {
      return this.$container.removeClass("selected");
    };

    TokenisedInput.prototype._onKeydown = function(e) {
      var inputVal, rawInputVal;
      rawInputVal = this.$input.val();
      inputVal = $.trim(rawInputVal);
      switch (e.which) {
        case 8:
          if (rawInputVal.length === 0) {
            this._removeTag();
            return this._resetInput();
          } else if (rawInputVal.length === 1 && this.tags.length === 0) {
            return this._resetInput(true);
          } else {
            return this.$input.width(this.$input.width() - addWidthPerChar);
          }
          break;
        case 32:
          e.preventDefault();
          if (inputVal !== "") return this.addTag(inputVal);
          break;
        default:
          if (rawInputVal.length < maxTagLength) {
            return this.$input.width(defaultInputWidth + (this.$input.val().length * addWidthPerChar));
          } else {
            return e.preventDefault();
          }
      }
    };

    return TokenisedInput;

  })();

  $(function() {
    var charWidth, defaultInputWidth;
    charWidth = 6;
    defaultInputWidth = 30;
    return $(".tokenised-typeahead").each(function() {
      return new TokenisedInput(this, ["aaa", "aab", "aac"]);
    });
  });

}).call(this);

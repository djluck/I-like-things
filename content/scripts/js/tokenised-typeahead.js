(function() {
  var TokenisedInput,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  TokenisedInput = (function() {
    var addWidthPerChar, defaultInputWidth, maxTagLength;

    defaultInputWidth = 30;

    addWidthPerChar = 6;

    maxTagLength = 25;

    function TokenisedInput($container, options) {
      var tagValue, _i, _len, _ref,
        _this = this;
      this.$container = $container;
      this._onKeydown = __bind(this._onKeydown, this);
      this._onInputBlur = __bind(this._onInputBlur, this);
      this._onInputFocus = __bind(this._onInputFocus, this);
      this._generateHiddenValue = __bind(this._generateHiddenValue, this);
      this._removeTag = __bind(this._removeTag, this);
      this._resetInput = __bind(this._resetInput, this);
      this.addTag = __bind(this.addTag, this);
      this.$container = $(this.$container);
      this.$input = $("input[type='text']", this.$container);
      this.$hidden = $("input[type='hidden']", this.$container);
      this.tags = [];
      this.inputPlaceholder = this.$input.attr("placeholder");
      if (options == null) options = {};
      if (options.source == null) options.source = [];
      this.$container.click(function() {
        return _this.$input.focus();
      });
      this.$input.typeahead({
        source: options.source,
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
      if (this.$hidden.val() !== "") {
        _ref = this.$hidden.val().split(",");
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          tagValue = _ref[_i];
          this.addTag(tagValue);
        }
      }
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
      this._generateHiddenValue();
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
        if (this.tags.length === 0 && this.$input.val() === "") this._resetInput();
        return this._generateHiddenValue();
      }
    };

    TokenisedInput.prototype._generateHiddenValue = function() {
      var tag;
      return this.$hidden.val((function() {
        var _i, _len, _ref, _results;
        _ref = this.tags;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          tag = _ref[_i];
          _results.push(tag.value);
        }
        return _results;
      }).call(this));
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
    return $(".tokenised-typeahead").each(function() {
      var srcVarName;
      srcVarName = $("input[type='hidden']", this).get(0).id + "_tagSrc";
      return new TokenisedInput(this, {
        "source": window[srcVarName]
      });
    });
  });

}).call(this);

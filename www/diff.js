$(document).ready(function () {
  var SELECTOR_BEFORE = '.before .syntaxhighlighter .code .line.number';
  var SELECTOR_AFTER = '.after .syntaxhighlighter .code .line.number';
  var CSS_MODIFIED = 'background-color: yellow !important;';
  var CSS_REMOVED = 'background-color: pink !important;';
  var CSS_HACK = 'cssText';

  function modified(n) {
    $(SELECTOR_BEFORE + n).css(CSS_HACK, CSS_MODIFIED);
    $(SELECTOR_AFTER + n).css(CSS_HACK, CSS_MODIFIED);
  }

  function removed(n) {
    $(SELECTOR_BEFORE + n).css(CSS_HACK, CSS_REMOVED);
  }

  modified(31);
  modified(187);

  removed(32);
  removed(33);
  removed(34);
  removed(35);

});

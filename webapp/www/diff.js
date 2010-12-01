var SELECTOR_BEFORE = ' .before .syntaxhighlighter .code .line.number';
var SELECTOR_AFTER = ' .after .syntaxhighlighter .code .line.number';
var CSS_ADDED = 'background-color: palegreen !important;';
var CSS_MODIFIED = 'background-color: yellow !important;';
var CSS_REMOVED = 'background-color: pink !important;';
var CSS_HACK = 'cssText';

function added(diff, n) {
  $('.diff' + diff + SELECTOR_AFTER + n).css(CSS_HACK, CSS_ADDED);
}

function modified(diff, n) {
  $('.diff' + diff + SELECTOR_BEFORE + n).css(CSS_HACK, CSS_MODIFIED);
  $('.diff' + diff + SELECTOR_AFTER + n).css(CSS_HACK, CSS_MODIFIED);
}

function removed(diff, n) {
  $('.diff' + diff + SELECTOR_BEFORE + n).css(CSS_HACK, CSS_REMOVED);
}

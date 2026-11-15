/* Language switcher: opens and closes the list of language links.
   The links themselves are plain <a> tags, so choosing a language is a normal page load. */
(function () {
  var root = document.querySelector('[data-lang]');
  if (!root) return;

  var button = root.querySelector('.lang-button');
  var menu = root.querySelector('.lang-menu');
  var items = Array.prototype.slice.call(menu.querySelectorAll('.lang-item'));

  function current() {
    return menu.querySelector('.lang-item[aria-current="true"]') || items[0];
  }
  function open(moveFocus) {
    menu.hidden = false;
    button.setAttribute('aria-expanded', 'true');
    if (moveFocus) current().focus();
  }
  function close(returnFocus) {
    if (menu.hidden) return;
    menu.hidden = true;
    button.setAttribute('aria-expanded', 'false');
    if (returnFocus) button.focus();
  }

  button.addEventListener('click', function (event) {
    if (menu.hidden) open(event.detail === 0); // detail 0 = opened from the keyboard
    else close(false);
  });
  button.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      open(true);
    }
  });

  menu.addEventListener('keydown', function (event) {
    var index = items.indexOf(document.activeElement);
    var next = null;
    if (event.key === 'ArrowDown') next = items[(index + 1) % items.length];
    else if (event.key === 'ArrowUp') next = items[(index - 1 + items.length) % items.length];
    else if (event.key === 'Home') next = items[0];
    else if (event.key === 'End') next = items[items.length - 1];
    if (next) {
      event.preventDefault();
      next.focus();
    }
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') close(root.contains(document.activeElement));
  });
  document.addEventListener('click', function (event) {
    if (!root.contains(event.target)) close(false);
  });
  root.addEventListener('focusout', function (event) {
    if (event.relatedTarget && !root.contains(event.relatedTarget)) close(false);
  });
})();

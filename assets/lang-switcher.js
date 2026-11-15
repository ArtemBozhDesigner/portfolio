/* Language switcher: opens the list, moves the check mark, updates the code on the button.
   It does not translate the page yet — translated versions are not built. */
(function () {
  var root = document.querySelector('[data-lang]');
  if (!root) return;

  var button = root.querySelector('.lang-button');
  var menu = root.querySelector('.lang-menu');
  var code = root.querySelector('.lang-code');
  var items = Array.prototype.slice.call(menu.querySelectorAll('.lang-item'));

  function checked() {
    return menu.querySelector('.lang-item[aria-checked="true"]') || items[0];
  }
  function open(moveFocus) {
    menu.hidden = false;
    button.setAttribute('aria-expanded', 'true');
    if (moveFocus) checked().focus();
  }
  function close(returnFocus) {
    if (menu.hidden) return;
    menu.hidden = true;
    button.setAttribute('aria-expanded', 'false');
    if (returnFocus) button.focus();
  }
  function select(item) {
    items.forEach(function (el) {
      el.setAttribute('aria-checked', el === item ? 'true' : 'false');
    });
    code.textContent = item.getAttribute('data-code');
    button.setAttribute('aria-label', 'Language: ' + item.textContent.trim());
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

  menu.addEventListener('click', function (event) {
    var item = event.target.closest('.lang-item');
    if (!item) return;
    select(item);
    close(event.detail === 0);
  });
  menu.addEventListener('keydown', function (event) {
    var index = items.indexOf(document.activeElement);
    var next = null;
    if (event.key === 'ArrowDown') next = items[(index + 1) % items.length];
    else if (event.key === 'ArrowUp') next = items[(index - 1 + items.length) % items.length];
    else if (event.key === 'Home') next = items[0];
    else if (event.key === 'End') next = items[items.length - 1];
    else if (event.key === 'Tab') { close(false); return; }
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
})();

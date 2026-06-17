/* Progressive enhancement for branch pages (e.g. the Guide).
   - Polyfills GFM task lists: Syrinx's markdown leaves "- [ ] item" as the literal
     text "[ ] item", so we turn those into real, tickable checkboxes that persist
     in localStorage.
   - Wraps content images in <figure> and lifts their alt text into a <figcaption>.
   Runs site-wide but only touches branch content (.page-sections / .prose), so the
   home page (#team, #community) is untouched. No-ops when there's nothing to do. */
(function () {
  "use strict";

  var TASK_RE = /^\s*\[([ xX])\]\s+/; // matches "[ ] " or "[x] " at the start of an item

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function enhanceTaskLists(root) {
    var items = root.querySelectorAll("li");
    var counter = 0;

    items.forEach(function (li) {
      // Read the leading text node only, so nested markup survives.
      var firstText = li.firstChild;
      if (!firstText || firstText.nodeType !== Node.TEXT_NODE) return;
      var m = firstText.nodeValue.match(TASK_RE);
      if (!m) return;

      var ul = li.parentElement;
      if (ul && ul.tagName === "UL") ul.classList.add("task-list");
      li.classList.add("task-item");

      // Strip the "[ ] " token from the visible text.
      firstText.nodeValue = firstText.nodeValue.replace(TASK_RE, "");

      var box = document.createElement("input");
      box.type = "checkbox";
      box.className = "task-box";

      var key = "et-task:" + location.pathname + ":" + counter++;
      var saved = null;
      try {
        saved = localStorage.getItem(key);
      } catch (e) {}
      box.checked = saved !== null ? saved === "1" : /[xX]/.test(m[1]);
      li.classList.toggle("is-checked", box.checked);

      box.addEventListener("change", function () {
        li.classList.toggle("is-checked", box.checked);
        try {
          localStorage.setItem(key, box.checked ? "1" : "0");
        } catch (e) {}
      });

      li.insertBefore(box, li.firstChild);
    });
  }

  function enhanceFigures(root) {
    var imgs = root.querySelectorAll("p > img");
    imgs.forEach(function (img) {
      var p = img.parentElement;
      if (!p.classList.contains("figure-row")) p.classList.add("figure-row");

      var figure = document.createElement("figure");
      figure.className = "guide-figure";
      p.insertBefore(figure, img);
      figure.appendChild(img);

      var alt = img.getAttribute("alt");
      if (alt && alt.trim()) {
        var cap = document.createElement("figcaption");
        cap.textContent = alt.trim();
        figure.appendChild(cap);
      }
    });
  }

  ready(function () {
    var areas = document.querySelectorAll(".page-sections .section-body, .prose");
    areas.forEach(function (area) {
      enhanceTaskLists(area);
      enhanceFigures(area);
    });
  });
})();

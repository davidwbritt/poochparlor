/* The Pooch Parlor — progressive enhancement only.
   Nav, FAQ and forms all work without this file; it just makes them nicer. */
(function () {
  "use strict";

  /* ---- mobile nav ---- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var panel = document.querySelector("[data-nav-panel]");
  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      var open = panel.getAttribute("data-open") === "true";
      panel.setAttribute("data-open", String(!open));
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.textContent = open ? "Menu" : "Close";
    });
    // close on navigation to an in-page anchor
    panel.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        panel.setAttribute("data-open", "false");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "Menu";
      }
    });
  }

  /* ---- service-area zip check ----
     The list of covered zips lives in one place: the data attribute on the
     form, so she (or whoever maintains this) can edit it without touching JS. */
  var zipForm = document.querySelector("[data-zip-check]");
  if (zipForm) {
    var covered = (zipForm.getAttribute("data-zips") || "")
      .split(",")
      .map(function (z) { return z.trim(); })
      .filter(Boolean);
    var out = zipForm.querySelector("[data-zip-result]");
    zipForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var val = (zipForm.querySelector("input[name=zip]").value || "").trim();
      if (!/^\d{5}$/.test(val)) {
        out.setAttribute("data-state", "error");
        out.textContent = "Please enter a 5-digit ZIP code.";
        return;
      }
      if (covered.indexOf(val) !== -1) {
        out.setAttribute("data-state", "ok");
        out.textContent =
          "Good news — " + val + " is in our regular route. Request an appointment and we'll confirm a time.";
      } else {
        out.setAttribute("data-state", "error");
        out.textContent =
          val + " is outside the usual route, but it's worth asking — call (919) 418-4773 and we'll tell you straight away.";
      }
    });
  }

  /* ---- appointment request form ----
     PROTOTYPE BEHAVIOUR: no server is wired up, so this validates and then
     shows the success state without sending anything. Replace the marked
     block below with a real endpoint (Formspree) or, in WordPress, delete
     this handler entirely and let the form plugin take over. */
  var reqForm = document.querySelector("[data-request-form]");
  if (reqForm) {
    var status = reqForm.querySelector("[data-form-status]");
    reqForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!reqForm.checkValidity()) {
        reqForm.reportValidity();
        return;
      }
      var dogs = reqForm.querySelectorAll("[name='dog_name']");
      var who = dogs.length && dogs[0].value ? dogs[0].value : "your dog";

      /* --- replace from here when a real endpoint exists --- */
      status.setAttribute("data-state", "ok");
      status.innerHTML =
        "<strong>Request received — nothing was actually sent.</strong><br>" +
        "This is the demo site, so no message left your browser. On the live site " +
        "this would email the request through and we'd text you back within a day to " +
        "confirm a time for " + who.replace(/[<>&]/g, "") + ".";
      /* --- to here --- */

      status.scrollIntoView({ behavior: "smooth", block: "center" });
      reqForm.querySelector("[type=submit]").disabled = true;
    });
  }

  /* ---- gallery lightbox ---- */
  var figures = document.querySelectorAll("[data-lightbox]");
  if (figures.length) {
    var box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("hidden", "");
    box.innerHTML =
      '<button class="lightbox__close" aria-label="Close">&times;</button><div class="lightbox__stage"></div>';
    document.body.appendChild(box);
    var stage = box.querySelector(".lightbox__stage");

    function close() {
      box.setAttribute("hidden", "");
      stage.innerHTML = "";
      document.body.style.overflow = "";
    }
    figures.forEach(function (fig) {
      fig.addEventListener("click", function () {
        stage.innerHTML = fig.innerHTML;
        box.removeAttribute("hidden");
        document.body.style.overflow = "hidden";
        box.querySelector(".lightbox__close").focus();
      });
    });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.classList.contains("lightbox__close")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !box.hasAttribute("hidden")) close();
    });
  }
})();

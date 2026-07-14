// ==========================================================================
// main.js — Bedirhan Çakıroğlu Portfolio
// Davranış: i18n dil değiştirme, mobil nav, scroll reveal, case alt-nav.
// ==========================================================================
(function(){
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SUPPORTED = ["en","de","tr"];
  var DEFAULT_LANG = "en";

  function detectLang(){
    var params = new URLSearchParams(window.location.search);
    var q = params.get("lang");
    if(q && SUPPORTED.indexOf(q) !== -1) return q;
    try{ var s = localStorage.getItem("lang"); if(s && SUPPORTED.indexOf(s)!==-1) return s; }catch(e){}
    var nav = (navigator.language || "en").slice(0,2).toLowerCase();
    if(SUPPORTED.indexOf(nav) !== -1) return nav;
    return DEFAULT_LANG;
  }

  function applyLang(lang){
    var dict = (window.I18N && window.I18N[lang]) || {};
    document.documentElement.setAttribute("lang", lang);
    document.querySelectorAll("[data-i18n]").forEach(function(el){
      var k = el.getAttribute("data-i18n"); if(dict[k]!=null) el.textContent = dict[k];
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function(el){
      var k = el.getAttribute("data-i18n-html"); if(dict[k]!=null) el.innerHTML = dict[k];
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function(el){
      var k = el.getAttribute("data-i18n-placeholder"); if(dict[k]!=null) el.setAttribute("placeholder", dict[k]);
    });
    document.querySelectorAll(".lang-switch button").forEach(function(btn){
      var on = btn.getAttribute("data-lang") === lang;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    try{ localStorage.setItem("lang", lang); }catch(e){}
  }

  var currentLang = detectLang();
  applyLang(currentLang);
  document.querySelectorAll(".lang-switch button").forEach(function(btn){
    btn.addEventListener("click", function(){ applyLang(btn.getAttribute("data-lang")); });
  });

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".primary-nav");
  if(toggle && nav){
    toggle.addEventListener("click", function(){
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function(l){
      l.addEventListener("click", function(){ nav.classList.remove("is-open"); toggle.setAttribute("aria-expanded","false"); });
    });
  }

  if(!reduceMotion && "IntersectionObserver" in window){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("is-visible"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll("[data-reveal]").forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll("[data-reveal]").forEach(function(el){ el.classList.add("is-visible"); });
  }

  var contactForm = document.getElementById("contact-form");
  if(contactForm){
    contactForm.addEventListener("submit", function(e){
      e.preventDefault();
      var name = contactForm.elements["name"].value.trim();
      var email = contactForm.elements["email"].value.trim();
      var message = contactForm.elements["message"].value.trim();
      var subject = "Portfolio contact — " + name;
      var body = message + "\n\n" + email;
      window.location.href = "mailto:bedirhanckr.id@gmail.com?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    });
  }

  var subnavLinks = document.querySelectorAll(".case-subnav a");
  var sections = document.querySelectorAll(".case-section[id]");
  if(subnavLinks.length && sections.length && "IntersectionObserver" in window){
    var so = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting){
          var id = e.target.getAttribute("id");
          subnavLinks.forEach(function(l){ l.classList.toggle("is-active", l.getAttribute("href") === "#"+id); });
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(function(s){ so.observe(s); });
  }
})();

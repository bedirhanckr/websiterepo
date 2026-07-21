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

  // Theme toggle — inline <head> script already stamped data-theme from
  // localStorage before paint (FOUC guard). Here we just wire the click.
  function currentTheme(){
    var forced = document.documentElement.getAttribute("data-theme");
    if(forced === "dark" || forced === "light") return forced;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var themeBtn = document.querySelector(".theme-toggle");
  if(themeBtn){
    themeBtn.addEventListener("click", function(){
      var next = currentTheme() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try{ localStorage.setItem("theme", next); }catch(e){}
    });
  }

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

  // Featured-work auto-flip carousel disabled. The alt images were shot in
  // 16:9 diagram framing and cropped inconsistently into the 4:3 thumb
  // slot. The hover blur + detail overlay covers what the flip was showing.

  // Hero parallax — portrait lags behind scroll for a subtle depth effect.
  // Only above 720px viewport (mobile portrait is too small to benefit).
  // Capped to the first 900px of scroll so it stops applying once hero is past.
  var heroPortrait = document.querySelector(".hero-portrait");
  if(heroPortrait && !reduceMotion && window.matchMedia("(min-width: 720px)").matches){
    var parallaxTicking = false;
    function updateParallax(){
      var y = Math.min(window.scrollY, 900);
      heroPortrait.style.transform = "translate3d(0," + (y * 0.14) + "px,0)";
      parallaxTicking = false;
    }
    window.addEventListener("scroll", function(){
      if(!parallaxTicking){
        window.requestAnimationFrame(updateParallax);
        parallaxTicking = true;
      }
    }, { passive: true });
    updateParallax();
  }

  // Consent banner (Google Consent Mode v2). Denied by default in the gtag
  // script; if the visitor accepts, we call gtag('consent','update') and let
  // Analytics start writing cookies. Decision persists to localStorage so
  // returning visitors don't see the banner again.
  function readConsent(){
    try{ return localStorage.getItem("consent"); }catch(e){ return null; }
  }
  function writeConsent(v){
    try{ localStorage.setItem("consent", v); }catch(e){}
  }
  function grantAnalytics(){
    if(typeof window.gtag === "function"){
      window.gtag('consent','update',{
        'analytics_storage':'granted',
        'ad_storage':'denied',
        'ad_user_data':'denied',
        'ad_personalization':'denied'
      });
    }
  }
  var storedConsent = readConsent();
  if(storedConsent === "granted"){
    grantAnalytics();
  } else if(storedConsent !== "denied"){
    // First visit — show banner. Text uses i18n if available, otherwise EN.
    var lang = document.documentElement.getAttribute("lang") || "en";
    var d = (window.I18N && window.I18N[lang]) || {};
    var msg = d["consent.msg"]
      || "This site uses analytics cookies to understand visitor patterns. You can decline.";
    var accept = d["consent.accept"] || "Accept";
    var decline = d["consent.decline"] || "Decline";

    var banner = document.createElement("div");
    banner.className = "consent-banner";
    banner.setAttribute("role","dialog");
    banner.setAttribute("aria-live","polite");
    banner.setAttribute("aria-label","Cookie consent");
    var p = document.createElement("p"); p.textContent = msg;
    var group = document.createElement("div"); group.className = "consent-buttons";
    var btnD = document.createElement("button");
    btnD.className = "consent-decline"; btnD.type = "button"; btnD.textContent = decline;
    var btnA = document.createElement("button");
    btnA.className = "consent-accept"; btnA.type = "button"; btnA.textContent = accept;
    group.appendChild(btnD); group.appendChild(btnA);
    banner.appendChild(p); banner.appendChild(group);
    document.body.appendChild(banner);
    setTimeout(function(){ banner.classList.add("is-in"); }, 20);

    function dismiss(){
      banner.classList.remove("is-in");
      setTimeout(function(){ banner.remove(); }, 320);
    }
    btnA.addEventListener("click", function(){
      writeConsent("granted"); grantAnalytics(); dismiss();
    });
    btnD.addEventListener("click", function(){
      writeConsent("denied"); dismiss();
    });
  }

  // Contact: submitted via formsubmit.co (see index.html <form action>).
  // After success formsubmit redirects back with ?sent=1, show a confirmation.
  try{
    var qs = new URLSearchParams(window.location.search);
    if(qs.get("sent") === "1"){
      var toastLang = document.documentElement.getAttribute("lang") || "en";
      var toastDict = (window.I18N && window.I18N[toastLang]) || {};
      var t = document.createElement("div");
      t.className = "form-toast";
      t.setAttribute("role","status");
      t.textContent = toastDict["contact.form.sent"] || "Thanks, I'll get back to you shortly.";
      document.body.appendChild(t);
      setTimeout(function(){ t.classList.add("is-in"); }, 20);
      setTimeout(function(){
        t.classList.remove("is-in");
        setTimeout(function(){ t.remove(); }, 400);
        // Clean up URL so the toast doesn't come back on refresh
        if(history.replaceState){
          history.replaceState({}, "", window.location.pathname);
        }
      }, 4200);
    }
  }catch(e){}

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

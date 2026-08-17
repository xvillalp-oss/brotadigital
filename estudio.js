/* Estudio Brota — comportamiento compartido del sitio */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fino = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ── menú ── */
  var burger = document.getElementById('burger'), mm = document.getElementById('mobileMenu');
  if (burger && mm) {
    burger.addEventListener('click', function () {
      var open = mm.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    mm.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { mm.classList.remove('open'); });
    });
  }

  /* ── nav reacciona al scroll ── */
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 12); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── reveals con stagger: cada elemento entra un poco después que el anterior de su sección ── */
  var seen = new Map();
  document.querySelectorAll('.rv').forEach(function (el) {
    var host = el.closest('section, header') || document.body;
    var n = seen.get(host) || 0;
    el.style.transitionDelay = reduced ? '0ms' : Math.min(n * 70, 420) + 'ms';
    seen.set(host, n + 1);
  });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });

  /* ── subrayado del hero ── */
  var hero = document.getElementById('hero');
  if (hero) requestAnimationFrame(function () { hero.classList.add('in'); });

  /* ── contadores numéricos ── */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var animar = function (el) {
      var to = parseInt(el.getAttribute('data-count'), 10);
      var suf = el.getAttribute('data-suffix') || '';
      if (reduced) { el.textContent = to + suf; return; }
      var start = null, dur = 1100;
      function tick(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(eased * to) + suf;
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    };
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { animar(e.target); cio.unobserve(e.target); } });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ── botones magnéticos ── */
  if (fino && !reduced) {
    document.querySelectorAll('.btn, .nav__cta').forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.28;
        var y = (e.clientY - r.top - r.height / 2) * 0.32;
        btn.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      });
      btn.addEventListener('mouseleave', function () { btn.style.transform = ''; });
    });
  }

  /* ── inclinación sutil de tarjetas (casos / fichas) ── */
  if (fino && !reduced) {
    document.querySelectorAll('.caso, .ficha').forEach(function (card) {
      card.style.transformStyle = 'preserve-3d';
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = 'perspective(900px) rotateX(' + (py * -3.5).toFixed(2) + 'deg) rotateY(' + (px * 3.5).toFixed(2) + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
  }

  /* ── showcase del hero (solo inicio) ── */
  var frame = document.getElementById('scFrame');
  if (frame) {
    var cap = document.getElementById('scCap'), dots = document.getElementById('scDots');
    var slides = [].slice.call(frame.querySelectorAll('a')), idx = 0, timer = null;
    slides.forEach(function (s, i) {
      var b = document.createElement('button');
      b.setAttribute('aria-label', 'Ver caso ' + (i + 1));
      if (i === 0) b.classList.add('on');
      b.addEventListener('click', function () { go(i); restart(); });
      dots.appendChild(b);
    });
    function go(i) {
      slides[idx].classList.remove('on'); dots.children[idx].classList.remove('on');
      idx = i;
      slides[idx].classList.add('on'); dots.children[idx].classList.add('on');
      cap.textContent = slides[idx].getAttribute('data-cap');
    }
    function next() { go((idx + 1) % slides.length); }
    function restart() { if (timer) clearInterval(timer); if (!reduced) timer = setInterval(next, 4200); }
    frame.addEventListener('mouseenter', function () { if (timer) clearInterval(timer); });
    frame.addEventListener('mouseleave', restart);
    restart();
  }

  /* ── filtros de casos (solo portafolio) ── */
  var chips = document.querySelectorAll('.chip');
  if (chips.length) {
    var casos = document.querySelectorAll('.caso');
    chips.forEach(function (ch) {
      ch.addEventListener('click', function () {
        chips.forEach(function (c) { c.classList.remove('on'); });
        ch.classList.add('on');
        var f = ch.getAttribute('data-f');
        casos.forEach(function (k) {
          k.classList.toggle('hide', f !== 'todos' && k.getAttribute('data-c') !== f);
        });
      });
    });
  }
})();

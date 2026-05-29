// ─────────────────────────────────────────────────────────────────────────────
// CALERO — catálogo autogestionable via Google Sheets
//
// CÓMO ACTUALIZAR EL CATÁLOGO SIN PROGRAMAR:
//   1. Abre tu Google Sheet (te damos el link)
//   2. Agrega, quita o edita filas libremente
//   3. Guarda — el sitio se actualiza en minutos, sin pagar nada extra
//
// COLUMNAS DEL SHEET:
//   id          → identificador único (p1, b1, t1…) — no repetir
//   categoria   → pantalla | base | tela
//   nombre      → nombre del producto
//   descripcion → descripción corta
//   precio      → número sin comas ni signos ($)
//   foto        → nombre de clase CSS  O  link de Google Drive (compartir → Copiar link)
//   activo      → TRUE para mostrar, FALSE para ocultar temporalmente
// ─────────────────────────────────────────────────────────────────────────────

// ← PEGA AQUÍ el ID de tu Google Sheet (solo la parte entre /d/ y /edit)
const SHEET_ID = '';

// ─── DATOS DEFAULT (respaldo si el Sheet no carga) ───────────────────────────
// ── URLs de Drive: https://drive.google.com/thumbnail?id=FILE_ID&sz=w800
// ── IMPORTANTE: las imágenes deben estar compartidas públicamente en Drive
const _DRV = id => `https://drive.google.com/thumbnail?id=${id}&sz=w800`;

const _DEF_PANTALLAS = [
  { id:'p1',  name:'Cónica Rafia',          desc:'Pantalla hecha a mano · rafia · cónica · base dorada · Ø 30 cm',           price:1800, img:_DRV('1iXP-OVNf6iR3tI6o_iR08yXdnvTj_-GH') },
  { id:'p2',  name:'Tambor Borgoña',         desc:'Pantalla hecha a mano · tela · cilíndrica · borgoña · Ø 35 cm',            price:1800, img:_DRV('1n3oibEM1FCkWcmK-zS55OShgj1vYi-P2')  },
  { id:'p3',  name:'Tambor Natural',         desc:'Pantalla hecha a mano · yute · cilíndrica · tono crudo · Ø 35 cm',        price:1800, img:_DRV('1_nSaeKjVcb1zqSWIuMw6gNt74OgZVTTk') },
  { id:'p4',  name:'Tambor Blanco',          desc:'Pantalla hecha a mano · tela · cilíndrica · blanco liso · Ø 35 cm',       price:1800, img:_DRV('1cYmJ0LI4SbK9XuAVdlM6ynjZtNO6NRhm') },
  { id:'p5',  name:'Tambor Flecos Rojo',     desc:'Pantalla hecha a mano · tela · cilíndrica · rojo · flecos dorados',       price:1800, img:_DRV('1-7SSLI5-VSYqE4SJal8UkpJga6F_MSb-')  },
  { id:'p6',  name:'Cónica Navy',            desc:'Pantalla hecha a mano · tela · cónica · azul marino · Ø 30 cm',           price:1800, img:_DRV('171JhXjkZw_EOOQycKxrpW9h0dyqxWSIB')  },
  { id:'p7',  name:'Tambor Flecos Borgoña',  desc:'Pantalla hecha a mano · tela · cilíndrica · borgoña · flecos en capas',  price:1800, img:_DRV('19DAXPEe1gA9bwDUMs-qWel3xg6AAlfkT')  },
  { id:'p8',  name:'Cónica Azul',            desc:'Pantalla hecha a mano · tela · cónica · azul pálido · Ø 30 cm',          price:1800, img:_DRV('14Fujwr9FFhDYccMafu49Idv45FcP8dZQ')  },
  { id:'p9',  name:'Tambor Plisado Blanco',  desc:'Pantalla hecha a mano · plisada · cilíndrica · blanco · Ø 35 cm',        price:1800, img:_DRV('1eMMDMlOggmTiBpDJ4z7ZI0Bs94v8zwH2')  },
  { id:'p10', name:'Tambor Plisado Verde',   desc:'Pantalla hecha a mano · plisada · cilíndrica · verde · Ø 35 cm',         price:1800, img:_DRV('1T5jzF0H1J5AYAmL-gCkAtFBQGU6C8iwT')  },
  { id:'p11', name:'Tambor Plisado Rosa',    desc:'Pantalla hecha a mano · plisada · cilíndrica · rosa · Ø 35 cm',          price:1800, img:_DRV('1A3L4BEw9xMpAw817eZkaa1hX-uXjUerX')  },
  { id:'p12', name:'Tambor Plisado Mostaza', desc:'Pantalla hecha a mano · plisada · cilíndrica · mostaza · Ø 35 cm',       price:1800, img:_DRV('1w0RkzJMcrS0LNVkMxbJd4aDFu_CgOEsL')  },
  { id:'p13', name:'Tambor Plisado Teal',    desc:'Pantalla hecha a mano · plisada · cilíndrica · verde azulado · Ø 35 cm', price:1800, img:_DRV('1M_s5LSXAmjmZ5MK9TD8xxdrYwA7dmBNr')  },
  { id:'p14', name:'Tambor Plisado Azul',    desc:'Pantalla hecha a mano · plisada · cilíndrica · azul · Ø 35 cm',          price:1800, img:_DRV('1Y8u_RmI5jhC6LO1tgvI1NTNYRYMx4Cl0')  },
  { id:'p15', name:'Tambor Plisado Coral',   desc:'Pantalla hecha a mano · plisada · cilíndrica · coral · Ø 35 cm',         price:1800, img:_DRV('1soxAgUXpnyBEVLksz0xafqykrMua9z99')   },
  { id:'p16', name:'Tambor Plisado Rayas',   desc:'Pantalla hecha a mano · plisada · cilíndrica · rayas · Ø 35 cm',         price:1800, img:_DRV('1EcuWyHQdne7vYwm5yil-xCbK0_7sEff7')  },
  { id:'p17', name:'Tambor Plisado Teal 2',  desc:'Pantalla hecha a mano · plisada · cilíndrica · teal bicolor · Ø 35 cm', price:1800, img:_DRV('1juXBMD8wdRL3PwX0CKh6jotpEEgdpMQj')  },
  { id:'p18', name:'Tambor Plisado Azul 2',  desc:'Pantalla hecha a mano · plisada · cilíndrica · azul bicolor · Ø 35 cm', price:1800, img:_DRV('1aXi_fEs-Cmift5vkVhPGndHoRCHtXM9Z')  },
  { id:'p19', name:'Tambor Flecos Blanco',   desc:'Pantalla hecha a mano · tela · cilíndrica · blanco · flecos dorados',   price:1800, img:_DRV('1Z-iAHl64nvpn-iU4cVDJ5QBBP019LmZ2')  },
  { id:'p20', name:'Tambor Marino',          desc:'Pantalla hecha a mano · tela · cilíndrica · azul marino · Ø 35 cm',     price:1800, img:_DRV('1qn3rv7y8T0QRLHAZSTLWSkc0h4qbnX6w')  },
];
const _DEF_BASES = [
  { id:'b1', name:'Margo',  desc:'Cerámica alta temperatura · 21cm Ø × 35cm alt. · 3kg',                         price:4600, img:_DRV('1zAAuNQdsHVO008e_eOgQts6IRgI0udGh') },
  { id:'b2', name:'Pepa',   desc:'Cerámica alta temperatura · 24cm Ø × 24cm alt. · 2.8kg',                       price:4100, img:_DRV('1JDPtUXwqITceHp3D4DheqqlGrGSqSGLp') },
  { id:'b3', name:'Toña',   desc:'Cerámica alta temperatura · 16cm Ø × 34cm alt. · 3.3kg · edición 5 piezas',   price:5100, img:'ph ph-7298' },
  { id:'b4', name:'Concha', desc:'Cerámica alta temperatura · hecha a mano CDMX · 36cm',                         price:4500, img:'ph ph-7304' },
  { id:'b5', name:'Lupita', desc:'Cerámica alta temperatura · engobe terracota · 44cm',                          price:5900, img:'ph ph-7322' },
  { id:'b6', name:'Chela',  desc:'Cerámica alta temperatura · barro negro · base baja · 32cm',                   price:5200, img:'ph ph-7414' },
];
const _DEF_TELAS = [
  { id:'t1', name:'Lino Crudo',    desc:'Lino 100% · tono natural · ancho 150 cm · por metro',       price:420, img:'bg-t1' },
  { id:'t2', name:'Algodón Tela',  desc:'Algodón natural · blanco hueso · ancho 140 cm · por metro', price:380, img:'bg-t2' },
  { id:'t3', name:'Lino Teñido',   desc:'Lino en tinte vegetal ocre · 150 cm · por metro',           price:480, img:'bg-t3' },
];

// ─── DATOS VIVOS (se reemplazan al cargar el Sheet) ──────────────────────────
let PANTALLAS = [..._DEF_PANTALLAS];
let BASES     = [..._DEF_BASES];
let TELAS     = [..._DEF_TELAS];
let ALL       = [...PANTALLAS, ...BASES, ...TELAS];

const FAQ = [
  { q:'¿Cuánto tarda mi pedido?', a:'Cada pieza se hace por encargo. El tiempo de producción es de 7 a 14 días hábiles a partir del anticipo. Te avisamos por WhatsApp en cuanto esté lista.' },
  { q:'¿El envío a CDMX realmente no tiene costo?', a:'Así es. El envío dentro de Ciudad de México está incluido en el precio. Para el resto del país cotizamos el costo de acuerdo al destino y lo confirmamos antes de que pagues.' },
  { q:'¿Puedo combinar cualquier base con cualquier pantalla?', a:'Sí. Todas las pantallas están diseñadas para embonar con cualquiera de las bases. Si tienes dudas sobre proporciones, con gusto te orientamos por WhatsApp.' },
  { q:'¿Aceptan pedidos personalizados?', a:'Sí. Hacemos piezas a medida: colores, tamaños y acabados específicos. Escríbenos para platicar tu proyecto.' },
  { q:'¿Cómo funciona el pago?', a:'50% anticipo al confirmar el pedido, 50% restante antes de la entrega. Aceptamos transferencia (SPEI) y en efectivo para entregas en CDMX.' },
];

// ─── SHEET LOADER ─────────────────────────────────────────────────────────────
const _readyCallbacks = [];
let   _ready = false;

/** Registra una función que se ejecuta cuando los datos estén disponibles */
function onDataReady(fn) {
  if (_ready) { fn(); return; }
  _readyCallbacks.push(fn);
}

function _fireReady() {
  _ready = true;
  _readyCallbacks.forEach(fn => fn());
}

/** Convierte link de Google Drive a URL de imagen directa */
function _driveToImg(raw) {
  if (!raw) return '';
  // Link completo de Drive: https://drive.google.com/file/d/ID/view…
  const m = raw.match(/\/d\/([a-zA-Z0-9_-]{10,})/);
  if (m) return `https://drive.google.com/thumbnail?id=${m[1]}&sz=w800`;
  // ID directo (sin slash)
  if (/^[a-zA-Z0-9_-]{25,}$/.test(raw)) return `https://drive.google.com/thumbnail?id=${raw}&sz=w800`;
  return raw; // URL externa o nombre de clase CSS
}

function _parseCSV(text) {
  const lines = text.trim().split('\n');
  const headers = _splitLine(lines[0]).map(h => h.toLowerCase().trim().replace(/\s+/g, '_'));
  return lines.slice(1)
    .filter(l => l.trim())
    .map(l => {
      const vals = _splitLine(l);
      const obj = {};
      headers.forEach((h, i) => { obj[h] = (vals[i] || '').trim(); });
      return obj;
    });
}

function _splitLine(line) {
  const res = []; let cur = '', inQ = false;
  for (const ch of line) {
    if (ch === '"') { inQ = !inQ; }
    else if (ch === ',' && !inQ) { res.push(cur); cur = ''; }
    else { cur += ch; }
  }
  res.push(cur);
  return res;
}

function _rowToProduct(r) {
  return {
    id:    r.id || '',
    name:  r.nombre || r.name || '',
    desc:  r.descripcion || r.desc || '',
    price: parseInt(r.precio || r.price || '0') || 0,
    img:   _driveToImg(r.foto || r.img || ''),
  };
}

async function _loadSheet() {
  if (!SHEET_ID) { _fireReady(); return; }
  const url = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv&gid=0`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const rows = _parseCSV(await res.text());
    // Filtrar activos (omitir filas con activo=FALSE o activo=0)
    const active = rows.filter(r => {
      const v = (r.activo || '').toUpperCase();
      return v !== 'FALSE' && v !== '0';
    });
    PANTALLAS = active.filter(r => r.categoria === 'pantalla').map(_rowToProduct);
    BASES     = active.filter(r => r.categoria === 'base').map(_rowToProduct);
    TELAS     = active.filter(r => r.categoria === 'tela').map(_rowToProduct);
    ALL       = [...PANTALLAS, ...BASES, ...TELAS];
    console.info(`✓ Catálogo cargado desde Sheet: ${PANTALLAS.length} pantallas, ${BASES.length} bases, ${TELAS.length} telas`);
  } catch (e) {
    console.info('Catálogo: usando datos locales (Sheet no disponible):', e.message);
  }
  _fireReady();
}

// ─── RENDER ──────────────────────────────────────────────────────────────────
function renderProducts(list, gridId, category) {
  const grid = document.getElementById(gridId);
  if (!grid) return;
  grid.innerHTML = list.map(p => {
    // Soporte para URL de imagen (Drive, externa) o nombre de clase CSS
    const isUrl = p.img && (p.img.startsWith('http') || p.img.startsWith('//'));
    const imgAttr = isUrl
      ? `class="product__image ph" style="background-image:url('${p.img}')"`
      : `class="product__image ${p.img}"`;
    return `
    <article class="product">
      <div ${imgAttr}></div>
      <h3 class="product__name">${p.name}</h3>
      <p class="product__desc">${p.desc}</p>
      <div class="product__row">
        <span class="product__price">$${p.price.toLocaleString('es-MX')} MXN</span>
        <button class="product__add" data-id="${p.id}" data-cat="${category}">Agregar</button>
      </div>
    </article>`;
  }).join('');
}

function renderFAQ(containerId = 'faqList') {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = FAQ.map((f, i) => `
    <div class="faq__item">
      <button class="faq__question" data-faq="${i}">
        ${f.q}
        <span class="faq__icon">+</span>
      </button>
      <div class="faq__answer"><p>${f.a}</p></div>
    </div>
  `).join('');
}

// ─── CARRITO ─────────────────────────────────────────────────────────────────
let cart = JSON.parse(localStorage.getItem('caleroCart2') || '[]');

function saveCart() { localStorage.setItem('caleroCart2', JSON.stringify(cart)); }

function addToCart(id, category) {
  const p = ALL.find(x => x.id === id);
  if (!p) return;
  cart.push({ ...p, category });
  saveCart(); renderCart();
}

function removeFromCart(idx) { cart.splice(idx, 1); saveCart(); renderCart(); }

function renderCart() {
  const countEl   = document.getElementById('cartCount');
  const countDesk = document.getElementById('cartCountDesktop');
  const totalEl   = document.getElementById('cartTotal');
  const body      = document.getElementById('cartBody');
  const btn       = document.getElementById('checkoutBtn');

  const n = cart.length;
  if (countEl)   { countEl.textContent = n;   countEl.classList.toggle('visible', n > 0); }
  if (countDesk) { countDesk.textContent = n; countDesk.classList.toggle('visible', n > 0); }
  if (totalEl)   { totalEl.textContent = `$${cart.reduce((s,i)=>s+i.price,0).toLocaleString('es-MX')} MXN`; }

  document.querySelectorAll('.product__add').forEach(b => {
    const inCart = cart.some(i => i.id === b.dataset.id);
    b.classList.toggle('in-cart', inCart);
    b.textContent = inCart ? '✓ Agregado' : 'Agregar';
  });

  if (!body) return;
  if (!n) {
    body.innerHTML = `<p class="cart__empty">Aún no has agregado piezas.</p>`;
    btn?.classList.add('disabled'); return;
  }
  btn?.classList.remove('disabled');
  body.innerHTML = cart.map((it, idx) => {
    const isUrl = it.img && (it.img.startsWith('http') || it.img.startsWith('//'));
    const imgAttr = isUrl
      ? `class="cart__item-img ph" style="background-image:url('${it.img}')"`
      : `class="cart__item-img ${it.img}"`;
    return `
    <div class="cart__item">
      <div ${imgAttr}></div>
      <div class="cart__item-info">
        <div class="cart__item-name">${it.name}</div>
        <div class="cart__item-cat">${it.category}</div>
        <button class="cart__item-remove" data-idx="${idx}">Quitar</button>
      </div>
      <div class="cart__item-price">$${it.price.toLocaleString('es-MX')}</div>
    </div>`;
  }).join('');
}

// ─── EVENTOS ─────────────────────────────────────────────────────────────────
document.addEventListener('click', e => {
  const addBtn = e.target.closest('.product__add');
  if (addBtn) { addToCart(addBtn.dataset.id, addBtn.dataset.cat); openCart(); return; }

  const rmBtn = e.target.closest('.cart__item-remove');
  if (rmBtn) { removeFromCart(parseInt(rmBtn.dataset.idx)); return; }

  const faqBtn = e.target.closest('.faq__question');
  if (faqBtn) { faqBtn.closest('.faq__item').classList.toggle('open'); return; }
});

// Menú móvil
const menuEl = document.getElementById('menu');
const menuOv = document.getElementById('menuOverlay');
function openMenu()  { menuEl?.classList.add('open');  menuOv?.classList.add('open'); }
function closeMenu() { menuEl?.classList.remove('open'); menuOv?.classList.remove('open'); }
document.getElementById('openMenu')?.addEventListener('click', openMenu);
document.getElementById('closeMenu')?.addEventListener('click', closeMenu);
menuOv?.addEventListener('click', closeMenu);
document.querySelectorAll('.menu-close-link').forEach(a => a.addEventListener('click', closeMenu));

// Tienda toggle (nivel 1)
document.getElementById('tiendaToggle')?.addEventListener('click', () => {
  document.getElementById('tiendaItem')?.classList.toggle('menu__item--open');
});

// Sub-sub toggles en menú móvil (Luminarias, De mesa, etc.)
document.querySelectorAll('.menu__sub-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('li');
    if (!li) return;
    // Cerrar otros al mismo nivel
    const siblings = li.parentElement?.querySelectorAll(':scope > li');
    siblings?.forEach(sib => { if (sib !== li) sib.classList.remove('menu__sub-item--open'); });
    li.classList.toggle('menu__sub-item--open');
  });
});

// Sidenav Tienda click (nivel 1)
document.getElementById('sidenavTiendaBtn')?.addEventListener('click', () => {
  const item = document.querySelector('.sidenav__item--tienda');
  item?.classList.toggle('open');
});

// Sidenav sub-toggles (Luminarias, De mesa)
document.querySelectorAll('.sidenav__sub-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const targetId = btn.dataset.target;
    if (!targetId) return;
    const panel = document.getElementById(targetId);
    if (!panel) return;
    const isOpen = panel.classList.toggle('open');
    // Rotar flecha del botón
    const svg = btn.querySelector('svg');
    if (svg) svg.style.transform = isOpen ? 'rotate(90deg)' : '';
  });
});

// Carrito drawer
const cartEl = document.getElementById('cart');
const cartOv = document.getElementById('cartOverlay');
function openCart()  { cartEl?.classList.add('open');  cartOv?.classList.add('open'); }
function closeCart() { cartEl?.classList.remove('open'); cartOv?.classList.remove('open'); }
document.getElementById('openCart')?.addEventListener('click', openCart);
document.getElementById('openCartDesktop')?.addEventListener('click', openCart);
document.getElementById('closeCart')?.addEventListener('click', closeCart);
cartOv?.addEventListener('click', closeCart);

// ─── CHECKOUT MODAL (Mercado Pago) ───────────────────────────────────────────
function abrirModalCheckout() {
  if (!cart.length) return;

  // Inyectar modal si no existe
  if (!document.getElementById('checkoutModal')) {
    const modal = document.createElement('div');
    modal.id = 'checkoutModal';
    modal.className = 'co-modal';
    modal.innerHTML = `
      <div class="co-modal__backdrop" id="coBackdrop"></div>
      <div class="co-modal__box" role="dialog" aria-modal="true" aria-labelledby="coTitle">
        <div class="co-modal__head">
          <p class="co-modal__eyebrow label">Datos de entrega</p>
          <h2 class="co-modal__title" id="coTitle">Un paso más</h2>
          <button class="co-modal__close" id="coClose" aria-label="Cerrar">✕</button>
        </div>
        <form class="co-modal__form" id="coForm" novalidate>
          <label class="co-modal__label" for="coNombre">Nombre completo</label>
          <input class="co-modal__input" id="coNombre" type="text" placeholder="Tu nombre" autocomplete="name" required/>

          <label class="co-modal__label" for="coEmail">Correo electrónico</label>
          <input class="co-modal__input" id="coEmail" type="email" placeholder="para enviarte la confirmación" autocomplete="email" required/>

          <label class="co-modal__label" for="coTel">Teléfono (WhatsApp)</label>
          <input class="co-modal__input" id="coTel" type="tel" placeholder="55 0000 0000" autocomplete="tel"/>

          <label class="co-modal__label">¿Dónde entregamos?</label>
          <div class="co-modal__radio-group">
            <label class="co-modal__radio">
              <input type="radio" name="coZona" value="cdmx" checked/>
              <span>CDMX <em>(envío incluido)</em></span>
            </label>
            <label class="co-modal__radio">
              <input type="radio" name="coZona" value="fuera"/>
              <span>Fuera de CDMX <em>(cotizamos envío)</em></span>
            </label>
          </div>

          <div id="coDirWrap">
            <label class="co-modal__label" for="coDir">Colonia y alcaldía / municipio</label>
            <input class="co-modal__input" id="coDir" type="text" placeholder="ej. Roma Norte, Cuauhtémoc"/>
          </div>

          <p class="co-modal__note">Piezas hechas a mano · <strong>8–9 días hábiles</strong> · Pago seguro vía Mercado Pago</p>

          <p class="co-modal__error" id="coError" hidden></p>

          <button class="co-modal__submit" id="coSubmit" type="submit">
            <span id="coSubmitText">Ir a pagar</span>
            <span id="coSubmitLoad" hidden>Preparando pago…</span>
          </button>
        </form>
      </div>
    `;
    document.body.appendChild(modal);

    // Cerrar con backdrop o botón
    document.getElementById('coBackdrop').addEventListener('click', cerrarModalCheckout);
    document.getElementById('coClose').addEventListener('click', cerrarModalCheckout);

    // Submit
    document.getElementById('coForm').addEventListener('submit', manejarCheckout);
  }

  document.getElementById('checkoutModal').classList.add('open');
  document.body.style.overflow = 'hidden';
  setTimeout(() => document.getElementById('coNombre')?.focus(), 100);
}

function cerrarModalCheckout() {
  document.getElementById('checkoutModal')?.classList.remove('open');
  document.body.style.overflow = '';
}

async function manejarCheckout(e) {
  e.preventDefault();

  const nombre   = document.getElementById('coNombre')?.value.trim();
  const email    = document.getElementById('coEmail')?.value.trim();
  const telefono = document.getElementById('coTel')?.value.trim();
  const zona     = document.querySelector('input[name="coZona"]:checked')?.value || 'cdmx';
  const dir      = document.getElementById('coDir')?.value.trim();
  const errorEl  = document.getElementById('coError');

  // Validación mínima
  if (!nombre) { mostrarError('Por favor escribe tu nombre.'); return; }
  if (!email || !email.includes('@')) { mostrarError('Por favor escribe un correo válido.'); return; }

  function mostrarError(msg) {
    if (!errorEl) return;
    errorEl.textContent = msg;
    errorEl.hidden = false;
  }

  // Estado de carga
  const btnText = document.getElementById('coSubmitText');
  const btnLoad = document.getElementById('coSubmitLoad');
  const btn     = document.getElementById('coSubmit');
  if (btnText) btnText.hidden = true;
  if (btnLoad) btnLoad.hidden = false;
  if (btn)     btn.disabled  = true;
  if (errorEl) errorEl.hidden = true;

  try {
    const resp = await fetch('/api/crear-pago', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: cart.map(i => ({
          id:       i.id,
          name:     i.name,
          desc:     i.desc || '',
          category: i.category || '',
          price:    i.price,
          qty:      1,
        })),
        customer: { nombre, email, telefono, zona, direccion: dir },
      }),
    });

    const data = await resp.json();

    if (!resp.ok || !data.init_point) {
      throw new Error(data.error || 'Error al crear el pago');
    }

    // Redirigir a Mercado Pago
    window.location.href = data.init_point;

  } catch (err) {
    console.error('checkout error:', err);
    mostrarError(err.message || 'Ocurrió un error. Intenta de nuevo o escríbenos por WhatsApp.');
    if (btnText) btnText.hidden = false;
    if (btnLoad) btnLoad.hidden = true;
    if (btn)     btn.disabled  = false;
  }
}

document.getElementById('checkoutBtn')?.addEventListener('click', e => {
  e.preventDefault();
  abrirModalCheckout();
});

// ─── TARJETA 3D ──────────────────────────────────────────────────────────────
(function() {
  const card = document.getElementById('card3d');
  if (!card) return;
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width  - 0.5;
    const y = (e.clientY - r.top)  / r.height - 0.5;
    card.style.transform = `perspective(900px) rotateY(${x * 22}deg) rotateX(${-y * 16}deg) scale(1.03)`;
    card.style.transition = 'transform .05s ease';
  });
  card.addEventListener('mouseleave', () => {
    card.style.transition = 'transform .4s ease';
    card.style.transform  = 'perspective(900px) rotateY(0deg) rotateX(0deg) scale(1)';
  });
})();

// Scroll reveals
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Auto-abrir sidenav Tienda cuando el botón tiene clase active (tienda.html)
if (document.getElementById('sidenavTiendaBtn')?.classList.contains('active')) {
  document.querySelector('.sidenav__item--tienda')?.classList.add('open');
}

// ─── INIT ────────────────────────────────────────────────────────────────────
renderCart();
_loadSheet(); // carga datos del Sheet (o usa defaults si no hay SHEET_ID)

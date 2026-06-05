// api/webhook.js
// Recibe notificaciones de Mercado Pago y envía emails de confirmación vía Resend
// Variables de entorno requeridas: MP_ACCESS_TOKEN, RESEND_API_KEY, RESEND_FROM

const { MercadoPagoConfig, Payment } = require('mercadopago');
const https = require('https');

// ─── Helper Resend (sin SDK extra) ───────────────────────────────────────────
// RESEND_FROM  → dirección verificada en resend.com, ej: "Calero <pedidos@calero.mx>"
// Para pruebas antes de verificar dominio: "Calero <onboarding@resend.dev>"
function resendSend({ toEmail, toName, subject, html }) {
  return new Promise((resolve, reject) => {
    const from = process.env.RESEND_FROM || 'Calero <onboarding@resend.dev>';
    const body = JSON.stringify({
      from,
      to:      [`${toName ? toName + ' <' : ''}${toEmail}${toName ? '>' : ''}`],
      subject,
      html,
    });

    const req = https.request({
      hostname: 'api.resend.com',
      path:     '/emails',
      method:   'POST',
      headers: {
        'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
        'Content-Type':  'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 400) reject(new Error(`Resend ${res.statusCode}: ${data}`));
        else resolve(JSON.parse(data || '{}'));
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ─── Plantilla email al CLIENTE ──────────────────────────────────────────────
function emailCliente(orderNumber, payment, metadata) {
  const items = (metadata?.itemsSummary || '').split(', ').filter(Boolean);
  const total = payment.transaction_amount?.toLocaleString('es-MX') || '—';
  const customer = metadata?.customer || {};

  const itemsHtml = items.length
    ? items.map(i => `<li style="padding:6px 0;border-bottom:1px solid #e8ddd0;">${i}</li>`).join('')
    : '';

  return `<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/></head>
<body style="margin:0;padding:0;background:#E6D9C8;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#E6D9C8;padding:40px 20px;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:4px;overflow:hidden;max-width:560px;width:100%;">

        <!-- Header -->
        <tr><td style="background:#700402;padding:28px 40px;">
          <p style="margin:0;font-size:22px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#E6D9C8;">Calero</p>
        </td></tr>

        <!-- Body -->
        <tr><td style="padding:36px 40px;">
          <p style="margin:0 0 8px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#a07060;">Pedido confirmado</p>
          <h1 style="margin:0 0 4px;font-size:28px;font-weight:700;color:#700402;">${orderNumber}</h1>
          <p style="margin:0 0 28px;font-size:13px;color:#a07060;">¡Gracias, ${customer.nombre || 'cliente'}! Tu pago fue aprobado.</p>

          <p style="margin:0 0 10px;font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#700402;">Tu pedido</p>
          <ul style="margin:0 0 24px;padding:0;list-style:none;">${itemsHtml}</ul>

          <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e8ddd0;border-radius:4px;margin-bottom:28px;">
            <tr>
              <td style="padding:14px 18px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#a07060;">Total pagado</td>
              <td style="padding:14px 18px;font-size:18px;font-weight:700;color:#700402;text-align:right;">$${total} MXN</td>
            </tr>
          </table>

          <p style="margin:0 0 6px;font-size:13px;color:#5a3030;line-height:1.7;">
            <strong>¿Qué sigue?</strong><br>
            Tus piezas se hacen a mano, una por una. El tiempo de producción es de <strong>8–9 días hábiles</strong>.
            Te contactaremos al <strong>${customer.telefono || 'número registrado'}</strong> por WhatsApp para coordinar la entrega.
          </p>

          ${customer.zona === 'fuera' ? `<p style="margin:16px 0 0;font-size:12px;color:#a07060;background:#f9f4ee;padding:12px 16px;border-radius:4px;">
            📦 Tu pedido es fuera de CDMX — te cotizaremos el envío por separado.
          </p>` : `<p style="margin:16px 0 0;font-size:12px;color:#a07060;background:#f9f4ee;padding:12px 16px;border-radius:4px;">
            🏙️ Envío incluido en CDMX.
          </p>`}
        </td></tr>

        <!-- Footer -->
        <tr><td style="padding:24px 40px;border-top:1px solid #e8ddd0;">
          <p style="margin:0;font-size:11px;color:#a07060;line-height:1.8;">
            Calero · CDMX · 2026<br>
            <a href="mailto:contacto@calero.mx" style="color:#700402;">contacto@calero.mx</a> ·
            <a href="https://www.instagram.com/caleromexicano/" style="color:#700402;">@caleromexicano</a>
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

// ─── Plantilla email a CALERO (notificación interna) ─────────────────────────
function emailAdmin(orderNumber, payment, metadata) {
  const customer = metadata?.customer || {};
  const total    = payment.transaction_amount?.toLocaleString('es-MX') || '—';
  const items    = (metadata?.itemsSummary || '').replace(/, /g, '\n• ');

  return `<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:32px;background:#f5f5f5;font-family:monospace,sans-serif;">
  <div style="background:#fff;max-width:500px;padding:28px;border:2px solid #700402;border-radius:4px;">
    <p style="margin:0 0 4px;font-size:11px;letter-spacing:.2em;color:#a07060;">NUEVO PEDIDO</p>
    <h2 style="margin:0 0 20px;font-size:24px;color:#700402;">${orderNumber}</h2>
    <table style="width:100%;font-size:13px;border-collapse:collapse;">
      <tr><td style="padding:7px 0;color:#888;width:120px;">Nombre</td><td style="padding:7px 0;font-weight:600;">${customer.nombre || '—'}</td></tr>
      <tr><td style="padding:7px 0;color:#888;">Email</td><td style="padding:7px 0;">${customer.email || '—'}</td></tr>
      <tr><td style="padding:7px 0;color:#888;">Teléfono</td><td style="padding:7px 0;">${customer.telefono || '—'}</td></tr>
      <tr><td style="padding:7px 0;color:#888;">Zona</td><td style="padding:7px 0;">${customer.zona === 'fuera' ? 'Fuera de CDMX' : 'CDMX'}</td></tr>
      <tr><td style="padding:7px 0;color:#888;">Dirección</td><td style="padding:7px 0;">${customer.direccion || '—'}</td></tr>
      <tr><td style="padding:7px 0;color:#888;">Total</td><td style="padding:7px 0;font-size:18px;font-weight:700;color:#700402;">$${total} MXN</td></tr>
    </table>
    <hr style="border:none;border-top:1px solid #eee;margin:16px 0;"/>
    <p style="margin:0;font-size:12px;color:#555;white-space:pre-line;">• ${items}</p>
    <hr style="border:none;border-top:1px solid #eee;margin:16px 0;"/>
    <p style="margin:0;font-size:11px;color:#aaa;">MP Payment ID: ${payment.id} · Estado: ${payment.status}</p>
  </div>
</body>
</html>`;
}

// ─── Código de tarjeta de regalo ─────────────────────────────────────────────
function generarCodigoRegalo() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // sin chars ambiguos
  const bloque = () => Array.from({length:4}, () => chars[Math.floor(Math.random()*chars.length)]).join('');
  return `CALERO-${bloque()}-${bloque()}`;
}

function emailRegalo(orderNumber, payment, metadata) {
  const codigo   = metadata?.giftCode || 'CALERO-XXXX-XXXX';
  const monto    = payment.transaction_amount?.toLocaleString('es-MX') || '—';
  const customer = metadata?.customer || {};

  return `<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background:#E6D9C8;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#E6D9C8;padding:40px 20px;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;overflow:hidden;">

        <!-- Gift card visual -->
        <tr><td style="background:#700402;border-radius:16px;padding:0;overflow:hidden;">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr><td style="padding:32px 40px 8px;">
              <p style="margin:0;font-size:32px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#E6D9C8;">Calero</p>
              <p style="margin:4px 0 0;font-size:9px;letter-spacing:.22em;text-transform:uppercase;color:rgba(230,217,200,.5);">Arte objeto · Hecho a mano · CDMX</p>
            </td></tr>
            <tr><td style="padding:16px 40px 32px;">
              <p style="margin:0;font-size:9px;letter-spacing:.22em;text-transform:uppercase;color:rgba(230,217,200,.5);">Tarjeta de regalo · Vigencia 1 año</p>
              <p style="margin:4px 0 0;font-size:48px;font-weight:700;color:#E6D9C8;line-height:1;">${monto}</p>
              <p style="margin:0;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:rgba(230,217,200,.5);">MXN</p>
            </td></tr>
          </table>
        </td></tr>

        <!-- Código -->
        <tr><td style="background:#fff;border-radius:8px;margin-top:12px;padding:32px 40px;text-align:center;">
          <p style="margin:0 0 8px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#a07060;">Tu código de regalo</p>
          <p style="margin:0 0 8px;font-size:28px;font-weight:700;color:#700402;letter-spacing:.22em;">${codigo}</p>
          <p style="margin:0 0 20px;font-size:11px;color:#a07060;">Canjeable en calero.mx · Vigente por 1 año</p>

          <p style="margin:0;font-size:13px;color:#5a3030;line-height:1.7;">Hola <strong>${customer.nombre || 'amiga'}</strong>, aquí está tu tarjeta de regalo.<br>
          Comparte este código con quien quieras regalar una luminaria Calero.</p>
        </td></tr>

        <!-- Footer -->
        <tr><td style="padding:20px 0;text-align:center;">
          <p style="margin:0;font-size:11px;color:#a07060;">Calero · CDMX · <a href="mailto:contacto@calero.mx" style="color:#700402;">contacto@calero.mx</a></p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

// ─── Handler principal ────────────────────────────────────────────────────────
module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST')    return res.status(405).end();

  try {
    const { type, data } = req.body;

    // MP envía varios tipos; solo nos interesan los pagos
    if (type !== 'payment') return res.status(200).json({ ok: true, skip: true });

    const client  = new MercadoPagoConfig({ accessToken: process.env.MP_ACCESS_TOKEN });
    const payment = await new Payment(client).get({ id: data.id });

    // Solo procesar pagos aprobados
    if (payment.status !== 'approved') return res.status(200).json({ ok: true, status: payment.status });

    const orderNumber = payment.external_reference;
    const metadata    = payment.metadata || {};

    // ── Detectar si es tarjeta de regalo ────────────────────────────────────
    const esRegalo  = metadata?.isGiftCard === true;
    const giftCode  = esRegalo ? generarCodigoRegalo() : null;
    if (giftCode) metadata.giftCode = giftCode;

    // ── Envío de emails ──────────────────────────────────────────────────────
    if (!process.env.RESEND_API_KEY) {
      console.warn('RESEND_API_KEY no configurado — saltando emails');
      return res.status(200).json({ ok: true, warn: 'no_email' });
    }

    const customerEmail = metadata?.customer?.email || payment.payer?.email;
    const customerName  = metadata?.customer?.nombre || '';

    const [emailA, emailB] = await Promise.all([
      // Email al cliente (regalo o pedido normal)
      customerEmail
        ? resendSend({
            toEmail:   customerEmail,
            toName:    customerName,
            subject:   esRegalo
              ? `Tu tarjeta de regalo Calero · ${giftCode}`
              : `Pedido ${orderNumber} confirmado — Calero`,
            html: esRegalo
              ? emailRegalo(orderNumber, payment, metadata)
              : emailCliente(orderNumber, payment, metadata),
          })
        : Promise.resolve({ skip: true }),

      // Notificación interna a Calero
      resendSend({
        toEmail:   'contacto@calero.mx',
        toName:    'Calero',
        subject:   esRegalo
          ? `Tarjeta de regalo ${orderNumber} · código ${giftCode}`
          : `Nuevo pedido ${orderNumber} · $${payment.transaction_amount?.toLocaleString('es-MX')} MXN`,
        html:      emailAdmin(orderNumber, payment, metadata),
      }),
    ]);

    console.log('Emails enviados:', { emailA: emailA?.id, emailB: emailB?.id });
    res.status(200).json({ ok: true, orderNumber });

  } catch (err) {
    console.error('webhook error:', err);
    // Siempre devolver 200 a MP para que no reintente
    res.status(200).json({ ok: false, error: err.message });
  }
};

// api/crear-pago.js
// Crea una preferencia de pago en Mercado Pago y devuelve el init_point
// Variables de entorno requeridas: MP_ACCESS_TOKEN, SITE_URL

const { MercadoPagoConfig, Preference } = require('mercadopago');

function generarNumeroPedido() {
  // Formato: CAL-YYYYMMDD-XXXX (ej. CAL-20260115-A3K9)
  const hoy = new Date();
  const fecha = hoy.toISOString().slice(0, 10).replace(/-/g, '');
  const sufijo = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `CAL-${fecha}-${sufijo}`;
}

module.exports = async (req, res) => {
  // Preflight CORS
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Método no permitido' });

  try {
    const { items, customer } = req.body;

    if (!items?.length)    return res.status(400).json({ error: 'Carrito vacío' });
    if (!customer?.email)  return res.status(400).json({ error: 'Email requerido' });
    if (!customer?.nombre) return res.status(400).json({ error: 'Nombre requerido' });

    const orderNumber = generarNumeroPedido();
    const siteUrl     = process.env.SITE_URL || 'https://calero.mx';

    const client = new MercadoPagoConfig({
      accessToken: process.env.MP_ACCESS_TOKEN,
    });

    const preference = new Preference(client);

    const result = await preference.create({
      body: {
        external_reference: orderNumber,
        items: items.map(it => ({
          id:          it.id,
          title:       it.name,
          description: it.desc || it.category || '',
          unit_price:  Number(it.price),
          quantity:    Number(it.qty || 1),
          currency_id: 'MXN',
        })),
        payer: {
          name:  customer.nombre,
          email: customer.email,
          phone: { number: customer.telefono || '' },
        },
        back_urls: {
          success: `${siteUrl}/pago-exitoso.html?pedido=${orderNumber}`,
          failure: `${siteUrl}/pago-fallido.html?pedido=${orderNumber}`,
          pending: `${siteUrl}/pago-pendiente.html?pedido=${orderNumber}`,
        },
        auto_return:      'approved',
        notification_url: `${siteUrl}/api/webhook`,
        metadata: {
          orderNumber,
          customer,
          itemsSummary: items.map(i => `${i.name} ($${i.price})`).join(', '),
        },
        statement_descriptor: 'CALERO CDMX',
        expires: false,
      },
    });

    res.status(200).json({
      id:           result.id,
      init_point:   result.init_point,
      orderNumber,
    });

  } catch (err) {
    console.error('crear-pago error:', err);
    res.status(500).json({ error: 'Error al crear el pago', detalle: err.message });
  }
};

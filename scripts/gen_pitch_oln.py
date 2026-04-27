from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

OUTPUT = "/Users/ximevillalpando/src/brota-digital/pitch-oln.pdf"

# ── Colores ──
RED    = colors.HexColor("#e01010")
DARK   = colors.HexColor("#0a0a0a")
DGRAY  = colors.HexColor("#1a1a1a")
BLUE   = colors.HexColor("#1B5EBF")
AMBER  = colors.HexColor("#F59E0B")
GRAY   = colors.HexColor("#888888")
LGRAY  = colors.HexColor("#f5f5f5")
WHITE  = colors.white
PINK   = colors.HexColor("#e07b8f")
GREEN  = colors.HexColor("#2d8a4e")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

# ── Estilos ──
S = lambda name, **kw: ParagraphStyle(name, **kw)

s_brand    = S("brand",   fontName="Helvetica-Bold",  fontSize=9,   textColor=PINK,  spaceAfter=2)
s_title    = S("title",   fontName="Helvetica-Bold",  fontSize=26,  textColor=DARK,  spaceAfter=6, leading=30)
s_sub      = S("sub",     fontName="Helvetica",       fontSize=11,  textColor=GRAY,  spaceAfter=4)
s_h2       = S("h2",      fontName="Helvetica-Bold",  fontSize=16,  textColor=DARK,  spaceBefore=14, spaceAfter=5)
s_h2r      = S("h2r",     fontName="Helvetica-Bold",  fontSize=16,  textColor=RED,   spaceBefore=14, spaceAfter=5)
s_h2b      = S("h2b",     fontName="Helvetica-Bold",  fontSize=16,  textColor=BLUE,  spaceBefore=14, spaceAfter=5)
s_h3       = S("h3",      fontName="Helvetica-Bold",  fontSize=12,  textColor=DARK,  spaceBefore=8,  spaceAfter=3)
s_body     = S("body",    fontName="Helvetica",       fontSize=10,  textColor=DARK,  leading=16, spaceAfter=5)
s_item     = S("item",    fontName="Helvetica",       fontSize=10,  textColor=DARK,  leading=16, spaceAfter=2, leftIndent=12)
s_note     = S("note",    fontName="Helvetica-Oblique", fontSize=9, textColor=GRAY,  leading=13, spaceAfter=4)
s_label    = S("label",   fontName="Helvetica-Bold",  fontSize=8,   textColor=GRAY,  spaceAfter=2, letterSpacing=1)
s_center   = S("center",  fontName="Helvetica",       fontSize=10,  textColor=DARK,  leading=14, spaceAfter=4, alignment=TA_CENTER)
s_footer   = S("footer",  fontName="Helvetica",       fontSize=8,   textColor=GRAY,  alignment=TA_CENTER)
s_price_r  = S("pricer",  fontName="Helvetica-Bold",  fontSize=28,  textColor=RED,   spaceAfter=2)
s_price_b  = S("priceb",  fontName="Helvetica-Bold",  fontSize=28,  textColor=BLUE,  spaceAfter=2)
s_big      = S("big",     fontName="Helvetica-Bold",  fontSize=20,  textColor=DARK,  spaceAfter=3)

story = []

# ══════════════════════════════════════════════
# PORTADA
# ══════════════════════════════════════════════
story.append(Spacer(1, 1*cm))
story.append(Paragraph("BROTA DIGITAL", s_brand))
story.append(Spacer(1, 6))
story.append(Paragraph("Propuesta de Servicios Digitales", s_title))
story.append(Paragraph("OLN Tires  ·  OLN Connect  ·  Grupo OLN", s_sub))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=8))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=20))

story.append(Paragraph(
    "Preparamos dos soluciones digitales complementarias para Grupo OLN: "
    "una página web de alto impacto para OLN Tires y una estrategia de redes sociales "
    "para OLN Connect. Este documento resume todo lo que incluye cada propuesta y la inversión correspondiente.",
    s_body
))
story.append(Spacer(1, 12))

# Stats row
stats = [
    ["2", "propuestas listas\npara presentar"],
    ["100%", "personalizado\npara Grupo OLN"],
    ["0", "intermediarios\nbrota trabaja directo"],
]
t_stats = Table([[Paragraph(v, S("sv", fontName="Helvetica-Bold", fontSize=26, textColor=RED, alignment=TA_CENTER)),
                  Paragraph(v, S("sv2", fontName="Helvetica-Bold", fontSize=26, textColor=BLUE, alignment=TA_CENTER)),
                  Paragraph(v, S("sv3", fontName="Helvetica-Bold", fontSize=26, textColor=DARK, alignment=TA_CENTER))]
                 for v, _ in [stats[0], stats[1], stats[2]]
                ] + [
                 [Paragraph(d, S("sd", fontName="Helvetica", fontSize=9, textColor=GRAY, alignment=TA_CENTER))
                  for _, d in stats]
                ], colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
# Rebuild simpler stats table
stats_data = []
row1 = []
row2 = []
for val, desc in stats:
    row1.append(Paragraph(val, S(f"v{val}", fontName="Helvetica-Bold", fontSize=24,
                                  textColor=RED if val=="2" else (BLUE if val=="100%" else DARK),
                                  alignment=TA_CENTER)))
    row2.append(Paragraph(desc, S(f"d{val}", fontName="Helvetica", fontSize=9,
                                   textColor=GRAY, alignment=TA_CENTER, leading=13)))
t_stats = Table([row1, row2], colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
t_stats.setStyle(TableStyle([
    ("ALIGN",        (0,0), (-1,-1), "CENTER"),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 10),
    ("BOTTOMPADDING",(0,0), (-1,-1), 10),
    ("LINEABOVE",    (0,0), (-1,0),  0.5, LGRAY),
    ("LINEBELOW",    (0,-1),(-1,-1), 0.5, LGRAY),
]))
story.append(t_stats)
story.append(Spacer(1, 20))

# ══════════════════════════════════════════════
# SECCIÓN 1 — OLN TIRES
# ══════════════════════════════════════════════
story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=10))
story.append(Paragraph("01 · OLN TIRES", s_label))
story.append(Paragraph("Página web de alto impacto", s_h2r))

story.append(Paragraph(
    "Outlet Llantas del Norte necesita una presencia digital que refleje su escala, "
    "catálogo y ventaja competitiva: precio de fábrica, entrega en 24 horas y más de 10 años en el mercado.",
    s_body
))

story.append(Paragraph("¿Qué incluye la página?", s_h3))
tires_items = [
    ("🏠", "Hero de impacto", "Headline visual fuerte: \"Deja Huella en Cada Kilómetro\" con fondo de operación real"),
    ("🏷", "Catálogo interactivo", "Filtros por categoría: Camión · Agrícola · Industrial — con ficha de cada producto"),
    ("🔴", "10 marcas distribuidas", "Gladiator, RoadX, Empire, Pegasus, JK Tyre, GMX, Benchmark y más"),
    ("📊", "Stats de confianza", "10+ años · Entrega 24h · Precio directo sin intermediarios"),
    ("📞", "Cotización directa", "Botón de contacto y formulario para solicitar precio por medida y cantidad"),
    ("📱", "100% responsive", "Diseño adaptado a celular, tablet y escritorio"),
    ("🔍", "SEO básico incluido", "Optimizada para búsquedas como 'llantas camión México' y 'distribuidora llantas industriales'"),
]
for icon, titulo, desc in tires_items:
    story.append(Paragraph(f"{icon}  <b>{titulo}</b> — {desc}", s_item))

story.append(Spacer(1, 10))

# Precio OLN Tires
precio_tires = Table([
    [Paragraph("Inversión página web OLN Tires", S("pt", fontName="Helvetica-Bold", fontSize=11, textColor=DARK)),
     Paragraph("Pago único", S("pu", fontName="Helvetica", fontSize=9, textColor=GRAY, alignment=TA_RIGHT))],
    [Paragraph("Precio a definir en reunión", S("pd", fontName="Helvetica-Bold", fontSize=14, textColor=RED)),
     Paragraph("", s_body)],
    [Paragraph("✓ Dominio y hosting primer año incluidos en propuesta  ✓ Entrega en 3 semanas",
               S("pi", fontName="Helvetica-Oblique", fontSize=9, textColor=GRAY)), ""],
], colWidths=[12*cm, 4.5*cm])
precio_tires.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#fff5f5")),
    ("LINEABOVE",    (0,0), (-1,0),  1.5, RED),
    ("LINEBELOW",    (0,-1),(-1,-1), 0.5, colors.HexColor("#dddddd")),
    ("TOPPADDING",   (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ("LEFTPADDING",  (0,0), (-1,-1), 12),
    ("SPAN",         (0,2), (-1,2)),
]))
story.append(precio_tires)
story.append(Spacer(1, 20))

# ══════════════════════════════════════════════
# SECCIÓN 2 — OLN CONNECT
# ══════════════════════════════════════════════
story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))
story.append(Paragraph("02 · OLN CONNECT", s_label))
story.append(Paragraph("Gestión de redes sociales", s_h2b))

story.append(Paragraph(
    "Una presencia digital activa y consistente en redes sociales. "
    "Nos encargamos del diseño, el contenido y la publicación para que "
    "OLN Connect se vea profesional todos los días — sin que tengas que hacerlo tú.",
    s_body
))

story.append(Paragraph("Planes disponibles", s_h3))

# Tabla de planes
plan_headers = ["", "Plan Básico", "Plan Crecimiento ⭐", "Plan Premium"]
plan_rows = [
    ["Posts / mes", "12", "20", "30"],
    ["Stories (3×sem)", "—", "✓", "✓"],
    ["Diseño de marca", "✓", "✓", "✓"],
    ["Copywriting", "✓", "✓", "✓"],
    ["Programación", "✓", "✓", "✓"],
    ["LinkedIn", "—", "✓", "✓"],
    ["Respuesta DMs", "—", "Lun–Vie", "Diario"],
    ["Hashtag & SEO", "—", "✓", "✓"],
    ["Reporte mensual", "✓", "✓", "✓"],
    ["PRECIO / MES", "$3,500", "$5,500", "$8,500"],
]

def cell(txt, bold=False, color=DARK, bg=None, align=TA_CENTER):
    style = S("c", fontName="Helvetica-Bold" if bold else "Helvetica",
              fontSize=9, textColor=color, alignment=align, leading=13)
    return Paragraph(txt, style)

table_data = [[cell(h, bold=True, color=WHITE if i > 0 else GRAY) for i, h in enumerate(plan_headers)]]
for row in plan_rows:
    is_price = row[0] == "PRECIO / MES"
    r = [cell(row[0], bold=is_price, color=DARK, align=TA_LEFT)]
    for v in row[1:]:
        r.append(cell(v, bold=is_price, color=BLUE if is_price else (GREEN if v=="✓" else DARK)))
    table_data.append(r)

from reportlab.lib import colors as rcolors
GREEN = rcolors.HexColor("#2d8a4e")

table_data2 = [[cell(h, bold=True, color=WHITE if i > 0 else GRAY) for i, h in enumerate(plan_headers)]]
for row in plan_rows:
    is_price = row[0] == "PRECIO / MES"
    r = [cell(row[0], bold=is_price, color=DARK, align=TA_LEFT)]
    for v in row[1:]:
        r.append(cell(v, bold=is_price, color=BLUE if is_price else (GREEN if v=="✓" else DARK)))
    table_data2.append(r)

t_planes = Table(table_data2, colWidths=[4*cm, 3.5*cm, 4*cm, 4*cm])
row_styles = []
for i, row in enumerate(plan_rows):
    bg = LGRAY if i % 2 == 0 else WHITE
    if row[0] == "PRECIO / MES":
        bg = colors.HexColor("#eff6ff")
    row_styles.append(("BACKGROUND", (0, i+1), (-1, i+1), bg))

t_planes.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),  (-1,0),  DARK),
    ("BACKGROUND",    (2,0),  (2,0),   BLUE),
    ("TEXTCOLOR",     (0,0),  (-1,0),  WHITE),
    ("FONTNAME",      (0,0),  (-1,0),  "Helvetica-Bold"),
    ("ALIGN",         (0,0),  (-1,-1), "CENTER"),
    ("ALIGN",         (0,0),  (0,-1),  "LEFT"),
    ("VALIGN",        (0,0),  (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0),  (-1,-1), 7),
    ("BOTTOMPADDING", (0,0),  (-1,-1), 7),
    ("LEFTPADDING",   (0,0),  (0,-1),  10),
    ("GRID",          (0,0),  (-1,-1), 0.3, colors.HexColor("#e5e7eb")),
    ("LINEBELOW",     (0,-1), (-1,-1), 1.5, BLUE),
] + row_styles))
story.append(t_planes)
story.append(Paragraph("MXN · IVA no incluido · Factura disponible", s_note))
story.append(Spacer(1, 20))

# ══════════════════════════════════════════════
# SECCIÓN 3 — RESUMEN INVERSIÓN
# ══════════════════════════════════════════════
story.append(HRFlowable(width="100%", thickness=1.5, color=DARK, spaceAfter=10))
story.append(Paragraph("RESUMEN DE INVERSIÓN", s_label))
story.append(Paragraph("Todo en un solo lugar", s_big))
story.append(Spacer(1, 6))

resumen_data = [
    [Paragraph("Servicio", S("rh", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE)),
     Paragraph("Tipo", S("rh2", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, alignment=TA_CENTER)),
     Paragraph("Inversión", S("rh3", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, alignment=TA_RIGHT))],
    [Paragraph("OLN Tires — Página web", S("r1", fontName="Helvetica", fontSize=10, textColor=DARK)),
     Paragraph("Pago único", S("r1t", fontName="Helvetica", fontSize=9, textColor=GRAY, alignment=TA_CENTER)),
     Paragraph("A confirmar", S("r1p", fontName="Helvetica-Bold", fontSize=10, textColor=RED, alignment=TA_RIGHT))],
    [Paragraph("OLN Connect — Plan Básico", S("r2", fontName="Helvetica", fontSize=10, textColor=DARK)),
     Paragraph("Mensual", S("r2t", fontName="Helvetica", fontSize=9, textColor=GRAY, alignment=TA_CENTER)),
     Paragraph("$3,500 MXN", S("r2p", fontName="Helvetica-Bold", fontSize=10, textColor=BLUE, alignment=TA_RIGHT))],
    [Paragraph("OLN Connect — Plan Crecimiento", S("r3", fontName="Helvetica-Bold", fontSize=10, textColor=DARK)),
     Paragraph("Mensual", S("r3t", fontName="Helvetica", fontSize=9, textColor=BLUE, alignment=TA_CENTER)),
     Paragraph("$5,500 MXN ⭐", S("r3p", fontName="Helvetica-Bold", fontSize=10, textColor=BLUE, alignment=TA_RIGHT))],
    [Paragraph("OLN Connect — Plan Premium", S("r4", fontName="Helvetica", fontSize=10, textColor=DARK)),
     Paragraph("Mensual", S("r4t", fontName="Helvetica", fontSize=9, textColor=GRAY, alignment=TA_CENTER)),
     Paragraph("$8,500 MXN", S("r4p", fontName="Helvetica-Bold", fontSize=10, textColor=BLUE, alignment=TA_RIGHT))],
]
t_resumen = Table(resumen_data, colWidths=[9*cm, 3.5*cm, 4*cm])
t_resumen.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),  (-1,0),  DARK),
    ("BACKGROUND",    (0,3),  (-1,3),  colors.HexColor("#eff6ff")),
    ("TEXTCOLOR",     (0,0),  (-1,0),  WHITE),
    ("ALIGN",         (0,0),  (-1,-1), "LEFT"),
    ("ALIGN",         (1,0),  (1,-1),  "CENTER"),
    ("ALIGN",         (2,0),  (2,-1),  "RIGHT"),
    ("VALIGN",        (0,0),  (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0),  (-1,-1), 9),
    ("BOTTOMPADDING", (0,0),  (-1,-1), 9),
    ("LEFTPADDING",   (0,0),  (-1,-1), 10),
    ("RIGHTPADDING",  (0,0),  (-1,-1), 10),
    ("GRID",          (0,0),  (-1,-1), 0.3, colors.HexColor("#e5e7eb")),
    ("LINEBELOW",     (0,3),  (-1,3),  1.5, BLUE),
]))
story.append(t_resumen)
story.append(Spacer(1, 20))

# ══════════════════════════════════════════════
# SECCIÓN 4 — PRÓXIMOS PASOS
# ══════════════════════════════════════════════
story.append(HRFlowable(width="100%", thickness=1.5, color=PINK, spaceAfter=10))
story.append(Paragraph("PRÓXIMOS PASOS", s_label))
story.append(Paragraph("¿Cómo arrancamos?", s_big))
story.append(Spacer(1, 6))

pasos = [
    ("01", "Confirmar propuesta y elegir plan", "Seleccionan el servicio que más les conviene en esta reunión."),
    ("02", "Recopilar materiales", "Logo, fotos, información del catálogo y datos de contacto."),
    ("03", "Arranque del proyecto", "OLN Tires: entrega en 3 semanas. OLN Connect: primer mes de contenido en 5 días."),
    ("04", "Revisión y ajustes", "Una ronda de correcciones incluida en ambos servicios."),
    ("05", "Publicación y seguimiento", "La página queda en vivo y las redes comienzan a publicar."),
]
pasos_data = []
for num, titulo, desc in pasos:
    pasos_data.append([
        Paragraph(num, S("pn", fontName="Helvetica-Bold", fontSize=18, textColor=RED, alignment=TA_CENTER)),
        Paragraph(f"<b>{titulo}</b><br/><font size=9 color='#888888'>{desc}</font>",
                  S("pd2", fontName="Helvetica", fontSize=10, textColor=DARK, leading=15))
    ])
t_pasos = Table(pasos_data, colWidths=[1.5*cm, 15*cm])
t_pasos.setStyle(TableStyle([
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING",   (1,0), (1,-1),  12),
    ("LINEBELOW",     (0,0), (-1,-2), 0.3, LGRAY),
]))
story.append(t_pasos)
story.append(Spacer(1, 20))

# ══════════════════════════════════════════════
# CIERRE
# ══════════════════════════════════════════════
story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=6))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))
story.append(Paragraph(
    "¿Listo para arrancar? Escríbenos y lo ponemos en marcha esta semana.",
    S("cl", fontName="Helvetica-Bold", fontSize=11, textColor=DARK, alignment=TA_CENTER, spaceAfter=4)
))
story.append(Paragraph("brota digital · brotadigital.mx", s_footer))

doc.build(story)
print(f"PDF generado: {OUTPUT}")

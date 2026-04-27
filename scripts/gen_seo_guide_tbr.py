from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = "/Users/ximevillalpando/src/brota-digital/guia-seo-thebakingroom.pdf"

PINK   = colors.HexColor("#e07b8f")
DARK   = colors.HexColor("#1a1a2e")
LIGHT  = colors.HexColor("#f5f5f5")
GRAY   = colors.HexColor("#888888")
GREEN  = colors.HexColor("#2d8a4e")
CREAM  = colors.HexColor("#fff8f0")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

style_brand    = ParagraphStyle("brand",    fontName="Helvetica-Bold",    fontSize=10,  textColor=PINK,  spaceAfter=2)
style_title    = ParagraphStyle("title",    fontName="Helvetica-Bold",    fontSize=22,  textColor=DARK,  spaceAfter=4,  leading=28)
style_subtitle = ParagraphStyle("subtitle", fontName="Helvetica",         fontSize=11,  textColor=GRAY,  spaceAfter=2)
style_section  = ParagraphStyle("section",  fontName="Helvetica-Bold",    fontSize=13,  textColor=PINK,  spaceBefore=16, spaceAfter=6)
style_body     = ParagraphStyle("body",     fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=16, spaceAfter=6)
style_bold     = ParagraphStyle("bold",     fontName="Helvetica-Bold",    fontSize=10,  textColor=DARK,  leading=16, spaceAfter=4)
style_note     = ParagraphStyle("note",     fontName="Helvetica-Oblique", fontSize=9,   textColor=GRAY,  leading=13, leftIndent=8, spaceAfter=4)
style_step     = ParagraphStyle("step",     fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=16, spaceAfter=3, leftIndent=16)
style_closing  = ParagraphStyle("closing",  fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=14, spaceAfter=4, alignment=TA_CENTER)
style_footer   = ParagraphStyle("footer",   fontName="Helvetica",         fontSize=8,   textColor=GRAY,  alignment=TA_CENTER)
style_tag      = ParagraphStyle("tag",      fontName="Helvetica-Bold",    fontSize=9,   textColor=PINK,  spaceAfter=2)

story = []

# Header
story.append(Paragraph("BROTA DIGITAL", style_brand))
story.append(Spacer(1, 4))
story.append(Paragraph("Tu página en Google", style_title))
story.append(Paragraph("Guía de SEO · The Baking Room® · thebakingroom.com.mx", style_subtitle))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=2, color=PINK, spaceAfter=12))

story.append(Paragraph(
    "Esta guía te explica qué es el SEO, qué ya tiene tu página y qué puedes hacer para que "
    "cada vez más personas te encuentren en Google sin pagar anuncios.",
    style_body
))
story.append(Spacer(1, 8))

# Sección 1
story.append(Paragraph("¿Qué es el SEO?", style_section))
story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=6))
story.append(Paragraph(
    "SEO significa <i>Search Engine Optimization</i> — en español: posicionamiento en buscadores. "
    "Es todo lo que hacemos para que tu página aparezca cuando alguien busca en Google cosas como "
    "<b>\"pasteles personalizados CDMX\"</b> o <b>\"pastel de cumpleaños Ciudad de México\"</b>.",
    style_body
))
story.append(Paragraph(
    "A diferencia de los anuncios pagados, el SEO trabaja de forma orgánica — "
    "no pagas por aparecer, pero toma tiempo (entre 4 y 12 semanas para ver resultados en páginas nuevas).",
    style_body
))
story.append(Spacer(1, 6))

# Sección 2
story.append(Paragraph("¿Qué ya tiene tu página?", style_section))
story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=8))

elementos = [
    ("🏷  Título optimizado",
     "The Baking Room® | Pasteles Artesanales Personalizados · Ciudad de México",
     "Es lo primero que ve Google y lo que aparece en la pestaña del navegador."),
    ("📝  Descripción",
     "Pastelería artesanal bajo pedido en Ciudad de México. Pasteles personalizados, florales, temáticos...",
     "Aparece debajo del título en los resultados de Google."),
    ("🔑  +70 palabras clave",
     "pasteles CDMX, pastel personalizado, vintage cake, aesthetic cakes, Polanco, Roma Norte...",
     "Le dice a Google de qué trata tu página y para quién es."),
    ("🔗  URL canónica",
     "https://thebakingroom.com.mx/",
     "Evita confusión cuando la página aparece en más de un lugar."),
    ("📊  Datos estructurados",
     "Tipo de negocio: Bakery · Calificación: 5/5 · Horario · Zona de servicio: CDMX",
     "Google puede mostrar esta información directamente en los resultados (ficha especial)."),
    ("🔒  HTTPS activado",
     "https://thebakingroom.com.mx",
     "El candado verde. Google premia las páginas seguras."),
]

for titulo, valor, nota in elementos:
    story.append(Paragraph(titulo, style_tag))
    story.append(Paragraph(valor, style_bold))
    story.append(Paragraph(nota, style_note))
    story.append(Spacer(1, 4))

story.append(Spacer(1, 6))

# Sección 3
story.append(Paragraph("Próximos pasos recomendados", style_section))
story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=8))

pasos = [
    ("1", "Conectar Google Search Console (gratis)",
     [
         "Entra a search.google.com/search-console",
         "Agrega tu dominio: thebakingroom.com.mx",
         "Verifica con el método DNS (Porkbun)",
         "En 3–7 días empieza a ver cuántas veces apareció tu página en Google",
     ],
     "Es la herramienta oficial de Google. Te muestra exactamente cómo te ven."),
    ("2", "Crear tu ficha en Google Business Profile (gratis)",
     [
         "Busca \"Google Business Profile\" en Google",
         "Registra: The Baking Room · Ciudad de México",
         "Agrega fotos, WhatsApp, horario y zona de entregas",
         "Pide a tus clientes que dejen reseñas",
     ],
     "Así apareces en Google Maps y en el panel lateral cuando buscan pasteles CDMX."),
    ("3", "Solicitar indexación de tu página",
     [
         "Entra a Google Search Console",
         "Clic en \"Inspeccionar URL\"",
         "Escribe: https://thebakingroom.com.mx/",
         "Clic en \"Solicitar indexación\"",
     ],
     "Le avisas a Google que la página existe para que la encuentre más rápido."),
]

for num, titulo, steps, nota in pasos:
    story.append(Paragraph(f"Paso {num} — {titulo}", style_bold))
    for s in steps:
        story.append(Paragraph(f"→  {s}", style_step))
    story.append(Paragraph(nota, style_note))
    story.append(Spacer(1, 8))

# Sección 4 — Tabla resumen
story.append(Paragraph("¿Cuándo veo resultados?", style_section))
story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=8))

tabla_data = [
    ["Acción", "Tiempo estimado"],
    ["Página indexada por Google", "1–2 semanas"],
    ["Primeras visitas orgánicas", "4–8 semanas"],
    ["Posiciones estables en Google", "3–6 meses"],
    ["Google Business activo", "Inmediato (con verificación)"],
]

tabla = Table(tabla_data, colWidths=[11*cm, 6*cm])
tabla.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), PINK),
    ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 10),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 9),
    ("TEXTCOLOR",     (0, 1), (-1, -1), DARK),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
    ("TOPPADDING",    (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING",   (0, 0), (-1, -1), 10),
]))
story.append(tabla)
story.append(Spacer(1, 12))

# Sección 5 — Consejo
story.append(Paragraph("💡  Consejo para mantener el SEO activo", style_section))
story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=6))
story.append(Paragraph(
    "Google premia las páginas que se actualizan. Algunas ideas sencillas:",
    style_body
))
consejos = [
    "Pide a tus clientes que dejen reseñas en Google Business",
    "Sube fotos nuevas a tu ficha de Google cada mes",
    "Comparte el link de tu página en Instagram y WhatsApp",
    "Cuando tengas ediciones de temporada (Navidad, San Valentín), avísanos para actualizar la página",
]
for c in consejos:
    story.append(Paragraph(f"→  {c}", style_step))
story.append(Spacer(1, 16))

# Cierre
story.append(HRFlowable(width="100%", thickness=1, color=PINK, spaceAfter=10))
story.append(Paragraph(
    "¿Tienes dudas? Escríbenos — con gusto te explicamos cualquier punto. ✨",
    style_closing
))
story.append(Paragraph("brota digital · brotadigital.mx", style_footer))

doc.build(story)
print(f"PDF generado: {OUTPUT}")

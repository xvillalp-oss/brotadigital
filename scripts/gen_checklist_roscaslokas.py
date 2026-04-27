from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER

OUTPUT = "/Users/ximevillalpando/src/brota-digital/checklist-roscas-lokas.pdf"

PINK   = colors.HexColor("#e32581")
DARK   = colors.HexColor("#1a1a2e")
LIGHT  = colors.HexColor("#f5f5f5")
GRAY   = colors.HexColor("#888888")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

style_brand    = ParagraphStyle("brand",    fontName="Helvetica-Bold",    fontSize=10,  textColor=PINK,  spaceAfter=2)
style_title    = ParagraphStyle("title",    fontName="Helvetica-Bold",    fontSize=22,  textColor=DARK,  spaceAfter=4,  leading=26)
style_subtitle = ParagraphStyle("subtitle", fontName="Helvetica",         fontSize=11,  textColor=GRAY,  spaceAfter=2)
style_section  = ParagraphStyle("section",  fontName="Helvetica-Bold",    fontSize=13,  textColor=PINK,  spaceBefore=16, spaceAfter=6)
style_item     = ParagraphStyle("item",     fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=16, spaceAfter=2, leftIndent=8)
style_note     = ParagraphStyle("note",     fontName="Helvetica-Oblique", fontSize=9,   textColor=GRAY,  leading=13, leftIndent=8, spaceAfter=2)
style_intro    = ParagraphStyle("intro",    fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=15, spaceAfter=8)
style_closing  = ParagraphStyle("closing",  fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=14, spaceAfter=4, alignment=TA_CENTER)
style_footer   = ParagraphStyle("footer",   fontName="Helvetica",         fontSize=8,   textColor=GRAY,  alignment=TA_CENTER)

CHECK = "☐  "

sections = [
    ("🖼  Marca e identidad", [
        (CHECK + "Logo en alta resolución (PNG con fondo transparente)", None),
        (CHECK + "Colores de tu marca (o dejarlo a criterio del diseñador)", None),
        (CHECK + "Tipografías que uses habitualmente", None),
        (CHECK + "Fotos de tus productos (roscas, postres, botanas) en buena calidad", "Mientras más fotos, mejor — son el corazón de tu catálogo"),
        (CHECK + "Foto tuya o de tu equipo (para generar confianza y conexión con clientes)", None),
    ]),
    ("📋  Catálogo de productos", [
        (CHECK + "Lista completa de productos con nombre y descripción breve", "Ej: Rosca de Reyes, Palomitas de colores, Esferas navideñas…"),
        (CHECK + "¿Tienes precios definidos o varían por pedido?", "Podemos poner precios fijos, rangos o solo 'solicita cotización'"),
        (CHECK + "Productos de temporada o ediciones limitadas (Reyes, Navidad, Día del Niño, etc.)", None),
        (CHECK + "¿Para qué ocasiones ofreces tus productos? (eventos, regalos, fiestas, bodas…)", None),
        (CHECK + "¿Haces entregas a domicilio? ¿En qué zonas de CDMX?", None),
        (CHECK + "¿Cuántos días de anticipación necesitas para un pedido?", None),
    ]),
    ("📞  Datos de contacto", [
        (CHECK + "Número de WhatsApp para pedidos (con clave de país: +52 55…)", None),
        (CHECK + "Correo electrónico (si tienes o quieres uno)", None),
        (CHECK + "¿Trabajas desde casa o tienes punto de recolección?", None),
        (CHECK + "Colonias o zonas de CDMX donde haces entregas", None),
        (CHECK + "Horario de atención y días disponibles", None),
        (CHECK + "Links de todas tus redes sociales (Instagram, Facebook, TikTok, etc.)", None),
    ]),
    ("⭐  Contenido de confianza", [
        (CHECK + "2 a 5 testimonios de clientes satisfechos (texto o capturas de pantalla)", None),
        (CHECK + "¿Tienes reseñas en Google? (para mostrarlas en la página)", None),
        (CHECK + "¿Algo que te haga diferente de otras rosquerías o pastelerías?", "Ej: receta familiar, ingredientes naturales, sin conservadores, diseños únicos…"),
    ]),
    ("🌐  Dominio y correo", [
        (CHECK + "¿Ya tienes dominio contratado? (Ej: roscaslokas.mx o roscaslokas.com)", "Si no, lo conseguimos juntos — costo aprox. $400–$500 MXN/año"),
        (CHECK + "¿Quieres un correo profesional? (Ej: hola@roscaslokas.mx)", "Costo adicional si aplica"),
    ]),
    ("⚙️  Funcionalidades", [
        (CHECK + "¿Quieres que los clientes puedan hacer pedidos desde la página?", "Puede ser un formulario simple o botón directo a WhatsApp"),
        (CHECK + "¿Quieres galería de fotos por categoría de producto?", None),
        (CHECK + "¿Algo más que quieras incluir? (Mapa, sección de eventos, blog…)", None),
    ]),
]

story = []

story.append(Paragraph("BROTA DIGITAL", style_brand))
story.append(Spacer(1, 4))
story.append(Paragraph("Checklist para tu página web", style_title))
story.append(Paragraph("Roscas Lokas CDMX · Recopilación de información", style_subtitle))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=2, color=PINK, spaceAfter=12))

story.append(Paragraph(
    "Para diseñar y desarrollar tu página web necesitamos que nos compartas la siguiente información. "
    "No te preocupes si no tienes todo — cuéntanos y lo resolvemos juntos. "
    "Entre más completa la recibamos, más rápido arrancamos.",
    style_intro
))
story.append(Spacer(1, 8))

for section_title, items in sections:
    story.append(Paragraph(section_title, style_section))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=6))
    for item_text, note in items:
        story.append(Paragraph(item_text, style_item))
        if note:
            story.append(Paragraph(note, style_note))
    story.append(Spacer(1, 4))

story.append(Spacer(1, 16))
story.append(HRFlowable(width="100%", thickness=1, color=PINK, spaceAfter=10))
story.append(Paragraph(
    "Puedes mandarnos todo por WhatsApp o correo. Con gusto resolvemos cualquier duda. ✨",
    style_closing
))
story.append(Paragraph("brota digital · brotadigital.mx", style_footer))

doc.build(story)
print(f"PDF generado: {OUTPUT}")

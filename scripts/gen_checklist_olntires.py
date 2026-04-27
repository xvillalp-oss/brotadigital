from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER

OUTPUT = "/Users/ximevillalpando/src/brota-digital/checklist-olntires.pdf"

RED   = colors.HexColor("#e01010")
DARK  = colors.HexColor("#1a1a2e")
LIGHT = colors.HexColor("#f5f5f5")
GRAY  = colors.HexColor("#888888")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

style_brand    = ParagraphStyle("brand",    fontName="Helvetica-Bold",    fontSize=10,  textColor=RED,   spaceAfter=2)
style_title    = ParagraphStyle("title",    fontName="Helvetica-Bold",    fontSize=22,  textColor=DARK,  spaceAfter=4,  leading=26)
style_subtitle = ParagraphStyle("subtitle", fontName="Helvetica",         fontSize=11,  textColor=GRAY,  spaceAfter=2)
style_section  = ParagraphStyle("section",  fontName="Helvetica-Bold",    fontSize=13,  textColor=RED,   spaceBefore=16, spaceAfter=6)
style_item     = ParagraphStyle("item",     fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=16, spaceAfter=2, leftIndent=8)
style_note     = ParagraphStyle("note",     fontName="Helvetica-Oblique", fontSize=9,   textColor=GRAY,  leading=13, leftIndent=8, spaceAfter=2)
style_intro    = ParagraphStyle("intro",    fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=15, spaceAfter=8)
style_closing  = ParagraphStyle("closing",  fontName="Helvetica",         fontSize=10,  textColor=DARK,  leading=14, spaceAfter=4, alignment=TA_CENTER)
style_footer   = ParagraphStyle("footer",   fontName="Helvetica",         fontSize=8,   textColor=GRAY,  alignment=TA_CENTER)

CHECK = "☐  "

sections = [
    ("Marca e identidad", [
        (CHECK + "Logo en alta resolución (PNG con fondo transparente)", None),
        (CHECK + "Colores oficiales de la marca (códigos hex o Pantone)", None),
        (CHECK + "Manual de marca o lineamientos visuales (si existe)", None),
        (CHECK + "Tipografías que usan habitualmente", None),
    ]),
    ("Catálogo y productos", [
        (CHECK + "PDF de catálogos de TODAS las marcas que distribuyen", "Gladiator, RoadX, Empire, Pegasus, JK Tyre, Benchmark, Royal Black, Rockbuster, StarStone, GMX — uno por marca si es posible"),
        (CHECK + "Imágenes de TODOS los productos (una foto por referencia mínimo)", "Idealmente en fondo blanco o neutro — las usaremos en el catálogo online"),
        (CHECK + "Descripción de cada producto: nombre, medida, uso recomendado y características clave", "Ej: Gladiator QR99 PD · 11R22.5 · Tracción para camión · Alta resistencia en carretera y terracería"),
        (CHECK + "Actualización de marcas distribuidas (agregar o quitar alguna)", None),
        (CHECK + "¿Publican precios en la página o solo cotización?", "Podemos poner precios, rangos o botón directo a WhatsApp"),
        (CHECK + "Medidas y especificaciones técnicas más vendidas", "Para destacarlas en el catálogo online"),
        (CHECK + "Productos con entrega inmediata vs. pedido especial", None),
    ]),
    ("Datos de la empresa", [
        (CHECK + "Razón social completa", "Outlet Llantas del Norte S.A. de C.V. — confirmar"),
        (CHECK + "Dirección física o zonas de cobertura", None),
        (CHECK + "Teléfono y WhatsApp para cotizaciones (con clave de país: +52 81...)", None),
        (CHECK + "Correo electrónico de contacto", None),
        (CHECK + "Horario de atención y días disponibles", None),
        (CHECK + "Links de redes sociales actuales (Instagram, Facebook, LinkedIn)", None),
    ]),
    ("Contenido de la empresa", [
        (CHECK + "Texto de 'Quiénes somos' o historia de OLN Tires", "10+ años en el mercado — ¿cómo empezaron?"),
        (CHECK + "Fotos del equipo, almacén u operación en campo", "Transmiten confianza y profesionalismo"),
        (CHECK + "Testimonios o clientes destacados (flotillas, plantas, empresas)", None),
        (CHECK + "Logros, certificaciones o reconocimientos", None),
        (CHECK + "¿Qué los hace diferentes de otras distribuidoras?", "Precio directo, entrega 24h, asesoría especializada..."),
    ]),
    ("Dominio y correo", [
        (CHECK + "¿Usamos olntires.com o quieren un dominio diferente?", "Si quieren .mx o variante, lo conseguimos juntos"),
        (CHECK + "¿Quién tiene acceso al dominio actual?", "Necesitamos poder modificar los registros DNS"),
        (CHECK + "¿Quieren correo profesional? (Ej: ventas@olntires.com)", "Costo adicional si aplica"),
    ]),
    ("Funcionalidades", [
        (CHECK + "¿Los clientes pueden solicitar cotización desde la página?", "Formulario o botón directo a WhatsApp"),
        (CHECK + "¿Quieren filtros por categoría en el catálogo? (Camión / Agrícola / Industrial)", None),
        (CHECK + "¿Quieren integrar los PDFs de catálogo descargables?", "El cliente entra, ve el catálogo y lo descarga en PDF"),
        (CHECK + "¿Quieren un mapa de ubicación o zonas de entrega?", None),
        (CHECK + "¿Algo más que quieran incluir? (Blog, calculadora de medidas, etc.)", None),
    ]),
]

story = []

story.append(Paragraph("BROTA DIGITAL", style_brand))
story.append(Spacer(1, 4))
story.append(Paragraph("Checklist para tu página web", style_title))
story.append(Paragraph("OLN Tires · Outlet Llantas del Norte S.A. de C.V.", style_subtitle))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=12))

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
story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=10))
story.append(Paragraph(
    "Puedes mandarnos todo por WhatsApp o correo. Con gusto resolvemos cualquier duda.",
    style_closing
))
story.append(Paragraph("brota digital · brotadigital.mx", style_footer))

doc.build(story)
print(f"PDF generado: {OUTPUT}")

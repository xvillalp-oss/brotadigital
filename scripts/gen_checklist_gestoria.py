from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/Users/ximevillalpando/src/brota-digital/checklist-gestoria-migratoria.pdf"

PINK = colors.HexColor("#e32581")
DARK = colors.HexColor("#1a1a2e")
LIGHT_GRAY = colors.HexColor("#f5f5f5")
MID_GRAY = colors.HexColor("#888888")
WHITE = colors.white

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

style_title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22, textColor=DARK, spaceAfter=4, leading=26)
style_subtitle = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=11, textColor=MID_GRAY, spaceAfter=2)
style_brand = ParagraphStyle("brand", fontName="Helvetica-Bold", fontSize=10, textColor=PINK, spaceAfter=2)
style_section = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=13, textColor=PINK, spaceBefore=16, spaceAfter=6)
style_item = ParagraphStyle("item", fontName="Helvetica", fontSize=10, textColor=DARK, leading=16, spaceAfter=2, leftIndent=8)
style_note = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=9, textColor=MID_GRAY, leading=13, leftIndent=8, spaceAfter=2)
style_footer = ParagraphStyle("footer", fontName="Helvetica", fontSize=8, textColor=MID_GRAY, alignment=TA_CENTER)

CHECK = "☐  "

sections = [
    ("🖼  Marca e identidad", [
        (CHECK + "Logo en alta resolución (PNG con fondo transparente)", None),
        (CHECK + "Colores de tu marca (o indicar si prefieres que los propongamos)", None),
        (CHECK + "Tipografías que uses (o dejarlo a criterio del diseñador)", None),
    ]),
    ("📋  Contenido de la página", [
        (CHECK + "Lista completa de servicios con descripción breve de cada uno", "Ej: Visa USA, Visa Canadá, Pasaporte Mexicano, Green Card, etc."),
        (CHECK + "¿Quieres mostrar precios o solo 'solicita cotización'?", None),
        (CHECK + "Texto para la sección 'Quiénes somos' (historia, misión, valores)", None),
        (CHECK + "Foto tuya o del equipo (genera confianza — muy importante en este giro)", None),
        (CHECK + "2 a 5 testimonios de clientes satisfechos (texto, no necesita ser de Google)", None),
        (CHECK + "Preguntas frecuentes que te hacen tus clientes (FAQ)", "Ej: ¿Cuánto tarda el trámite? ¿Trabajan en todo México? ¿Cómo garantizan que no es fraude?"),
    ]),
    ("📞  Datos de contacto", [
        (CHECK + "Número de WhatsApp (con clave de país: +52 55...)", None),
        (CHECK + "Correo electrónico de contacto", None),
        (CHECK + "¿Tienen oficina física o son 100% remotos?", None),
        (CHECK + "Dirección (si aplica, para aparecer en Google Maps)", None),
        (CHECK + "Horario de atención", None),
        (CHECK + "Links de redes sociales (Instagram, Facebook, TikTok, etc.)", None),
    ]),
    ("🌐  Dominio y correo", [
        (CHECK + "¿Ya tienes dominio contratado? (Ej: okgestoria.mx)", "Si no, lo conseguimos juntos — costo aproximado $400–$500 MXN/año"),
        (CHECK + "¿Quieres correo profesional? (Ej: hola@okgestoria.mx)", "Costo adicional si aplica"),
    ]),
    ("⚙️  Funcionalidades", [
        (CHECK + "¿Quieres formulario de contacto además del botón de WhatsApp?", None),
        (CHECK + "¿Quieres sección de blog/artículos? (Muy útil para SEO)", "Ej: 'Cómo tramitar tu visa canadiense en 2026'"),
        (CHECK + "¿Alguna otra función especial? (Calculadora, calendario, etc.)", None),
    ]),
]

story = []

# Header block
story.append(Paragraph("BROTA DIGITAL", style_brand))
story.append(Spacer(1, 4))
story.append(Paragraph("Checklist para tu página web", style_title))
story.append(Paragraph("OK Gestoría Migratoria · Recopilación de información", style_subtitle))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=2, color=PINK, spaceAfter=12))

intro = Paragraph(
    "Para poder diseñar y desarrollar tu página web necesitamos que nos compartas la siguiente información. "
    "Entre más completa la recibamos, más rápido podemos arrancar. Si no tienes algo o tienes dudas, "
    "puedes avisarnos y lo resolvemos juntos.",
    ParagraphStyle("intro", fontName="Helvetica", fontSize=10, textColor=DARK, leading=15, spaceAfter=8)
)
story.append(intro)
story.append(Spacer(1, 8))

for section_title, items in sections:
    story.append(Paragraph(section_title, style_section))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=6))
    for item_text, note in items:
        story.append(Paragraph(item_text, style_item))
        if note:
            story.append(Paragraph(note, style_note))
    story.append(Spacer(1, 4))

story.append(Spacer(1, 16))
story.append(HRFlowable(width="100%", thickness=1, color=PINK, spaceAfter=10))

story.append(Paragraph(
    "Puedes mandarnos esta información por WhatsApp o correo. Con gusto resolvemos cualquier duda.",
    ParagraphStyle("closing", fontName="Helvetica", fontSize=10, textColor=DARK, leading=14, spaceAfter=4, alignment=TA_CENTER)
))
story.append(Paragraph(
    "brota digital · brotadigital.mx",
    style_footer
))

doc.build(story)
print(f"PDF generado: {OUTPUT}")

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER

OUTPUT = "/Users/ximevillalpando/src/brota-digital/checklist-maky.pdf"

PINK  = colors.HexColor("#e8637a")
DARK  = colors.HexColor("#1a1a2e")
LIGHT = colors.HexColor("#f5f5f5")
GRAY  = colors.HexColor("#888888")

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
    ("Marca e identidad", [
        (CHECK + "Logo en alta resolución (PNG con fondo transparente)", "El que usan en Instagram o cualquier versión que tengan guardada"),
        (CHECK + "Colores oficiales de la marca (el rosa/coral del logo y cualquier otro color que usen)", None),
        (CHECK + "Tipografía o fuente que usan en sus publicaciones", "Si no saben el nombre, manden una captura y lo identificamos"),
        (CHECK + "Nombre oficial del negocio para la página", "Ej: Creaciones Maky, Maky Accesorios, etc."),
        (CHECK + "Frase o slogan (si tienen uno)", None),
    ]),
    ("Catalogo y productos", [
        (CHECK + "Fotos de TODOS sus productos, una por referencia minimo", "Idealmente en fondo blanco o neutro — para verlas bien en el catalogo online"),
        (CHECK + "Nombre de cada producto o coleccion", "Ej: Mony rosa pastel, Diadema flores primavera, Colita lazo doble..."),
        (CHECK + "Descripcion breve de cada producto", "Ej: Mono de grosgrain, medida 8 cm, disponible en 6 colores"),
        (CHECK + "Precio de cada producto (o rango de precios)", "Si no quieren mostrar precios, lo manejamos con boton de WhatsApp"),
        (CHECK + "Categorias en las que dividen sus productos", "Ej: Monos, Diademas, Colitas, Sets, Colecciones — lo que tenga mas sentido para ustedes"),
        (CHECK + "Colores o tallas disponibles por producto (si aplica)", "Para que la clienta pueda elegir desde la pagina"),
        (CHECK + "Productos disponibles de inmediato vs. por pedido", "Para avisarle al cliente cuanto tiempo esperar"),
        (CHECK + "Cuanto tardan en hacer un pedido personalizado", "Ej: 3-5 dias habiles"),
    ]),
    ("Datos del negocio", [
        (CHECK + "Nombre completo para contacto", "Maky o el nombre que quieran que aparezca"),
        (CHECK + "Numero de WhatsApp para pedidos (con clave de pais: +52)", None),
        (CHECK + "Correo electronico de contacto (si tienen)", None),
        (CHECK + "Ciudad o zona donde hacen entregas", "Ej: Cancun, Quintana Roo — envios a toda la republica"),
        (CHECK + "Opciones de entrega: recoleccion, envio local, paqueteria nacional", None),
        (CHECK + "Horario en que responden pedidos", "Ej: Lun-Vie 10am-6pm"),
        (CHECK + "Link de Instagram y cualquier otra red social que usen", None),
    ]),
    ("Contenido del negocio", [
        (CHECK + "Historia corta de Creaciones Maky", "Como empezaron, cuanto tiempo llevan, que los hace especiales"),
        (CHECK + "Fotos del proceso o taller (si tienen)", "Manos trabajando, materiales, maquina de coser — generan mucha confianza"),
        (CHECK + "Fotos del producto puesto (ninas usando los accesorios)", "Las mejores para vender — si tienen en Instagram, podemos usarlas"),
        (CHECK + "Testimonios o resenias de clientas (texto o capturas)", None),
        (CHECK + "Ocasiones especiales que trabajan", "Ej: bautizos, XV anos, baby shower, dia del nino, regreso a clases"),
    ]),
    ("Dominio y correo", [
        (CHECK + "Nombre de dominio que quieren para la pagina", "Ej: creacionesmaky.com, creacionesmaky.mx — buscamos juntas cual esta disponible"),
        (CHECK + "Si ya tienen dominio comprado, quien lo administra", "Para configurar correctamente"),
        (CHECK + "Quieren correo profesional con su dominio?", "Ej: hola@creacionesmaky.com — tiene costo adicional segun el proveedor"),
    ]),
    ("Funcionalidades de la pagina", [
        (CHECK + "Las clientas compran directo en la pagina o por WhatsApp?", "Podemos hacer catalogo con boton de WhatsApp (mas sencillo) o tienda con carrito de compras (mas complejo)"),
        (CHECK + "Quieren filtros por categoria, color o coleccion?", None),
        (CHECK + "Quieren mostrar sus colecciones de temporada (Navidad, San Valentin, etc.)?", None),
        (CHECK + "Quieren galeria tipo Instagram embebida en la pagina?", "Muestra sus publicaciones recientes automaticamente"),
        (CHECK + "Quieren formulario de contacto ademas de WhatsApp?", None),
        (CHECK + "Algo mas que quieran incluir?", "Blog, guia de tamanos, cuidado de los accesorios, etc."),
    ]),
]

story = []

story.append(Paragraph("BROTA DIGITAL", style_brand))
story.append(Spacer(1, 4))
story.append(Paragraph("Checklist para tu pagina web", style_title))
story.append(Paragraph("Creaciones Maky · Accesorios para ninas", style_subtitle))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=2, color=PINK, spaceAfter=12))

story.append(Paragraph(
    "Para disenar y desarrollar tu pagina web necesitamos que nos compartas la siguiente informacion. "
    "No te preocupes si no tienes todo de inmediato — cuentanos y lo resolvemos juntas. "
    "Entre mas completa la recibamos, mas rapido arrancamos.",
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
    "Puedes mandarnos todo por WhatsApp o correo. Con gusto resolvemos cualquier duda.",
    style_closing
))
story.append(Paragraph("brota digital · brotadigital.mx", style_footer))

doc.build(story)
print(f"PDF generado: {OUTPUT}")

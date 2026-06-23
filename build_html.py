#!/usr/bin/env python3
"""
Genera la version HTML autocontenida del template "Marketing" (mismas 13 slides
que el .pptx), para inspeccionar en navegador y conectar a herramientas de diseno.
Armin Grotesk embebida en base64, logos SVG inline. Coordenadas = pulgadas x 96px.
"""
import os, base64

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "perpetual-fintech.html")

# --- fuentes OTF -> @font-face base64 ---
FONTS = [("Normal", 300), ("Regular", 400), ("Semi_Bold", 600), ("Black", 800)]
faces = []
for name, weight in FONTS:
    data = open(os.path.join(ASSETS, "fonts", f"ArminGrotesk_{name}.otf"), "rb").read()
    b64 = base64.b64encode(data).decode()
    faces.append("@font-face{font-family:'Armin Grotesk';font-weight:%d;font-display:swap;"
                 "src:url(data:font/otf;base64,%s) format('opentype');}" % (weight, b64))
FONT_FACES = "\n".join(faces)


def _svg(path):
    return open(os.path.join(ASSETS, "logo", path)).read().split("?>", 1)[-1].strip()
LOGO_COLOR, LOGO_DARK = _svg("perpetual-color.svg"), _svg("perpetual-dark.svg")

# --- tokens ---
ACCENT, ACCENT2, YELLOW = "#1a56db", "#f97316", "#fbb900"
BGD, TEXT, DIM, MUTED = "#0b1220", "#111827", "#374151", "#6b7280"
SURFACE, SURFACE2, BORDER, WHITE, DBE4FF = "#f8f9fc", "#eef1f8", "#dde1ef", "#ffffff", "#dbe4ff"
PXIN = 96


def _p(v):
    return f"{v * PXIN:.1f}px"


def box(x, y, w, h, fill=None, r=0, oval=False, shadow=False, line=None):
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
    st += "border-radius:50%;" if oval else (f"border-radius:{r}px;" if r else "")
    if fill: st += f"background:{fill};"
    if line: st += f"border:1px solid {line};"
    if shadow: st += "box-shadow:0 8px 26px rgba(20,40,90,.13);"
    return f'<div style="{st}"></div>'


def txt(x, y, w, h, content, size, color=TEXT, weight=400, align="left",
        valign="top", spacing=None, upper=False, lh=1.1):
    just = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}[valign]
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
          f"display:flex;flex-direction:column;justify-content:{just};overflow:hidden;"
          f"font-size:{size*1.333:.1f}px;color:{color};font-weight:{weight};"
          f"text-align:{align};line-height:{lh};")
    if align == "center": st += "align-items:center;"
    if spacing: st += f"letter-spacing:{spacing}px;"
    if upper: st += "text-transform:uppercase;"
    return f'<div style="{st}">{content}</div>'


def logo(x, y, w, dark=False):
    svg = LOGO_DARK if dark else LOGO_COLOR
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};"
    return f'<div class="lg" style="{st}">{svg}</div>'


def hexagon(x, y, size, fill):
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(size)};height:{_p(size)};"
          f"background:{fill};clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%);")
    return f'<div style="{st}"></div>'


def blob(x, y, d, fill):
    return box(x, y, d, d, fill=fill, oval=True)


def pill(x, y, w, label, fill=ACCENT, fg=WHITE, arrow=True):
    out = [box(x, y, w, 0.62, fill=fill, r=31, shadow=True),
           txt(x + 0.34, y, w - 1.0, 0.62, label, 11.5, fg, 600, "left", "middle",
               spacing=0.8, upper=True)]
    if arrow:
        out.append(box(x + w - 0.74, y + 0.1, 0.42, 0.42, fill=WHITE, oval=True))
        out.append(txt(x + w - 0.74, y + 0.02, 0.42, 0.42, "&rsaquo;", 17, fill, 800, "center", "middle"))
    return "".join(out)


def photo_ph(x, y, w, h, r=12, tint="#E3ECFB"):
    d = min(w, h) * 0.24
    cxp, cyp = x + w / 2, y + h / 2
    return (box(x, y, w, h, fill=tint, r=r)
            + box(cxp - d / 2, cyp - d / 2, d, d, fill=WHITE, oval=True)
            + box(cxp - d * 0.16, cyp - d * 0.16, d * 0.32, d * 0.32, fill=ACCENT, oval=True))


def tool_icon(x, y, d, fill):
    return box(x, y, d, d, fill=fill, oval=True) + hexagon(x + d * 0.3, y + d * 0.3, d * 0.4, WHITE)


def graphic(x, y, w, h, tint="#DBE7FB", variant="abstract", r=12, shadow=False):
    """Grafico de marca (en vez de foto): composicion abstracta on-brand.
    En Perpetual no usamos fotos de personas salvo en la slide de equipo."""
    out = [box(x, y, w, h, fill=tint, r=r, shadow=shadow)]
    cx, cy = x + w / 2, y + h / 2
    if variant == "growth":
        n, bw, gap = 4, w * 0.13, w * 0.06
        total = n * bw + (n - 1) * gap
        bx, base = cx - total / 2, y + h * 0.8
        cols = [ACCENT, ACCENT2, YELLOW, ACCENT]
        for i in range(n):
            bh = h * (0.16 + 0.13 * i)
            out.append(box(bx + i * (bw + gap), base - bh, bw, bh, fill=cols[i], r=4))
        out.append(box(cx - w * 0.3, y + h * 0.16, h * 0.2, h * 0.2, fill=ACCENT, oval=True))
        out.append(hexagon(cx + w * 0.16, y + h * 0.14, h * 0.16, YELLOW))
    elif variant == "quote":
        out.append(txt(x, y + h * 0.06, w, h * 0.45, "&ldquo;", 92, ACCENT, 800, "center"))
        out.append(txt(x, y + h * 0.62, w, h * 0.2,
                       "&#9733; &#9733; &#9733; &#9733; &#9733;", 17, YELLOW, 700, "center"))
    else:  # abstract: circulos + hexagono de marca
        out.append(box(cx - w * 0.28, cy - h * 0.16, h * 0.34, h * 0.34, fill=ACCENT, oval=True))
        out.append(box(cx + w * 0.03, cy - h * 0.02, h * 0.22, h * 0.22, fill=ACCENT2, oval=True))
        out.append(box(cx - w * 0.02, cy + h * 0.16, h * 0.13, h * 0.13, fill=YELLOW, oval=True))
        out.append(hexagon(cx + w * 0.12, cy - h * 0.26, h * 0.17, WHITE))
    return "".join(out)


def title(runs, x=0.7, y=0.7, w=7.5, size=33):
    return logo(0.6, 0.5, 1.15) + txt(x, y + 0.55, w, 1.2, runs, size, TEXT, 800, lh=1.0)


def footer(page):
    return (logo(0.55, 7.02, 0.92)
            + txt(1.75, 7.0, 7, 0.3, "Confidencial &middot; Perpetual Technologies &copy; 2026",
                  8.5, MUTED, 400, "left", "middle")
            + txt(11.7, 7.0, 1.1, 0.3, str(page).zfill(2), 8.5, MUTED, 400, "right", "middle"))


def AC(t):  # helper: envuelve en span de acento
    return f'<span style="color:{ACCENT}">{t}</span>'


# --- paleta de datos (graficas) ---
DATA = [ACCENT, ACCENT2, "#059669", YELLOW, "#7e22ce", MUTED]


def bars(x, y, w, h, vals, colors=None, gap=0.12, r=4):
    """Barras verticales. vals: lista de numeros (se normalizan)."""
    colors = colors or DATA
    n = len(vals)
    bw = (w - gap * (n - 1)) / n
    mx = max(vals) or 1
    out = []
    for i, v in enumerate(vals):
        bh = v / mx * h
        out.append(box(x + i * (bw + gap), y + h - bh, bw, bh,
                       fill=colors[i % len(colors)], r=r))
    return "".join(out)


def donut(x, y, d, segs, hole=0.58, track="#eef1f8"):
    """Donut con conic-gradient. segs: lista de (valor, color)."""
    total = sum(v for v, _ in segs) or 1
    stops, acc = [], 0.0
    for v, c in segs:
        a0 = acc / total * 360
        acc += v
        a1 = acc / total * 360
        stops.append(f"{c} {a0:.1f}deg {a1:.1f}deg")
    grad = ",".join(stops)
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(d)};height:{_p(d)};"
          f"border-radius:50%;background:conic-gradient({grad});"
          f"-webkit-mask:radial-gradient(circle, transparent {hole*50:.0f}%, #000 {hole*50:.0f}%);"
          f"mask:radial-gradient(circle, transparent {hole*50:.0f}%, #000 {hole*50:.0f}%);")
    return f'<div style="{st}"></div>'


# ===========================================================================
# Slides — Template "Financial Technology (fintech)" en marca Perpetual
# Coords = pulgadas x 96px. Sin fotos de personas: paneles de marca tintados.
# ===========================================================================
def initials_card(x, y, w, name, role, ini, tint="#DBE7FB"):
    """Tarjeta de perfil SIN foto: circulo con iniciales + nombre + rol."""
    return (box(x, y, w, 1.55, fill=WHITE, r=16, shadow=True, line=BORDER)
            + blob(x + 0.32, y + 0.43, 0.7, ACCENT)
            + txt(x + 0.32, y + 0.43, 0.7, 0.7, ini, 16, WHITE, 800, "center", "middle")
            + txt(x + 1.25, y + 0.42, w - 1.4, 0.35, name, 13.5, TEXT, 600)
            + txt(x + 1.25, y + 0.82, w - 1.4, 0.3, role, 10, ACCENT, 600, upper=True, spacing=0.5))


def brand_panel(x, y, w, h, tint, variant="abstract", label=None):
    out = [graphic(x, y, w, h, tint=tint, variant=variant, r=14, shadow=True)]
    if label:
        out.append(box(x + 0.3, y + h - 0.62, w - 0.6, 0.36, fill=WHITE, r=18))
        out.append(txt(x + 0.3, y + h - 0.62, w - 0.6, 0.36, label, 9.5, ACCENT, 600,
                       "center", "middle", spacing=0.6, upper=True))
    return "".join(out)


def hex_icon(x, y, d, fill):
    return hexagon(x, y, d, fill) + box(x + d * 0.34, y + d * 0.34, d * 0.32, d * 0.32, fill=WHITE, oval=True)


# 1. Portada -----------------------------------------------------------------
def s01():
    return (box(0, 4.7, 13.333, 2.8, fill=ACCENT)
            + blob(9.2, -1.0, 3.3, YELLOW) + blob(11.7, 2.1, 1.9, ACCENT2) + blob(8.2, 1.4, 3.4, ACCENT)
            + hexagon(8.75, 2.25, 2.0, WHITE) + box(9.45, 2.9, 0.66, 0.66, fill=ACCENT, oval=True)
            + blob(11.5, 4.6, 0.8, YELLOW)
            + txt(12.35, 0.55, 0.7, 0.6, "+", 28, ACCENT, 800)
            + logo(0.7, 0.7, 1.5)
            + txt(0.65, 1.55, 7.2, 2.0, f"Financial<br>{AC('Technology.')}", 46, TEXT, 800, lh=0.98)
            + txt(0.7, 3.5, 6.6, 0.4, "Tecnologia financiera para escalar tu negocio",
                  13, DIM, 600)
            + txt(0.7, 3.95, 6.6, 0.7, "Plataformas de pagos, datos e inteligencia para decisiones financieras mas rapidas.",
                  12.5, MUTED, 400, lh=1.3)
            # tarjeta de perfil sin foto, sobre la banda azul
            + box(8.3, 5.15, 4.3, 1.45, fill=WHITE, r=16, shadow=True)
            + blob(8.62, 5.5, 0.78, ACCENT)
            + txt(8.62, 5.5, 0.78, 0.78, "MC", 17, WHITE, 800, "center", "middle")
            + txt(9.65, 5.5, 2.7, 0.32, "Mariana Castro", 13.5, TEXT, 700)
            + txt(9.65, 5.88, 2.7, 0.3, "Directora de Producto Fintech", 10, ACCENT, 600, upper=True, spacing=0.4)
            + pill(0.7, 5.5, 2.9, "Saber mas", fill=WHITE, fg=ACCENT))


# 2. Unlocking Wealth --------------------------------------------------------
def s02():
    return (title(f"Potencial de riqueza con<br>{AC('estrategias inteligentes.')}", size=29)
            + txt(0.7, 2.65, 5.0, 1.4,
                  "Convertimos datos transaccionales en estrategias de inversion y ahorro que hacen crecer el capital de tus clientes.",
                  13, MUTED, 400, lh=1.4)
            + brand_panel(0.7, 4.35, 2.55, 2.05, "#DBE7FB", "abstract", "Inversion")
            + brand_panel(3.45, 4.35, 2.55, 2.05, "#FDE9D6", "abstract", "Ahorro")
            # card azul "Explorar"
            + box(6.9, 2.5, 5.7, 4.0, fill=ACCENT, r=16, shadow=True)
            + hex_icon(7.4, 2.95, 0.9, WHITE)
            + txt(7.4, 4.0, 4.8, 0.5, "Gestion patrimonial digital", 17, WHITE, 700)
            + txt(7.4, 4.6, 4.8, 1.0, "Portafolios automatizados y alertas en tiempo real, con cumplimiento normativo integrado.",
                  12, DBE4FF, 400, lh=1.35)
            + pill(7.4, 5.7, 2.7, "Explorar", fill=WHITE, fg=ACCENT)
            + footer(2))


# 3. Redefining Growth -------------------------------------------------------
def s03():
    out = [title(f"Redefiniendo el {AC('crecimiento.')}"),
           txt(0.7, 1.95, 6.5, 0.5, "Resultados que respaldan nuestra plataforma fintech.",
               13, MUTED, 400)]
    stats = [("1.200+", "Ingresos recurrentes (USD K)", ACCENT),
             ("45M", "Transacciones procesadas", ACCENT2),
             ("76K+", "Cuentas activas", "#059669")]
    for i, (v, lbl, col) in enumerate(stats):
        x = 0.7 + i * 2.15
        out += [box(x, 2.8, 1.95, 1.9, fill=SURFACE, r=14, line=BORDER),
                txt(x + 0.3, 3.05, 1.55, 0.7, v, 30, col, 800),
                txt(x + 0.3, 3.95, 1.55, 0.65, lbl, 9.5, MUTED, 600, lh=1.2)]
    out += [box(7.45, 2.8, 5.15, 3.9, fill=ACCENT, r=16, shadow=True),
            hex_icon(7.95, 3.25, 0.85, WHITE),
            txt(7.95, 4.25, 4.3, 0.5, "Escala sin friccion", 17, WHITE, 700),
            txt(7.95, 4.85, 4.3, 1.4,
                "Infraestructura cloud que crece con tu volumen: APIs de pago, conciliacion automatica y reportes en vivo.",
                12, DBE4FF, 400, lh=1.4),
            footer(3)]
    return "".join(out)


# 4. Secure Your Future ------------------------------------------------------
def s04():
    return (title(f"Asegura tu {AC('futuro financiero.')}", size=30)
            + txt(0.7, 2.7, 5.0, 1.3,
                  "Crecimiento sostenido y proteccion del capital con modelos de riesgo verificados periodicamente.",
                  13, MUTED, 400, lh=1.4)
            + blob(0.95, 4.35, 0.4, ACCENT) + txt(1.55, 4.35, 4.5, 0.4, "Cifrado de nivel bancario", 12, DIM, 600)
            + blob(0.95, 4.95, 0.4, ACCENT) + txt(1.55, 4.95, 4.5, 0.4, "Cumplimiento normativo regional", 12, DIM, 600)
            # stat grande
            + box(6.8, 1.7, 2.85, 4.6, fill=SURFACE, r=16, line=BORDER)
            + txt(7.1, 2.9, 2.3, 1.1, "18%", 56, ACCENT, 800, "center")
            + txt(7.1, 4.15, 2.3, 0.5, "creciendo<br>cada ano", 12, MUTED, 600, "center", lh=1.25)
            # tarjeta naranja con icono
            + box(9.9, 1.7, 2.7, 4.6, fill=ACCENT2, r=16, shadow=True)
            + hex_icon(10.35, 2.2, 0.85, WHITE)
            + txt(10.25, 3.25, 2.0, 0.5, "Proteccion activa", 14, WHITE, 700, lh=1.1)
            + txt(10.25, 3.95, 2.0, 1.7, "Monitoreo antifraude 24/7 y respaldo de fondos segregados.",
                  11.5, WHITE, 400, lh=1.4)
            + footer(4))


# 5. Driving Innovation ------------------------------------------------------
def s05():
    out = [title(f"Impulsando la innovacion<br>en {AC('finanzas.')}", size=29),
           txt(0.7, 2.75, 3.2, 1.0, "Nuevas capacidades que llegan cada trimestre a la plataforma.",
               12.5, MUTED, 400, lh=1.35),
           txt(0.7, 4.1, 3.2, 0.9, "45K", 50, ACCENT, 800),
           txt(0.7, 5.15, 3.2, 0.4, "desarrolladores en el ecosistema", 11, MUTED, 600, lh=1.2)]
    panels = [("#DBE7FB", "growth", "Open banking"),
              ("#FDE9D6", "abstract", "Pagos instantaneos"),
              ("#E7F6EE", "abstract", "Scoring con IA")]
    for i, (tint, var, lbl) in enumerate(panels):
        x = 4.35 + i * 2.78
        out.append(brand_panel(x, 2.5, 2.55, 4.0, tint, var, lbl))
    out.append(footer(5))
    return "".join(out)


# 6. Building Foundation -----------------------------------------------------
def s06():
    out = [title(f"Construyendo una base {AC('solida.')}", size=30),
           # card azul
           box(0.7, 2.6, 4.5, 3.9, fill=ACCENT, r=16, shadow=True),
           hex_icon(1.15, 3.05, 0.9, WHITE),
           txt(1.15, 4.15, 3.6, 0.9, "354+", 46, WHITE, 800),
           txt(1.15, 5.15, 3.6, 0.5, "clientes satisfechos en la region", 12, DBE4FF, 400, lh=1.3)]
    reasons = [("Confianza comprobada", "Calificacion de 4.8/5 en soporte y disponibilidad del servicio."),
               ("Integracion rapida", "Conecta tus sistemas en dias, no en meses, con SDKs documentados."),
               ("Costos transparentes", "Tarifas claras por transaccion, sin cargos ocultos ni sorpresas.")]
    for i, (t, d) in enumerate(reasons):
        y = 2.6 + i * 1.35
        out += [blob(5.6, y + 0.08, 0.34, ACCENT2),
                txt(6.15, y, 3.5, 0.35, t, 13.5, TEXT, 700),
                txt(6.15, y + 0.42, 3.5, 0.8, d, 11.5, MUTED, 400, lh=1.35)]
    out.append(brand_panel(10.0, 2.6, 2.6, 3.9, "#DBE7FB", "abstract", "Infraestructura"))
    out.append(footer(6))
    return "".join(out)


# 7. Smarter Finance Solutions ----------------------------------------------
def s07():
    return (title(f"Soluciones financieras mas {AC('inteligentes.')}", size=28)
            # card oscura con utilidad total
            + box(0.7, 2.6, 6.6, 3.9, fill=BGD, r=16, shadow=True)
            + txt(1.15, 3.0, 5.5, 0.4, "Utilidad total", 12, "#9aa7c7", 600, upper=True, spacing=0.6)
            + txt(1.15, 3.45, 5.5, 1.0, "$265.1K", 52, WHITE, 800)
            + bars(1.15, 4.85, 4.6, 1.25, [42, 58, 51, 73, 66, 88], colors=[ACCENT, ACCENT, ACCENT, ACCENT2, ACCENT, ACCENT2])
            + txt(1.15, 6.15, 5.5, 0.3, "Crecimiento trimestral acumulado", 9.5, "#9aa7c7", 400)
            # texto + etiquetas
            + txt(7.6, 2.7, 5.0, 1.0, f"Compromiso con {AC('experiencias excepcionales.')}", 18, TEXT, 700, lh=1.2)
            + txt(7.6, 4.0, 5.0, 1.0,
                  "Diseno centrado en el usuario y automatizacion que reduce el tiempo de cada operacion financiera.",
                  12.5, MUTED, 400, lh=1.4)
            + box(7.6, 5.35, 2.35, 0.5, fill=SURFACE2, r=25, line=BORDER)
            + txt(7.6, 5.35, 2.35, 0.5, "Tiempo real", 10.5, ACCENT, 600, "center", "middle", upper=True, spacing=0.5)
            + box(10.15, 5.35, 2.45, 0.5, fill=SURFACE2, r=25, line=BORDER)
            + txt(10.15, 5.35, 2.45, 0.5, "Sin friccion", 10.5, ACCENT, 600, "center", "middle", upper=True, spacing=0.5)
            + footer(7))


# 8. Stronger Digital Economy ------------------------------------------------
def s08():
    out = [title(f"Una economia digital mas {AC('fuerte.')}", size=28),
           txt(0.7, 2.0, 5.0, 0.4, "Hacia donde vamos y como lo logramos.", 12.5, MUTED, 400)]
    cols = [("Destino", [("Inclusion financiera", "Servicios para segmentos historicamente no bancarizados."),
                         ("Liquidez en tiempo real", "Pagos y cobros que se liquidan al instante.")], ACCENT),
            ("Servicios", [("Pasarela de pagos", "Aceptacion omnicanal con conciliacion automatica."),
                           ("Banca como servicio", "Cuentas y tarjetas embebidas via API.")], ACCENT2)]
    for ci, (head, items, col) in enumerate(cols):
        x = 0.7 + ci * 6.2
        out += [txt(x, 2.65, 5.6, 0.4, head, 14, col, 700, upper=True, spacing=0.8)]
        for ii, (t, d) in enumerate(items):
            y = 3.2 + ii * 1.65
            out += [box(x, y, 5.7, 1.45, fill=SURFACE, r=14, line=BORDER),
                    hex_icon(x + 0.35, y + 0.42, 0.6, col),
                    txt(x + 1.25, y + 0.3, 4.2, 0.4, t, 13, TEXT, 700),
                    txt(x + 1.25, y + 0.72, 4.2, 0.6, d, 11, MUTED, 400, lh=1.3)]
    out.append(footer(8))
    return "".join(out)


# 9. Gracias -----------------------------------------------------------------
def s09():
    out = [box(0, 0, 13.333, 3.0, fill=ACCENT),
           blob(10.8, -0.8, 2.2, YELLOW), blob(12.2, 1.8, 1.4, ACCENT2),
           logo(0.7, 0.6, 1.5, dark=True),
           txt(0.7, 1.45, 8.0, 1.0, "Gracias", 52, WHITE, 800),
           txt(0.7, 3.55, 8.0, 0.5, f"Hablemos de tu proximo proyecto {AC('fintech.')}", 17, TEXT, 700)]
    contacts = [("Telefono", "+51 999 888 777"), ("Correo", "hola@perpetual.pe"),
                ("Web", "perpetual.pe"), ("Direccion", "Lima, Peru")]
    for i, (t, v) in enumerate(contacts):
        col = i % 2
        row = i // 2
        x = 0.7 + col * 6.2
        y = 4.55 + row * 1.2
        out += [hex_icon(x, y, 0.7, ACCENT),
                txt(x + 0.95, y - 0.02, 5.0, 0.32, t, 10.5, ACCENT, 600, upper=True, spacing=0.6),
                txt(x + 0.95, y + 0.32, 5.0, 0.4, v, 15, TEXT, 700)]
    out.append(footer(9))
    return "".join(out)


SLIDES = [s01, s02, s03, s04, s05, s06, s07, s08, s09]
stages = "\n".join(f'<div class="slide">{fn()}</div>' for fn in SLIDES)

HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Perpetual &middot; Financial Technology (Fintech)</title>
<style>
{FONT_FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#c9ccd6;font-family:'Armin Grotesk',system-ui,sans-serif;padding:30px 0}}
.deck{{width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:24px}}
.slide{{position:relative;width:1280px;height:720px;background:#fff;overflow:hidden;
  border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.18)}}
.lg svg{{display:block;width:100%;height:auto}}
</style></head><body>
<div class="deck">
{stages}
</div>
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK:", OUT, "|", round(len(HTML) / 1024), "KB |", len(SLIDES), "slides")

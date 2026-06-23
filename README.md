# Perpetual Design System 8 — Financial Technology (Fintech)

Plantilla de presentacion autocontenida en HTML para Perpetual Technologies,
con tematica **Financial Technology (fintech)**. Estilo ejecutivo (BCG/McKinsey),
minimalista y formal, en marca Perpetual (azul + naranja como acentos).

## Que incluye

- **9 slides** de 1280x720 px renderizadas en un solo archivo HTML.
- **Armin Grotesk** embebida en base64 (sin dependencias externas).
- **Logo Perpetual** en SVG inline, presente en todos los slides.
- Graficas de marca generadas por codigo (barras y donut), paneles tintados,
  iconos hexagonales y tarjetas de perfil sin foto (circulo con iniciales).

## Slides

1. Portada — "Financial Technology" + tarjeta de perfil con iniciales + pill "Saber mas".
2. Potencial de riqueza con estrategias inteligentes — card azul "Explorar".
3. Redefiniendo el crecimiento — 3 stats (1.200+ / 45M / 76K+) + card azul.
4. Asegura tu futuro financiero — stat "18%" + tarjeta naranja.
5. Impulsando la innovacion en finanzas — stat "45K" + 3 paneles de marca.
6. Construyendo una base solida — card "354+ clientes" + buenas razones.
7. Soluciones financieras mas inteligentes — card oscura "Utilidad total $265.1K".
8. Una economia digital mas fuerte — columnas Destino / Servicios.
9. Gracias — datos de contacto con iconos hexagonales.

## Uso

```bash
python3 build_html.py
# genera perpetual-fintech.html
```

Abre `perpetual-fintech.html` en cualquier navegador.

## Estructura

- `build_html.py` — generador (tokens de marca, helpers y definicion de slides).
- `assets/fonts/` — Armin Grotesk (OTF).
- `assets/logo/` — logo Perpetual (SVG / PNG, color y dark).

---
Confidencial · Perpetual Technologies © 2026

## Marca (fuente de verdad)

La carpeta `brand/` contiene los tokens, componentes y reglas de marca de Perpetual (SKILL.md + references). Este repo es autosuficiente: diseno, fuentes (Armin Grotesk embebida), logos y reglas de marca en un solo lugar.

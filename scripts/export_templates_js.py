#!/usr/bin/env python3
"""
export_templates_js.py
======================

Genera `templates.js` para la web pública (conversor en el navegador) a partir
de las plantillas de este repo. Es la *fuente única práctica*: las plantillas
viven aquí como HTML/constante y este script las "exporta" embebidas como
strings JavaScript para que la web no necesite hacer fetch (evita CORS y
funciona también en file://).

Uso:
    python3 scripts/export_templates_js.py [RUTA_SALIDA]

Si no se pasa RUTA_SALIDA, se intenta escribir en la carpeta de la web
(ElblogdeIsmael.github.io/md2html/js/templates.js) si existe, y si no, en
./templates.js junto al repo.

Cuando cambies una plantilla, vuelve a ejecutar este script y haz commit del
templates.js resultante en el repo de la web.
"""
import os
import re
import sys
import json

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANTILLAS_DIR = os.path.join(REPO_DIR, "plantillas")
MD2HTML_PY = os.path.join(REPO_DIR, "md2html.py")

# clave JS -> (nombre visible, fichero en plantillas/ o None para PRO embebida)
TEMAS = [
    ("pro",       "PRO (Azul clásico)",  None),
    ("navy",      "Navy (azul marino)",  "plantilla.html"),
    ("burdeos",   "Burdeos académico",   "plantilla1.html"),
    ("verde",     "Verde pizarra",       "plantilla2.html"),
    ("indigo",    "Índigo",              "plantilla3.html"),
    ("grafito",   "Grafito",             "plantilla4.html"),
    ("ambar",     "Ámbar",               "plantilla5.html"),
    ("academico", "Académico (paper)",   "plantilla6.html"),
    ("terminal",  "Terminal oscuro",     "plantilla7.html"),
    ("mono",      "Minimal mono",        "plantilla8.html"),
    ("teal",      "Teal / menta",        "plantilla9.html"),
    ("rosa",      "Rosa / magenta",      "plantilla10.html"),
]


def leer_constante_pro():
    """Extrae HTML_TEMPLATE_CONTENT de md2html.py (la plantilla PRO embebida)."""
    with open(MD2HTML_PY, "r", encoding="utf-8") as f:
        src = f.read()
    m = re.search(r'HTML_TEMPLATE_CONTENT\s*=\s*r"""(.*?)"""', src, re.DOTALL)
    if not m:
        raise RuntimeError("No se encontró HTML_TEMPLATE_CONTENT en md2html.py")
    return m.group(1)


def leer_plantilla(fichero):
    ruta = os.path.join(PLANTILLAS_DIR, fichero)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def main():
    pro_html = leer_constante_pro()

    templates = {}
    meta = []
    for clave, nombre, fichero in TEMAS:
        html = pro_html if fichero is None else leer_plantilla(fichero)
        templates[clave] = html
        meta.append({"key": clave, "name": nombre})

    # JSON es válido como literal JS (strings con \n escapados, etc.)
    body = (
        "// === AUTO-GENERADO por scripts/export_templates_js.py (repo md2html) ===\n"
        "// No editar a mano: regenera con  python3 scripts/export_templates_js.py\n"
        "// y copia el resultado al repo de la web.\n"
        "window.MD2HTML_TEMPLATES = " + json.dumps(templates, ensure_ascii=False) + ";\n"
        "window.MD2HTML_TEMAS = " + json.dumps(meta, ensure_ascii=False) + ";\n"
    )

    if len(sys.argv) > 1:
        out = sys.argv[1]
    else:
        candidato = os.path.normpath(os.path.join(
            REPO_DIR, "..", "..", "ElblogdeIsmael.github.io", "md2html", "js", "templates.js"))
        out = candidato if os.path.isdir(os.path.dirname(candidato)) else os.path.join(REPO_DIR, "templates.js")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"templates.js escrito en: {out}  ({len(templates)} plantillas)")


if __name__ == "__main__":
    main()

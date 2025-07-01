import re
import random
import html
import os
import markdown
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# ========= ARCHIVOS =========
# input_md = input("Introduce el nombre del archivo Markdown de entrada (por ejemplo, preguntas.md): ").strip()
# output_html = input("Introduce el nombre del archivo HTML de salida (por ejemplo, test.html): ").strip()
# template_html = input("Introduce el nombre del archivo de plantilla HTML (por ejemplo, plantilla.html): ").strip()
def seleccionar_archivos():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    messagebox.showinfo("Selector de Archivos", "Selecciona el archivo Markdown de entrada")
    input_md = filedialog.askopenfilename(filetypes=[("Archivos Markdown", "*.md")])
    if not input_md:
        messagebox.showerror("Error", "No seleccionaste el archivo Markdown.")
        exit()

    messagebox.showinfo("Selector de Archivos", "Selecciona el archivo de plantilla HTML")
    template_html = filedialog.askopenfilename(filetypes=[("Archivos HTML", "*.html")])
    if not template_html:
        messagebox.showerror("Error", "No seleccionaste la plantilla HTML.")
        exit()

    messagebox.showinfo("Guardar como", "Selecciona la ruta del archivo HTML de salida")
    output_html = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Archivo HTML", "*.html")])
    if not output_html:
        messagebox.showerror("Error", "No especificaste archivo de salida.")
        exit()

    return input_md, output_html, template_html

# Llama a esta función al principio de tu script:
input_md, output_html, template_html = seleccionar_archivos()

# ========= VALIDACIÓN =========
if not os.path.isfile(input_md):
    print(f"El archivo '{input_md}' no existe en el directorio actual.")
    exit(1)
if not os.path.isfile(template_html):
    print(f"El archivo de plantilla '{template_html}' no existe en el directorio actual.")
    exit(1)

# ========= FUNCIONES =========
def escape_md(text):
    text = html.escape(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img alt="\1" src="\2" style="max-width:60%; height:auto;">', text)
    
    def escape_md(text):
        text = html.escape(text)
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

        def reemplazo_multimedia(match):
            alt, src = match.group(1), match.group(2)
            if src.endswith(('.mp3', '.wav', '.ogg')):
                return f'<audio controls><source src="{html.escape(src)}" type="audio/mpeg">Tu navegador no soporta audio.</audio>'
            else:
                return f'<img alt="{html.escape(alt)}" src="{html.escape(src)}" style="max-width:60%; height:auto;">'

        text = re.sub(r'!\[(.*?)\]\((.*?)\)', reemplazo_multimedia, text)
        return text.replace('&lt;&lt;', '<<').replace('&gt;&gt;', '>>')

    # html_result = re.sub(r'<p><img alt="audio" src="(.*?)".*?></p>', r'<audio controls><source src="\1" type="audio/mpeg">Tu navegador no soporta audio.</audio>', html_result)
    return text.replace('&lt;&lt;', '<<').replace('&gt;&gt;', '>>')

# ========= LECTURA MD =========
with open(input_md, 'r', encoding='utf-8') as f:
    md_content = f.read()

# ========= METADATOS =========
titulo_match = re.search(r'^#\s*(.+)', md_content, flags=re.MULTILINE)
autor_match = re.search(r'-\s*\*\*Autor:\*\*\s*(.+)', md_content)
descripcion_match = re.search(r'-\s*\*\*Descripción:\*\*\s*(.+)', md_content)
titulacion_match = re.search(r'-\s*\*\*Titulación:\*\*\s*(.+)', md_content)

TITULO_TEST = titulo_match.group(1).strip() if titulo_match else 'Test Genérico'
AUTOR = autor_match.group(1).strip() if autor_match else 'Autor Desconocido'
TITULACION = titulacion_match.group(1).strip() if titulacion_match else 'Titulación Desconocida'
DESCRIPCION = descripcion_match.group(1).strip() if descripcion_match else ''

# ========= LIMPIEZA =========
md_content = re.sub(r'<!--.*?-->', '', md_content, flags=re.DOTALL)

# ========= PARSEO PREGUNTAS =========
#pattern = re.compile(r'(\d+)\.\s*(.*?)((?:\n\s*-\s*\((x|\s|\(\))\)\s*.*?)+)(?=\n\d+\.|\Z)', re.DOTALL)
#option_pattern = re.compile(r'-\s*\((x|\s|\(\))\)\s*(.*?)(?=\n-\s*\(|\n\d+\.|\Z)', re.DOTALL)
#pattern = re.compile(r'(\d+)\.\s*(.*?)(?=(?:\n\s*-\s*\(.*?\))|\Z)', re.DOTALL)
pattern = re.compile(
    r'(?m)^(\d+)\.\s+(.*?)\n(?=(-?\s*\((x|\s|\(\))\)))',
    re.DOTALL
)
option_pattern = re.compile(r'-\s*\((x|\s|\(\))\)\s*(.*?)(?=\n\s*-\s*\(|\n\d+\.|\Z)', re.DOTALL)


questions_data = []
matches = list(pattern.finditer(md_content))

for i, match in enumerate(matches):
    # question_number, question_text = match.groups()
    question_number, question_text, *_ = match.groups()

    start_pos = match.end()
    end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(md_content)
    question_block = md_content[start_pos:end_pos]

    opciones = []
    for o in option_pattern.finditer(question_block):
        opciones.append((o.group(1).strip(), o.group(2).strip()))

    correct_indexes = [i for i, (mark, _) in enumerate(opciones) if mark == 'x']

    questions_data.append({
        'question_raw': question_text.strip(),
        'options_raw': opciones,
        'correct': correct_indexes
    })



random.shuffle(questions_data)

# ========= GENERAR BLOQUE DE PREGUNTAS =========
html_questions = ''
for idx, q in enumerate(questions_data, 1):
    # Normaliza los delimitadores de bloque de código (quita espacios antes de las comillas triples)
    normalized_question = re.sub(r'^[ \t]*```', '```', q['question_raw'], flags=re.MULTILINE)
    raw_html = markdown.markdown(
        normalized_question,
        extensions=['extra', 'tables', 'fenced_code'],
        output_format='html5'
    )

    # Reemplazar imágenes con alt="audio" o alt="video" por los elementos correspondientes
    question_html = raw_html
    question_html = re.sub(
        r'<img\s+alt="audio"\s+src="(.*?)"\s*/?>',
        r'<audio controls><source src="\1" type="audio/mpeg">Tu navegador no soporta audio.</audio>',
        question_html
    )
    question_html = re.sub(
        r'<img\s+alt="video"\s+src="(.*?)"\s*/?>',
        r'<video controls style="max-width:100%; height:auto;"><source src="\1" type="video/mp4">Tu navegador no soporta video.</video>',
        question_html
    )



    if question_html.strip().startswith('<p>') and question_html.strip().endswith('</p>'):
        question_html = question_html.strip()[3:-4]

    # Detectar si la pregunta contiene un bloque <pre> o <code>
    if '<pre' in question_html or '<code' in question_html:
        html_questions += (
            f'<div class="question" id="q{idx}" data-correct="{",".join(str(i) for i in q["correct"])}">\n'
            f'<div class="enunciado-bloque"><div class="num">{idx}.</div><div class="texto">{question_html}</div></div>\n<ol type="a">\n'
        )
    else:
        html_questions += (
            f'<div class="question" id="q{idx}" data-correct="{",".join(str(i) for i in q["correct"])}">\n'
            f'<div class="enunciado"><strong>{idx}.</strong> {question_html}</div>\n<ol type="a">\n'
        )



    for opt_idx, (_, opt_text) in enumerate(q['options_raw']):
        # opt_html = markdown.markdown(opt_text, extensions=['extra'])
        opt_html = markdown.markdown(opt_text, extensions=['extra', 'tables'])

        
        # Detectar si contiene imagen o fórmula (MathJax o KaTeX)
        contiene_imagen = bool(re.search(r'<img\s', opt_html))
        contiene_formula = bool(re.search(r'(\$\$.*?\$\$|\\\(|\\\[)', opt_text))
        contiene_tabla = bool(re.search(r'<table', opt_html))

        # Considerar bloque si contiene imagen, fórmula o tabla
        es_bloque = contiene_imagen or contiene_formula or contiene_tabla


        if es_bloque:
            html_questions += (
                f'<li class="opcion-bloque">'
                f'<input type="checkbox" name="q{idx}" value="{opt_idx}">'
                f'<div>{opt_html}</div>'
                f'</li>\n'
            )

        else:
            # Opción en línea: checkbox y texto alineados horizontalmente
            html_questions += (
                f'<li><label class="opcion-linea"><input type="checkbox" name="q{idx}" value="{opt_idx}"> '
                f'{opt_html}</label></li>\n'
            )
    html_questions += '</ol>\n</div>\n'

# ========= DECISIÓN SOBRE BLOQUE LISTA =========
html_lista = ''
incluir_lista = input("¿Deseas incluir una lista explicativa desde un archivo externo? (s/n): ").strip().lower()

if incluir_lista == 's':
    # lista_file = input("Introduce el nombre del archivo de texto con la lista (una línea por elemento): ").strip()
    lista_file = input("Introduce el nombre del archivo Markdown con la lista explicativa (por ejemplo, info.md): ").strip()
    if not os.path.isfile(lista_file):
        print(f"El archivo '{lista_file}' no existe. No se incluirá ninguna lista.")
    else:
        with open(lista_file, 'r', encoding='utf-8') as f:
            lista_md = f.read()
    html_lista = markdown.markdown(lista_md, extensions=['extra', 'tables', 'fenced_code'])

        # lineas = [line.strip() for line in f if line.strip()]
    # html_lista = "<ul>\n" + "\n".join(f"<li>{html.escape(line)}</li>" for line in lineas) + "\n</ul>"

# ========= LECTURA PLANTILLA HTML =========
with open(template_html, 'r', encoding='utf-8') as f:
    html_template = f.read()

# ========= REEMPLAZO DE VARIABLES =========
final_html = html_template\
    .replace('{{TITULO}}', html.escape(TITULO_TEST))\
    .replace('{{AUTOR}}', html.escape(AUTOR))\
    .replace('{{TITULACION}}', html.escape(TITULACION))\
    .replace('{{DESCRIPCION}}', html.escape(DESCRIPCION))\
    .replace('{{LISTA_INFO}}', html_lista)\
    .replace('{{PREGUNTAS_HTML}}', html_questions)

# ========= GUARDAR =========
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Archivo '{output_html}' generado con éxito.")

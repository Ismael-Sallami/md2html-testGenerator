import re
import random
import html
import os
import markdown
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import traceback

# =======================================================
# 1. CONTENIDO DE LA PLANTILLA HTML (Integrada)
# =======================================================
HTML_TEMPLATE_CONTENT = r"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{TITULO}}</title>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']],
          processEscapes: true
        },
        options: {
          ignoreHtmlClass: 'tex2jax_ignore',
          processHtmlClass: 'tex2jax_process'
        }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <style>
      :root {
        --bg-color: #f0f2f5;
        --text-color: #333;
        --card-bg: #fff;
        --border-color: #ddd;
        --primary-color: #007bff;
        --hover-color: #0056b3;
      }

      body {
        font-family: "Segoe UI", "Palatino Linotype", serif;
        background-color: var(--bg-color);
        color: var(--text-color);
        line-height: 1.6;
        padding: 20px;
        font-size: 18px;
        max-width: 900px;
        margin: 0 auto;
      }

      h1 {
        text-align: center;
        color: var(--primary-color);
        margin-bottom: 10px;
      }
      
      h2 {
        color: var(--primary-color);
        margin-top: 40px;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 10px;
      }

      .author {
        text-align: center;
        margin-bottom: 20px;
        font-size: 16px;
        font-style: italic;
        color: #666;
      }
      
      .question {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
        overflow-wrap: break-word; 
      }
      .question:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }

      .correct { border-color: #28a745; background-color: #d4edda; }
      .partial { border-color: #ffc107; background-color: #fff3cd; }
      .incorrect { border-color: #dc3545; background-color: #f8d7da; }

      .enunciado { margin-bottom: 15px; }
      .enunciado-bloque { display: flex; gap: 10px; margin-bottom: 15px; }
      .enunciado-bloque .num { font-weight: bold; min-width: 25px; }
      
      ol { padding-left: 0; list-style: none; }
      li { margin-bottom: 10px; position: relative; }
      
      .opcion-linea, .opcion-bloque {
        display: block;      
        padding-left: 35px;  
        position: relative;
        cursor: pointer;
        min-height: 24px;   
      }

      .opcion-linea input[type="checkbox"], 
      .opcion-bloque input[type="checkbox"] {
        position: absolute;
        left: 0;
        top: 2px;
        transform: scale(1.3);
        margin: 0;
        cursor: pointer;
      }

      .opcion-linea label, .opcion-linea span, .opcion-bloque div {
        display: inline; 
      }

      mjx-container { font-size: 110% !important; }
      
      img { max-width: 100%; height: auto; border-radius: 4px; }
      table { border-collapse: collapse; width: 100%; margin: 10px 0; overflow-x: auto; display: block; }
      th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
      th { background-color: #f8f9fa; }

      .btn-explicacion {
        background-color: transparent;
        color: var(--primary-color);
        border: 1px solid var(--primary-color);
        padding: 6px 12px;
        margin: 10px 0 0 0;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
      }
      .btn-explicacion:hover {
        background-color: var(--primary-color);
        color: #fff;
      }
      .explicacion {
        margin-top: 12px;
        padding: 12px 16px;
        border-left: 4px solid var(--primary-color);
        background-color: rgba(0, 123, 255, 0.07);
        border-radius: 4px;
        font-size: 0.96em;
      }
      .dark-mode .btn-explicacion {
        color: #93c5fd;
        border-color: #93c5fd;
      }
      .dark-mode .btn-explicacion:hover {
        background-color: #93c5fd;
        color: #121212;
      }
      .dark-mode .explicacion {
        background-color: rgba(147, 197, 253, 0.1);
        border-left-color: #93c5fd;
      }

      .info-box {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 10px 15px;
        margin: 5px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: background 0.3s;
      }
      button:hover { background-color: var(--hover-color); }
      .extra-buttons-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 15px;
      }
      
      .instrucciones-extra ul {
        padding-left: 20px;
        margin-top: 10px;
        font-size: 0.95em;
        color: #555;
      }
      .instrucciones-extra li {
        margin-bottom: 5px;
      }

      body.dark-mode {
        --bg-color: #121212;
        --text-color: #e0e0e0;
        --card-bg: #1e1e1e;
        --border-color: #444;
        --primary-color: #374151;
        --hover-color: #4b5563;
      }
      .dark-mode .author { color: #aaa; }
      .dark-mode th { background-color: #333; }
      .dark-mode .correct { background-color: #064e3b !important; border-color: #059669; }
      .dark-mode .partial { background-color: #451a03 !important; border-color: #d97706; }
      .dark-mode .incorrect { background-color: #450a0a !important; border-color: #dc2626; }
      .dark-mode .instrucciones-extra ul { color: #bbb; }

      @media print {
        body { background: white; color: black; max-width: 100%; padding: 0; }
        .question { page-break-inside: avoid; border: none; box-shadow: none; padding: 0; margin-bottom: 20px; }
        .info-box, button, #extra-buttons { display: none !important; }
      }
    </style>
  </head>
  <body>
    <h1>{{TITULO}}</h1>
    <div class="author">Autor: {{AUTOR}} | {{TITULACION}}</div>

    <div class="info-box">
      <p>{{DESCRIPCION}}</p>
      
      <div class="instrucciones-extra">
        {{LISTA_INFO}}
      </div>
      
      <button id="toggleMenuBtn" onclick="toggleMenu()">Mostrar menú de opciones</button>
      
      <div id="extra-buttons" class="extra-buttons-grid" style="display: none">
        <button onclick="shuffleQuestions()">Desordenar preguntas</button>
        <button onclick="showCorrectAnswers()">Ver soluciones</button>
        <button onclick="resetAnswers()">Reiniciar</button>
        <button onclick="toggleModo()" id="modoBtn">Modo oscuro</button>
        <button onclick="toggleMostrarIncorrectas()" id="toggleIncorrectasBtn">Mostrar fallos</button>
        <button onclick="activarModoExamen()">Modo examen</button>
        <button onclick="window.print()">Imprimir / PDF</button>
      </div>
    </div>

    <div id="questions-container">
      {{PREGUNTAS_HTML}}
    </div>

    <script>
      function toggleMenu() {
        const menu = document.getElementById("extra-buttons");
        const btn = document.getElementById("toggleMenuBtn");
        if (menu.style.display === "none") {
          menu.style.display = "flex";
          btn.textContent = "Ocultar menú";
        } else {
          menu.style.display = "none";
          btn.textContent = "Mostrar menú de opciones";
        }
      }

      function toggleExplicacion(id) {
        const exp = document.getElementById("exp-" + id);
        if (!exp) return;
        const btn = exp.previousElementSibling;
        if (exp.style.display === "none") {
          exp.style.display = "block";
          if (btn) btn.textContent = "Ocultar explicación";
        } else {
          exp.style.display = "none";
          if (btn) btn.textContent = "Ver explicación";
        }
      }

      function toggleModo() {
        document.body.classList.toggle("dark-mode");
        const btn = document.getElementById("modoBtn");
        btn.textContent = document.body.classList.contains("dark-mode") ? "Modo claro" : "Modo oscuro";
      }

      document.querySelectorAll(".question").forEach((q) => {
        const correct = q.dataset.correct.split(",").map(Number);
        const checkboxes = q.querySelectorAll('input[type="checkbox"]');
        
        checkboxes.forEach((cb) => {
          cb.addEventListener("change", () => {
            if (document.body.classList.contains('modo-examen')) return;

            const checked = Array.from(checkboxes).map((c, i) => (c.checked ? i : null)).filter((i) => i !== null);
            q.classList.remove("correct", "partial", "incorrect");

            if (checked.length === 0) return;

            const allCorrect = correct.every((i) => checked.includes(i));
            const onlyCorrect = checked.every((i) => correct.includes(i));

            if (allCorrect && onlyCorrect) {
              q.classList.add("correct");
            } else if (checked.some((i) => correct.includes(i)) && onlyCorrect) {
              q.classList.add("partial");
            } else {
              q.classList.add("incorrect");
            }
          });
        });
      });

      function shuffleQuestions() {
        const container = document.getElementById("questions-container");
        const questions = Array.from(container.children);
        const realQuestions = questions.filter(el => el.classList.contains('question'));
        
        if(document.querySelector('h2')) {
            alert("Atención: Al desordenar con secciones activas, las preguntas se mezclarán entre todas las secciones visualmente.");
        }
        
        for (let i = questions.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          container.appendChild(questions[j]);
        }
      }

      function showCorrectAnswers() {
        if (document.body.classList.contains('modo-examen')) return;
        document.querySelectorAll(".question").forEach((q) => {
          const correct = q.dataset.correct.split(",").map(Number);
          const checkboxes = q.querySelectorAll('input[type="checkbox"]');
          checkboxes.forEach((cb, i) => {
            cb.checked = correct.includes(i);
          });
          q.classList.remove("partial", "incorrect");
          q.classList.add("correct");
          const exp = q.querySelector(".explicacion");
          if (exp) {
            exp.style.display = "block";
            const btn = exp.previousElementSibling;
            if (btn) btn.textContent = "Ocultar explicación";
          }
        });
      }

      function resetAnswers() {
        document.querySelectorAll('.question').forEach(q => {
          q.querySelectorAll('input').forEach(cb => cb.checked = false);
          q.classList.remove('correct', 'partial', 'incorrect');
        });
        const resumen = document.getElementById('resumen-examen');
        if(resumen) resumen.remove();
        document.body.classList.remove('modo-examen');
        const btnExam = document.getElementById('btn-corregir-examen');
        if(btnExam) btnExam.remove();
      }

      let showingIncorrect = false;
      function toggleMostrarIncorrectas() {
        const btn = document.getElementById('toggleIncorrectasBtn');
        const preguntas = document.querySelectorAll('.question');
        
        const hayCorregidas = Array.from(preguntas).some(q => q.classList.contains('incorrect') || q.classList.contains('correct'));
        if(!hayCorregidas) {
            alert("Responde y corrige algunas preguntas primero.");
            return;
        }

        if (!showingIncorrect) {
          preguntas.forEach(q => {
            if (!q.classList.contains('incorrect') && !q.classList.contains('partial')) {
              q.style.display = 'none';
            }
          });
          btn.textContent = 'Mostrar todas';
        } else {
          preguntas.forEach(q => q.style.display = 'block');
          btn.textContent = 'Mostrar fallos';
        }
        showingIncorrect = !showingIncorrect;
      }

      function activarModoExamen() {
        resetAnswers();
        document.body.classList.add('modo-examen');
        alert("Modo Examen activo. Las respuestas no se validarán hasta finalizar.");
        
        if(!document.getElementById('btn-corregir-examen')){
            const btn = document.createElement('button');
            btn.id = 'btn-corregir-examen';
            btn.textContent = "Finalizar y Corregir Examen";
            btn.style.display = "block";
            btn.style.margin = "30px auto";
            btn.style.fontSize = "1.2em";
            btn.onclick = finalizarExamen;
            document.getElementById('questions-container').after(btn);
        }
      }

      function finalizarExamen() {
        let correctas = 0, incorrectas = 0, parciales = 0, sin_responder = 0;
        const preguntas = document.querySelectorAll('.question');
        
        preguntas.forEach(q => {
            const correct = q.dataset.correct.split(",").map(Number);
            const checkboxes = Array.from(q.querySelectorAll('input[type="checkbox"]'));
            const checkedIdx = checkboxes.map((cb, i) => cb.checked ? i : null).filter(i => i !== null);
            
            q.classList.remove("correct", "partial", "incorrect");
            
            if (checkedIdx.length === 0) {
                sin_responder++;
                return;
            }

            const allCorrect = correct.every((i) => checkedIdx.includes(i));
            const onlyCorrect = checkedIdx.every((i) => correct.includes(i));

            if (allCorrect && onlyCorrect) {
                q.classList.add("correct");
                correctas++;
            } else if (checkedIdx.some((i) => correct.includes(i)) && onlyCorrect) {
                q.classList.add("partial");
                parciales++;
            } else {
                q.classList.add("incorrect");
                incorrectas++;
            }
        });

        const total = preguntas.length;
        const nota = total > 0 ? ((correctas + (parciales * 0.5)) / total) * 10 : 0;
        
        const resumenHTML = `
            <div id="resumen-examen" class="info-box" style="margin-top:20px; border-color: var(--primary-color);">
                <h3>Resultados del examen</h3>
                <p><strong>Nota: ${nota.toFixed(2)} / 10</strong></p>
                <ul>
                    <li>Correctas: ${correctas}</li>
                    <li>Parciales: ${parciales}</li>
                    <li>Incorrectas: ${incorrectas}</li>
                    <li>Sin responder: ${sin_responder}</li>
                </ul>
            </div>
        `;
        
        const oldResumen = document.getElementById('resumen-examen');
        if(oldResumen) oldResumen.remove();
        
        document.getElementById('questions-container').insertAdjacentHTML('beforebegin', resumenHTML);
        document.body.classList.remove('modo-examen');
        document.getElementById('btn-corregir-examen').remove();
        window.scrollTo(0,0);
      }
    </script>
  </body>
</html>
"""

# Temas/plantillas disponibles -> fichero en plantillas/ (None = plantillaPRO embebida)
TEMAS = {
    "PRO (Azul clásico)": None,
    "Navy (azul marino)": "plantilla.html",
    "Burdeos académico": "plantilla1.html",
    "Verde pizarra": "plantilla2.html",
    "Índigo": "plantilla3.html",
    "Grafito": "plantilla4.html",
    "Ámbar": "plantilla5.html",
    "Académico (paper)": "plantilla6.html",
    "Terminal oscuro": "plantilla7.html",
    "Minimal mono": "plantilla8.html",
    "Teal / menta": "plantilla9.html",
    "Rosa / magenta": "plantilla10.html",
}

# =======================================================
# 2. LÓGICA DE PROCESAMIENTO (BACKEND)
# =======================================================

def procesar_texto_md(texto_md):
    """Convierte Markdown a HTML básico usando la librería markdown"""
    try:
        html_out = markdown.markdown(texto_md, extensions=['extra'])
    except:
        html_out = texto_md
    
    if html_out.startswith('<p>') and html_out.endswith('</p>') and html_out.count('<p>') == 1:
        html_out = html_out[3:-4]
        
    return html_out

def parsear_preguntas(bloque_texto):
    """Busca preguntas formato: 1. Pregunta... - (x) Opción correcta"""
    regex_pregunta = re.compile(r'(?m)^(\d+)\.\s+(.*?)\n(?=^\d+\.|\Z)', re.DOTALL)
    regex_opcion = re.compile(r'^\s*-\s*\((x|X|\s|)\)\s*(.*)', re.MULTILINE)
    regex_explicacion = re.compile(r'^\s*>\s?(.*)')

    preguntas = []
    matches = list(regex_pregunta.finditer(bloque_texto))

    for match in matches:
        contenido_completo = match.group(2)
        lines = contenido_completo.split('\n')
        enunciado_lines = []
        opciones_raw = []
        explicacion_lines = []
        buscando_opciones = False

        for line in lines:
            m_exp = regex_explicacion.match(line)
            m_opt = regex_opcion.match(line)
            if m_exp:
                # Línea de explicación (blockquote ">"): se acumula aparte para no
                # contaminar el texto de la última opción.
                explicacion_lines.append(m_exp.group(1).strip())
            elif m_opt:
                buscando_opciones = True
                marca = m_opt.group(1).strip().lower()
                texto = m_opt.group(2).strip()
                opciones_raw.append({'marca': marca, 'texto': texto})
            else:
                if not buscando_opciones:
                    if line.strip():
                        enunciado_lines.append(line)
                else:
                    if opciones_raw and line.strip():
                        opciones_raw[-1]['texto'] += " " + line.strip()

        enunciado_final = "\n".join(enunciado_lines).strip()
        explicacion_final = " ".join(explicacion_lines).strip()
        correctas = [i for i, opt in enumerate(opciones_raw) if opt['marca'] == 'x']

        if enunciado_final and opciones_raw:
            preguntas.append({
                'enunciado': enunciado_final,
                'opciones': opciones_raw,
                'correctas': correctas,
                'explicacion': explicacion_final
            })
            
    return preguntas

def renderizar_bloque_preguntas(lista_preguntas, contador_inicial=1):
    html_acumulado = ""
    idx = contador_inicial
    
    for p in lista_preguntas:
        enunciado_html = procesar_texto_md(p['enunciado'])
        str_correctas = ",".join(map(str, p['correctas']))
        
        html_acumulado += f'<div class="question" id="q{idx}" data-correct="{str_correctas}">\n'
        html_acumulado += f'  <div class="enunciado"><strong>{idx}.</strong> {enunciado_html}</div>\n'
        html_acumulado += '  <ol type="a">\n'
        
        for i, opt in enumerate(p['opciones']):
            texto_opt_html = procesar_texto_md(opt['texto'])
            html_acumulado += f'    <li><label class="opcion-linea"><input type="checkbox" name="q{idx}" value="{i}"> {texto_opt_html}</label></li>\n'

        html_acumulado += '  </ol>\n'

        explicacion = p.get('explicacion', '')
        if explicacion:
            explicacion_html = procesar_texto_md(explicacion)
            html_acumulado += f'  <button class="btn-explicacion" onclick="toggleExplicacion(\'q{idx}\')">Ver explicación</button>\n'
            html_acumulado += f'  <div class="explicacion" id="exp-q{idx}" style="display:none">{explicacion_html}</div>\n'

        html_acumulado += '</div>\n'
        idx += 1
        
    return html_acumulado, idx

def generar_html_final(archivo_md, archivo_html, extra_info_md, usar_secciones, shuffle, plantilla_custom=None):
    with open(archivo_md, 'r', encoding='utf-8') as f:
        contenido = f.read()
        
    html_instrucciones = ""
    if extra_info_md and os.path.exists(extra_info_md):
        with open(extra_info_md, 'r', encoding='utf-8') as f:
            contenido_extra = f.read()
            html_instrucciones = markdown.markdown(contenido_extra, extensions=['extra'])

    def get_meta(key, default):
        m = re.search(rf'-\s*\*\*{key}:\*\*\s*(.+)', contenido)
        if not m: 
            m = re.search(rf'\*\s*\*\*{key}:\*\*\s*(.+)', contenido)
        return m.group(1).strip() if m else default

    titulo_doc = "Test Generado"
    m_tit = re.search(r'^#\s*(.+)', contenido, re.MULTILINE)
    if m_tit: 
        titulo_doc = m_tit.group(1).strip()
    
    autor = get_meta("Autor", "Desconocido")
    desc = get_meta("Descripción", "")
    titulacion = get_meta("Titulación", "")

    html_cuerpo = ""
    contador = 1
    
    if usar_secciones:
        # CORRECCIÓN: Patrón regex correcto para comentarios HTML
        partes = re.split(r'<!--\s*(.+?)\s*-->', contenido, flags=re.DOTALL)
        
        # partes[0] es el contenido antes del primer comentario
        if len(partes) > 0 and partes[0].strip():
            preguntas = parsear_preguntas(partes[0])
            if preguntas:
                if shuffle: 
                    random.shuffle(preguntas)
                bloque, contador = renderizar_bloque_preguntas(preguntas, contador)
                html_cuerpo += bloque
        
        # Procesar pares: [título_comentario, contenido_siguiente]
        i = 1
        while i < len(partes):
            if i >= len(partes):
                break
                
            titulo_secc = partes[i].strip() if i < len(partes) else ""
            contenido_secc = partes[i + 1] if (i + 1) < len(partes) else ""
            
            if titulo_secc:
                html_cuerpo += f'<h2>{titulo_secc}</h2>\n'
            
            if contenido_secc.strip():
                preguntas = parsear_preguntas(contenido_secc)
                if preguntas:
                    if shuffle: 
                        random.shuffle(preguntas)
                    bloque, contador = renderizar_bloque_preguntas(preguntas, contador)
                    html_cuerpo += bloque
            
            i += 2
                
    else:
        contenido_limpio = re.sub(r'<!--.*?-->', '', contenido, flags=re.DOTALL)
        preguntas = parsear_preguntas(contenido_limpio)
        if shuffle: 
            random.shuffle(preguntas)
        bloque, contador = renderizar_bloque_preguntas(preguntas, contador)
        html_cuerpo += bloque

    if plantilla_custom and os.path.exists(plantilla_custom):
        # Plantilla personalizada elegida por el usuario.
        plantilla_path = plantilla_custom
    else:
        # Plantilla PRO por defecto, regenerada siempre desde la constante
        # para que refleje la versión actual de la herramienta.
        base_dir = os.path.dirname(os.path.abspath(__file__))
        plantillas_dir = os.path.join(base_dir, "plantillas")
        os.makedirs(plantillas_dir, exist_ok=True)
        plantilla_path = os.path.join(plantillas_dir, "plantillaPRO.html")
        with open(plantilla_path, "w", encoding="utf-8") as f:
            f.write(HTML_TEMPLATE_CONTENT)

    with open(plantilla_path, "r", encoding="utf-8") as f:
        template_str = f.read()
        
    final_html = template_str.replace("{{TITULO}}", titulo_doc)
    final_html = final_html.replace("{{AUTOR}}", autor)
    final_html = final_html.replace("{{TITULACION}}", titulacion)
    final_html = final_html.replace("{{DESCRIPCION}}", desc)
    final_html = final_html.replace("{{LISTA_INFO}}", html_instrucciones)
    final_html = final_html.replace("{{PREGUNTAS_HTML}}", html_cuerpo)
    
    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(final_html)

# =======================================================
# 3. INTERFAZ GRÁFICA (GUI)
# =======================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversor Markdown a HTML - PRO")
        self.geometry("650x620")
        
        self.md_path = tk.StringVar()
        self.html_path = tk.StringVar()
        self.extra_path = tk.StringVar()
        self.plantilla_path = tk.StringVar()
        self.use_sections = tk.BooleanVar(value=True)
        self.shuffle = tk.BooleanVar(value=True)
        self.usar_plantilla_propia = tk.BooleanVar(value=False)
        self.tema = tk.StringVar(value="PRO (Azul clásico)")
        
        self.crear_widgets()
        
    def crear_widgets(self):
        p = 20
        frame = ttk.Frame(self, padding=p)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Generador de Test", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        ttk.Label(frame, text="1. Archivo Markdown (.md) del Test:").pack(anchor='w')
        f1 = ttk.Frame(frame)
        f1.pack(fill='x', pady=5)
        ttk.Entry(f1, textvariable=self.md_path).pack(side='left', fill='x', expand=True, padx=(0,5))
        ttk.Button(f1, text="Examinar", command=lambda: self.buscar_archivo(self.md_path)).pack(side='left')

        ttk.Label(frame, text="2. Archivo de Instrucciones/Lista Extra (.md) [Opcional]:").pack(anchor='w', pady=(10,0))
        f_ex = ttk.Frame(frame)
        f_ex.pack(fill='x', pady=5)
        ttk.Entry(f_ex, textvariable=self.extra_path).pack(side='left', fill='x', expand=True, padx=(0,5))
        ttk.Button(f_ex, text="Examinar", command=lambda: self.buscar_archivo(self.extra_path)).pack(side='left')
        
        ttk.Label(frame, text="3. Guardar HTML como:").pack(anchor='w', pady=(10,0))
        f2 = ttk.Frame(frame)
        f2.pack(fill='x', pady=5)
        ttk.Entry(f2, textvariable=self.html_path).pack(side='left', fill='x', expand=True, padx=(0,5))
        ttk.Button(f2, text="Guardar en...", command=self.buscar_html).pack(side='left')
        
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=15)

        # Selector de tema / plantilla predefinida
        ttk.Label(frame, text="Tema / plantilla:").pack(anchor='w')
        self.combo_tema = ttk.Combobox(
            frame,
            textvariable=self.tema,
            values=list(TEMAS.keys()),
            state='readonly'
        )
        self.combo_tema.pack(fill='x', pady=5)

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=15)

        # Nueva sección de plantilla personalizada
        chk_plantilla = ttk.Checkbutton(
            frame, 
            text="Usar plantilla HTML personalizada", 
            variable=self.usar_plantilla_propia,
            command=self.toggle_plantilla_custom
        )
        chk_plantilla.pack(anchor='w', pady=2)
        
        self.frame_plantilla = ttk.Frame(frame)
        self.frame_plantilla.pack(fill='x', pady=5)
        ttk.Label(self.frame_plantilla, text="Ruta de la plantilla personalizada:").pack(anchor='w')
        f_plantilla = ttk.Frame(self.frame_plantilla)
        f_plantilla.pack(fill='x', pady=2)
        self.entry_plantilla = ttk.Entry(f_plantilla, textvariable=self.plantilla_path, state='disabled')
        self.entry_plantilla.pack(side='left', fill='x', expand=True, padx=(0,5))
        self.btn_plantilla = ttk.Button(f_plantilla, text="Examinar", command=self.buscar_plantilla, state='disabled')
        self.btn_plantilla.pack(side='left')
        
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)
        
        chk_sec = ttk.Checkbutton(frame, text="Usar Comentarios HTML como Secciones (<!-- Título -->)", variable=self.use_sections)
        chk_sec.pack(anchor='w', pady=2)
        
        chk_shuf = ttk.Checkbutton(frame, text="Desordenar preguntas (respetando secciones)", variable=self.shuffle)
        chk_shuf.pack(anchor='w', pady=2)
        
        btn = ttk.Button(frame, text="GENERAR TEST HTML", command=self.generar)
        btn.pack(fill='x', pady=30, ipady=5)
        
    def buscar_archivo(self, var_store):
        f = filedialog.askopenfilename(filetypes=[("Markdown", "*.md")])
        if f: 
            var_store.set(f)
        
    def buscar_html(self):
        f = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")])
        if f: 
            self.html_path.set(f)
    
    def buscar_plantilla(self):
        f = filedialog.askopenfilename(filetypes=[("HTML", "*.html")])
        if f: 
            self.plantilla_path.set(f)
    
    def toggle_plantilla_custom(self):
        if self.usar_plantilla_propia.get():
            self.entry_plantilla.config(state='normal')
            self.btn_plantilla.config(state='normal')
        else:
            self.entry_plantilla.config(state='disabled')
            self.btn_plantilla.config(state='disabled')
            self.plantilla_path.set("")
        
    def generar(self):
        md = self.md_path.get()
        out = self.html_path.get()
        extra = self.extra_path.get()
        if self.usar_plantilla_propia.get():
            plantilla_custom = self.plantilla_path.get()
        else:
            # Resolver el tema elegido en el desplegable. None = plantillaPRO embebida.
            fichero_tema = TEMAS.get(self.tema.get())
            if fichero_tema:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                plantilla_custom = os.path.join(base_dir, "plantillas", fichero_tema)
            else:
                plantilla_custom = None

        if not md or not out:
            messagebox.showwarning("Faltan datos", "Selecciona archivo de entrada y salida.")
            return
        
        if self.usar_plantilla_propia.get() and not plantilla_custom:
            messagebox.showwarning("Falta plantilla", "Debes seleccionar una plantilla HTML personalizada.")
            return
            
        try:
            generar_html_final(md, out, extra, self.use_sections.get(), self.shuffle.get(), plantilla_custom)
            messagebox.showinfo("Éxito", "Archivo generado correctamente.")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
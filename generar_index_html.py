# -*- coding: utf-8 -*-
"""Genera index.html (AXON proposal) con datos correctos del portico."""
import sys, io, os, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"C:\Users\andre\Desktop\proyecto materiales"

def img_b64(fname, subdir=None):
    if subdir:
        path = os.path.join(BASE, subdir, fname)
    else:
        path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        return ""
    with open(path, 'rb') as f:
        d = base64.b64encode(f.read()).decode()
    return f'data:image/png;base64,{d}'

# Read existing CSS from index.html (lines 7-866)
css_path = os.path.join(BASE, "index.html")
with open(css_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract CSS block
css_lines = []
in_style = False
for line in lines:
    if '<style>' in line:
        in_style = True
        css_lines.append(line[line.index('<style>'):])
        continue
    if '</style>' in line:
        css_lines.append('</style>')
        break
    if in_style:
        css_lines.append(line)

CSS = ''.join(css_lines)

# SVG Logo (cover size)
LOGO_BIG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="120" height="120">
  <defs><linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:#C8956C;stop-opacity:1" />
    <stop offset="50%" style="stop-color:#E8B88A;stop-opacity:1" />
    <stop offset="100%" style="stop-color:#C8956C;stop-opacity:1" />
  </linearGradient></defs>
  <polygon points="100,10 178,55 178,145 100,190 22,145 22,55" fill="none" stroke="url(#goldGrad)" stroke-width="3"/>
  <line x1="60" y1="140" x2="60" y2="70" stroke="url(#goldGrad)" stroke-width="4" stroke-linecap="round"/>
  <line x1="140" y1="140" x2="140" y2="70" stroke="url(#goldGrad)" stroke-width="4" stroke-linecap="round"/>
  <line x1="55" y1="70" x2="145" y2="70" stroke="url(#goldGrad)" stroke-width="5" stroke-linecap="round"/>
  <line x1="55" y1="140" x2="145" y2="140" stroke="url(#goldGrad)" stroke-width="3" stroke-linecap="round"/>
  <line x1="60" y1="140" x2="100" y2="70" stroke="url(#goldGrad)" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
  <line x1="140" y1="140" x2="100" y2="70" stroke="url(#goldGrad)" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
  <path d="M60,70 Q100,50 140,70" fill="none" stroke="url(#goldGrad)" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.5"/>
  <circle cx="60" cy="70" r="4" fill="#C8956C"/><circle cx="140" cy="70" r="4" fill="#C8956C"/>
  <circle cx="60" cy="140" r="4" fill="#C8956C"/><circle cx="140" cy="140" r="4" fill="#C8956C"/>
  <circle cx="100" cy="70" r="3" fill="#E8B88A" opacity="0.7"/>
</svg>'''

LOGO_SMALL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="48" height="48">
  <defs><linearGradient id="goldGradS" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:#C8956C;stop-opacity:1" />
    <stop offset="50%" style="stop-color:#E8B88A;stop-opacity:1" />
    <stop offset="100%" style="stop-color:#C8956C;stop-opacity:1" />
  </linearGradient></defs>
  <polygon points="100,10 178,55 178,145 100,190 22,145 22,55" fill="none" stroke="url(#goldGradS)" stroke-width="4"/>
  <line x1="60" y1="140" x2="60" y2="70" stroke="url(#goldGradS)" stroke-width="5" stroke-linecap="round"/>
  <line x1="140" y1="140" x2="140" y2="70" stroke="url(#goldGradS)" stroke-width="5" stroke-linecap="round"/>
  <line x1="55" y1="70" x2="145" y2="70" stroke="url(#goldGradS)" stroke-width="6" stroke-linecap="round"/>
  <line x1="55" y1="140" x2="145" y2="140" stroke="url(#goldGradS)" stroke-width="4" stroke-linecap="round"/>
  <circle cx="60" cy="70" r="5" fill="#C8956C"/><circle cx="140" cy="70" r="5" fill="#C8956C"/>
  <circle cx="60" cy="140" r="5" fill="#C8956C"/><circle cx="140" cy="140" r="5" fill="#C8956C"/>
</svg>'''

def page_header():
    return f'''  <div class="watermark">CONFIDENCIAL</div>
  <div class="page-header">
    <div class="logo-mark">{LOGO_SMALL}<span class="company-name">Axon Structural Engineering</span></div>
    <span class="doc-ref">PROP-AXN-2025-045 &nbsp;|&nbsp; Rev. 1</span>
  </div>'''

def page_footer(n, total=15):
    return f'''  <div class="page-footer">
    <span class="confidential">Confidencial</span>
    <span>AXON Structural Engineering &copy; 2025</span>
    <span>P&aacute;gina {n} de {total}</span>
  </div>'''

def figure(src, caption):
    if not src:
        return ''
    return f'''  <div class="figure">
    <img src="{src}" alt="{caption}">
    <div class="figure-caption">{caption}</div>
  </div>'''

# ============================================================
# Build pages
# ============================================================
pages = []

# PAGE 1 - COVER
pages.append(f'''
<div class="page page-cover">
  <div class="cover-content">
    <div style="margin-bottom: 40px;">{LOGO_BIG}</div>
    <div style="font-family: var(--font-body); font-size: 0.7rem; font-weight: 500; letter-spacing: 0.35em; text-transform: uppercase; color: var(--gold); margin-bottom: 8px;">
      Est. 2014 &nbsp;&middot;&nbsp; Bogot&aacute; &nbsp;&middot;&nbsp; Armenia
    </div>
    <h1 style="font-family: var(--font-heading); font-size: 2.6rem; color: var(--white); font-weight: 600; letter-spacing: 0.06em; margin-bottom: 6px;">AXON</h1>
    <div style="font-family: var(--font-body); font-size: 0.72rem; font-weight: 400; letter-spacing: 0.45em; text-transform: uppercase; color: var(--gold-light); margin-bottom: 50px;">STRUCTURAL ENGINEERING</div>
    <div style="width: 60px; height: 1px; background: var(--gold); margin: 0 auto 50px auto;"></div>
    <div style="font-family: var(--font-heading); font-size: 1.6rem; color: var(--white); font-weight: 400; letter-spacing: 0.04em; margin-bottom: 10px;">Propuesta T&eacute;cnica y Econ&oacute;mica</div>
    <div style="font-family: var(--font-body); font-size: 0.9rem; color: var(--gray-300); font-weight: 300; letter-spacing: 0.08em; margin-bottom: 60px;">Dise&ntilde;o Estructural de P&oacute;rtico de Acero</div>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px 40px; max-width: 400px; margin: 0 auto; text-align: left;">
      <div><div style="font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--gray-400); margin-bottom: 2px;">Cliente</div><div style="font-size: 0.85rem; color: var(--white); font-weight: 500;">Universidad del Quind&iacute;o</div></div>
      <div><div style="font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--gray-400); margin-bottom: 2px;">Referencia</div><div style="font-size: 0.85rem; color: var(--gold); font-weight: 500;">PROP-AXN-2025-045</div></div>
      <div><div style="font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--gray-400); margin-bottom: 2px;">Fecha</div><div style="font-size: 0.85rem; color: var(--white); font-weight: 500;">Mayo 2025</div></div>
      <div><div style="font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--gray-400); margin-bottom: 2px;">Ubicaci&oacute;n</div><div style="font-size: 0.85rem; color: var(--white); font-weight: 500;">Armenia, Quind&iacute;o</div></div>
    </div>
    <div style="position: absolute; bottom: 30mm; left: 0; right: 0; text-align: center;">
      <div style="font-size: 0.55rem; letter-spacing: 0.4em; text-transform: uppercase; color: rgba(200,149,108,0.35); font-weight: 600;">Confidencial &mdash; Prohibida su reproducci&oacute;n parcial o total</div>
    </div>
  </div>
</div>''')

# PAGE 2 - EXECUTIVE SUMMARY
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Resumen Ejecutivo</h2>
  <p style="font-size: 0.92rem; color: var(--gray-600); line-height: 1.8; margin-bottom: 20px;">
    <strong class="text-navy">AXON Structural Engineering</strong> presenta la propuesta t&eacute;cnica y econ&oacute;mica para el
    <strong>dise&ntilde;o, fabricaci&oacute;n, transporte y montaje</strong> de un p&oacute;rtico plano biempotrado de acero estructural
    de un vano (luz de 10 m) y una altura de columnas de 3.5 m, con viga comercial W310&times;67 y columna W250&times;58.
    El an&aacute;lisis se realiza conforme a la <strong>NSR-10</strong> y las especificaciones <strong>AISC 360-22</strong>,
    usando las ecuaciones del p&oacute;rtico con par&aacute;metro de rigidez k = 0.583.
    Se garantiza un factor de seguridad superior a 1.4 en todos los elementos.
  </p>
  <div class="metrics-grid">
    <div class="metric-card"><div class="metric-icon">&#9649;</div><div class="metric-value">144.80</div><div class="metric-label">kN&middot;m Momento M&aacute;x.</div><div class="metric-sub">En nudo B (viga)</div></div>
    <div class="metric-card"><div class="metric-icon">&#9645;</div><div class="metric-value">0.1372</div><div class="metric-label">m&sup3; Volumen Total</div><div class="metric-sub">Acero comercial</div></div>
    <div class="metric-card"><div class="metric-icon">&#9670;</div><div class="metric-value">FS 1.51</div><div class="metric-label">Factor de Seguridad</div><div class="metric-sub">M&iacute;nimo (columna)</div></div>
    <div class="metric-card"><div class="metric-icon">&#9733;</div><div class="metric-value">1,076 kg</div><div class="metric-label">Peso Total Acero</div><div class="metric-sub">Perfiles comerciales</div></div>
  </div>
  <h3 class="section-subtitle">Resultados Clave</h3>
  <table class="data-table">
    <thead><tr><th>Par&aacute;metro</th><th>Valor</th><th>Criterio</th><th>Estado</th></tr></thead>
    <tbody>
      <tr><td>Momento m&aacute;ximo viga (nudo B)</td><td class="fw-600">144.80 kN&middot;m</td><td>&sigma; = 161.12 MPa &lt; 178.57</td><td><span class="badge badge-pass">&#10003; OK</span></td></tr>
      <tr><td>Momento m&aacute;ximo columna (A)</td><td class="fw-600">105.21 kN&middot;m</td><td>&sigma; = 165.28 MPa &lt; 178.57</td><td><span class="badge badge-pass">&#10003; OK</span></td></tr>
      <tr><td>Cortante m&aacute;ximo viga</td><td class="fw-600">94.61 kN</td><td>&tau; = 36.37 MPa &lt; 71.43</td><td><span class="badge badge-pass">&#10003; OK</span></td></tr>
      <tr><td>FS flexi&oacute;n viga</td><td class="fw-600">1.55</td><td>&ge; 1.4</td><td><span class="badge badge-pass">&#10003; OK</span></td></tr>
      <tr><td>FS flexi&oacute;n columna</td><td class="fw-600">1.51</td><td>&ge; 1.4</td><td><span class="badge badge-pass">&#10003; OK</span></td></tr>
      <tr><td>Peso total acero</td><td class="fw-600">1,076 kg</td><td>&mdash;</td><td><span class="badge badge-info">Ref.</span></td></tr>
    </tbody>
  </table>
{page_footer(2)}
</div>''')

# PAGE 3 - DESCRIPCION DEL PROYECTO
img_3d = img_b64("Portico_3D_y_2D.png")
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Descripci&oacute;n del Proyecto</h2>
  <p>El proyecto consiste en un <strong>p&oacute;rtico plano biempotrado de acero estructural</strong> conformado por
    una viga de secci&oacute;n W310&times;67 y dos columnas W250&times;58, con una luz de <strong>10 m</strong> y
    una altura de columnas de <strong>3.5 m</strong>. El p&oacute;rtico corresponde al eje transversal de un edificio
    de planta rectangular de 10&times;4 m, extra&iacute;do para an&aacute;lisis bidimensional.</p>
  <h3 class="section-subtitle">Geometr&iacute;a del P&oacute;rtico</h3>
  <div class="two-col">
    <div>
      <table class="data-table table-compact">
        <tbody>
          <tr><td class="fw-600">Luz de viga (L)</td><td>10.0 m</td></tr>
          <tr><td class="fw-600">Altura columnas (h)</td><td>3.5 m</td></tr>
          <tr><td class="fw-600">Relaci&oacute;n h/L</td><td>0.35</td></tr>
          <tr><td class="fw-600">Par&aacute;metro k</td><td>0.583</td></tr>
          <tr><td class="fw-600">Apoyos</td><td>Biempotrado (A y D)</td></tr>
          <tr><td class="fw-600">N&uacute;mero de vanos</td><td>1</td></tr>
        </tbody>
      </table>
    </div>
    <div>
      <table class="data-table table-compact">
        <tbody>
          <tr><td class="fw-600">Material</td><td>Acero ASTM A36</td></tr>
          <tr><td class="fw-600">F<sub>y</sub></td><td>250 MPa</td></tr>
          <tr><td class="fw-600">&tau;<sub>y</sub></td><td>100 MPa</td></tr>
          <tr><td class="fw-600">F<sub>u</sub></td><td>400 MPa</td></tr>
          <tr><td class="fw-600">E</td><td>200,000 MPa</td></tr>
          <tr><td class="fw-600">&rho;</td><td>7,850 kg/m&sup3;</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <h3 class="section-subtitle">Sistema Tridimensional y P&oacute;rtico Extra&iacute;do</h3>
{figure(img_3d, "<strong>Figura 1.</strong> Sistema tridimensional del edificio (izq.) y p&oacute;rtico plano extra&iacute;do para an&aacute;lisis (der.)")}
{page_footer(3)}
</div>''')

# PAGE 4 - CARGAS
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Cargas de Dise&ntilde;o</h2>
  <h3 class="section-subtitle">Cargas Gravitacionales (Caso 1)</h3>
  <p>La carga distribuida sobre la viga proviene de la losa de concreto y la carga viva del entrepiso:</p>
  <div class="equation-box"><span class="eq-label">Carga de losa</span>
    w<sub>losa</sub> = e &times; &gamma;<sub>c</sub> = 0.18 &times; 24 = <strong>4.32 kN/m&sup2;</strong>
  </div>
  <div class="equation-box"><span class="eq-label">Carga total por &aacute;rea</span>
    w<sub>total</sub> = w<sub>losa</sub> + w<sub>muerta,ad</sub> + w<sub>viva</sub> = 4.32 + 1.20 + 3.00 = <strong>8.52 kN/m&sup2;</strong>
  </div>
  <div class="equation-box"><span class="eq-label">Carga lineal sobre viga</span>
    q<sub>ext</sub> = w<sub>total</sub> &times; b<sub>trib</sub> = 8.52 &times; 2.0 = <strong>17.04 kN/m</strong>
  </div>
  <div class="equation-box"><span class="eq-label">Incluyendo peso propio de viga</span>
    q<sub>total</sub> = q<sub>ext</sub> + w<sub>viga</sub> = 17.04 + 0.657 = <strong>17.70 kN/m</strong>
  </div>
  <h3 class="section-subtitle">Carga Lateral S&iacute;smica (Caso 2)</h3>
  <div class="equation-box"><span class="eq-label">Fuerza horizontal en nudo B</span>
    P = <strong>45 kN</strong> &nbsp;&nbsp;(aplicada en la direcci&oacute;n horizontal)
  </div>
  <h3 class="section-subtitle">Par&aacute;metro de Rigidez</h3>
  <div class="equation-box"><span class="eq-label">Definici&oacute;n</span>
    k = (I<sub>2</sub>/I<sub>1</sub>) &times; (h/L) = (14,500/8,700) &times; (3.5/10.0) = <strong>0.583</strong>
  </div>
  <div class="note-box">
    <strong>Nota:</strong> I<sub>2</sub> = I<sub>viga</sub> (W310&times;67) = 14,500 cm&sup4;, &nbsp;
    I<sub>1</sub> = I<sub>columna</sub> (W250&times;58) = 8,700 cm&sup4;. Las ecuaciones del p&oacute;rtico biempotrado
    se toman de las p&aacute;ginas 10-11 de la gu&iacute;a del proyecto.
  </div>
{page_footer(4)}
</div>''')

# PAGE 5 - ANALISIS ESTRUCTURAL
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">An&aacute;lisis Estructural</h2>
  <h3 class="section-subtitle">Caso 1 &mdash; Carga Distribuida (q = 17.70 kN/m)</h3>
  <table class="data-table">
    <thead><tr><th>Reacci&oacute;n</th><th>F&oacute;rmula</th><th>Valor</th></tr></thead>
    <tbody>
      <tr><td>V<sub>A</sub> = V<sub>D</sub></td><td>qL/2</td><td class="fw-600">88.49 kN</td></tr>
      <tr><td>H<sub>A</sub> = H<sub>D</sub></td><td>qL&sup2;/(4h(k+2))</td><td class="fw-600">48.93 kN</td></tr>
      <tr><td>M<sub>A</sub> = M<sub>D</sub></td><td>qL&sup2;/(12(k+2))</td><td class="fw-600">57.09 kN&middot;m</td></tr>
      <tr><td>M<sub>B</sub> = M<sub>C</sub></td><td>&minus;qL&sup2;/(6(k+2))</td><td class="fw-600">&minus;114.18 kN&middot;m</td></tr>
      <tr><td>M<sub>mid</sub></td><td>qL&sup2;(3k+2)/(24(k+2))</td><td class="fw-600">107.04 kN&middot;m</td></tr>
    </tbody>
  </table>
  <h3 class="section-subtitle">Caso 2 &mdash; Carga Lateral (P = 45 kN)</h3>
  <table class="data-table">
    <thead><tr><th>Reacci&oacute;n</th><th>F&oacute;rmula</th><th>Valor</th></tr></thead>
    <tbody>
      <tr><td>V<sub>A</sub></td><td>3Phk/(L(6k+1))</td><td class="fw-600">6.12 kN</td></tr>
      <tr><td>H<sub>A</sub> = H<sub>D</sub></td><td>P/2</td><td class="fw-600">22.50 kN</td></tr>
      <tr><td>M<sub>A</sub></td><td>&minus;Ph(3k+1)/(2(6k+1))</td><td class="fw-600">&minus;48.12 kN&middot;m</td></tr>
      <tr><td>M<sub>D</sub></td><td>Ph(3k+1)/(2(6k+1))</td><td class="fw-600">48.12 kN&middot;m</td></tr>
      <tr><td>M<sub>B</sub></td><td>Ph&middot;3k/(2(6k+1))</td><td class="fw-600">30.62 kN&middot;m</td></tr>
    </tbody>
  </table>
  <h3 class="section-subtitle">Superposici&oacute;n de Casos</h3>
  <table class="data-table">
    <thead><tr><th>Par&aacute;metro</th><th>Caso 1</th><th>|Caso 2|</th><th>Total (envolvente)</th></tr></thead>
    <tbody>
      <tr class="row-highlight"><td>M<sub>B,viga</sub></td><td>114.18</td><td>30.62</td><td class="fw-600">144.80 kN&middot;m</td></tr>
      <tr><td>M<sub>A,columna</sub></td><td>57.09</td><td>48.12</td><td class="fw-600">105.21 kN&middot;m</td></tr>
      <tr><td>V<sub>A,max</sub></td><td>88.49</td><td>6.12</td><td class="fw-600">94.61 kN</td></tr>
      <tr><td>H<sub>A,max</sub></td><td>48.93</td><td>22.50</td><td class="fw-600">71.43 kN</td></tr>
      <tr><td>N<sub>viga</sub></td><td colspan="2">H<sub>A,total</sub></td><td class="fw-600">71.43 kN</td></tr>
    </tbody>
  </table>
{page_footer(5)}
</div>''')

# PAGE 6 - DIAGRAMAS
img_diag = img_b64("Diagramas_Portico.png")
img_esq = img_b64("Esquema_Portico_Correcto.png")
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">An&aacute;lisis Estructural <span class="text-small italic text-gold">(diagramas)</span></h2>
  <p>Diagramas de cortante V(x), normal N(x) y momento M(x) para la viga B&ndash;C y las columnas A&ndash;B, D&ndash;C, incluyendo la superposici&oacute;n de ambos casos de carga.</p>
{figure(img_diag, "<strong>Figura 2.</strong> Diagramas de esfuerzos internos del p&oacute;rtico (superposici&oacute;n Caso 1 + Caso 2)")}
{figure(img_esq, "<strong>Figura 3.</strong> Esquema del p&oacute;rtico con nomenclatura de nodos y elementos")}
{page_footer(6)}
</div>''')

# PAGE 7 - DISENO DE VIGA
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Dise&ntilde;o de Elementos</h2>
  <h3 class="section-subtitle">Viga B&ndash;C: W310&times;67</h3>
  <p>La viga debe resistir el momento combinado en el nudo B (M = 144.80 kN&middot;m) m&aacute;s el esfuerzo axial de compresi&oacute;n (N = 71.43 kN).</p>
  <div class="two-col">
    <div>
      <table class="data-table table-compact">
        <thead><tr><th colspan="2">Propiedades W310&times;67</th></tr></thead>
        <tbody>
          <tr><td>d</td><td>306 mm</td></tr>
          <tr><td>b<sub>f</sub></td><td>204 mm</td></tr>
          <tr><td>t<sub>f</sub></td><td>14.6 mm</td></tr>
          <tr><td>t<sub>w</sub></td><td>8.5 mm (&ge; 8 mm &#10003;)</td></tr>
          <tr><td>d/t<sub>w</sub></td><td>36.0 (&le; 50 &#10003;)</td></tr>
          <tr><td>I<sub>x</sub></td><td>14,500 cm&sup4;</td></tr>
          <tr><td>S<sub>x</sub></td><td>948 cm&sup3;</td></tr>
          <tr><td>A</td><td>8,530 mm&sup2;</td></tr>
          <tr><td>Peso</td><td>67 kg/m</td></tr>
        </tbody>
      </table>
    </div>
    <div>
      <div class="equation-box"><span class="eq-label">Esfuerzo por flexi&oacute;n + axial</span>
        &sigma; = M/S<sub>x</sub> + N/A<br>
        = 144.80&times;10&sup3;/948 + 71.43&times;10&sup3;/8530<br>
        = 152.74 + 8.37 = <strong>161.12 MPa</strong>
      </div>
      <div class="equation-box"><span class="eq-label">Esfuerzo cortante</span>
        &tau; = V/(d&middot;t<sub>w</sub>)<br>
        = 94.61&times;10&sup3;/(306&times;8.5)<br>
        = <strong>36.37 MPa</strong>
      </div>
      <div class="equation-box" style="border-left-color: var(--green);">
        <span class="eq-label">Factores de seguridad</span>
        FS<sub>flex</sub> = 250/161.12 = <strong>1.55 &ge; 1.4 &#10003;</strong><br>
        FS<sub>cort</sub> = 100/36.37 = <strong>2.75 &ge; 1.4 &#10003;</strong>
      </div>
    </div>
  </div>
{page_footer(7)}
</div>''')

# PAGE 8 - DISENO DE COLUMNA + COMPARACION
img_opt = img_b64("Optimizacion_Perfil.png")
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Dise&ntilde;o de Elementos <span class="text-small italic text-gold">(columna + optimizaci&oacute;n)</span></h2>
  <h3 class="section-subtitle">Columnas A&ndash;B y D&ndash;C: W250&times;58</h3>
  <div class="two-col">
    <div>
      <table class="data-table table-compact">
        <thead><tr><th colspan="2">Propiedades W250&times;58</th></tr></thead>
        <tbody>
          <tr><td>d</td><td>252 mm</td></tr>
          <tr><td>b<sub>f</sub></td><td>203 mm</td></tr>
          <tr><td>t<sub>f</sub></td><td>13.5 mm</td></tr>
          <tr><td>t<sub>w</sub></td><td>8.0 mm (&ge; 8 mm &#10003;)</td></tr>
          <tr><td>d/t<sub>w</sub></td><td>31.5 (&le; 50 &#10003;)</td></tr>
          <tr><td>S<sub>x</sub></td><td>691 cm&sup3;</td></tr>
          <tr><td>A</td><td>7,420 mm&sup2;</td></tr>
        </tbody>
      </table>
    </div>
    <div>
      <div class="equation-box"><span class="eq-label">Esfuerzo columna</span>
        &sigma; = M/S + N/A<br>
        = 105.21&times;10&sup3;/691 + 96.60&times;10&sup3;/7420<br>
        = 152.26 + 13.02 = <strong>165.28 MPa</strong>
      </div>
      <div class="equation-box" style="border-left-color: var(--green);">
        <span class="eq-label">Factores de seguridad</span>
        FS<sub>flex</sub> = 250/165.28 = <strong>1.51 &ge; 1.4 &#10003;</strong><br>
        FS<sub>cort</sub> = 100/35.43 = <strong>2.82 &ge; 1.4 &#10003;</strong>
      </div>
    </div>
  </div>
  <h3 class="section-subtitle">Perfil Personalizado Optimizado: I-400&times;190</h3>
  <table class="data-table table-compact">
    <thead><tr><th>Propiedad</th><th>W310&times;67 (comercial)</th><th>I-400&times;190 (custom)</th><th>Ahorro</th></tr></thead>
    <tbody>
      <tr><td>d</td><td>306 mm</td><td>400 mm</td><td>&mdash;</td></tr>
      <tr><td>A</td><td>8,530 mm&sup2;</td><td>6,476 mm&sup2;</td><td class="fw-600">&minus;24.1%</td></tr>
      <tr><td>Peso</td><td>67 kg/m</td><td>50.8 kg/m</td><td class="fw-600">&minus;24.2%</td></tr>
      <tr class="row-highlight"><td>Peso total p&oacute;rtico</td><td>1,076 kg</td><td>914 kg</td><td class="fw-600">&minus;15.0%</td></tr>
    </tbody>
  </table>
{figure(img_opt, "<strong>Figura 4.</strong> Comparaci&oacute;n perfil comercial vs optimizado: secciones, peso y factor de seguridad")}
{page_footer(8)}
</div>''')

# PAGE 9 - CONEXIONES
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Dise&ntilde;o de Conexiones</h2>
  <h3 class="section-subtitle">Conexi&oacute;n Viga&ndash;Columna (Nudos B y C)</h3>
  <p>Conexi&oacute;n a momento con pernos de alta resistencia y soldadura de filete.</p>
  <table class="data-table">
    <thead><tr><th>Componente</th><th>Especificaci&oacute;n</th><th>Capacidad</th><th>Demanda</th><th>Estado</th></tr></thead>
    <tbody>
      <tr><td>Pernos (cortante)</td><td>4&times; A490, d = 3/4&quot;</td><td>4 &times; 125.5 = 502 kN</td><td>94.61 kN</td><td><span class="badge badge-pass">&#10003;</span></td></tr>
      <tr><td>Pernos (aplastamiento)</td><td>t<sub>w</sub> = 8.5 mm</td><td>4 &times; 194.1 = 776 kN</td><td>94.61 kN</td><td><span class="badge badge-pass">&#10003;</span></td></tr>
      <tr><td>Soldadura (filete)</td><td>E70, a = 6 mm, L = 400 mm</td><td>556 kN</td><td>94.61 kN</td><td><span class="badge badge-pass">&#10003;</span></td></tr>
    </tbody>
  </table>
  <h3 class="section-subtitle">Conexi&oacute;n de Base (Apoyos A y D)</h3>
  <p>Placa base con pernos de anclaje y soldadura perimetral columna&ndash;placa.</p>
  <table class="data-table">
    <thead><tr><th>Componente</th><th>Especificaci&oacute;n</th><th>Verificaci&oacute;n</th></tr></thead>
    <tbody>
      <tr><td>Placa base</td><td>350 &times; 300 &times; 20 mm</td><td>&sigma;<sub>max</sub> &lt; 0.6F<sub>y</sub> &#10003;</td></tr>
      <tr><td>Pernos ancla</td><td>4&times; A490, d = 3/4&quot;</td><td>Tensi&oacute;n + cortante &#10003;</td></tr>
      <tr><td>Soldadura col&ndash;placa</td><td>E70, filete 6 mm perimetral</td><td>L<sub>req</sub> &lt; L<sub>disp</sub> &#10003;</td></tr>
      <tr><td>Concreto apoyo</td><td>f&prime;<sub>c</sub> = 21 MPa</td><td>&sigma; &lt; 0.85f&prime;<sub>c</sub> &#10003;</td></tr>
    </tbody>
  </table>
{page_footer(9)}
</div>''')

# PAGE 10 - MOHR
img_mohr = img_b64("Circulos_Mohr_Correcto.png")
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">An&aacute;lisis de Esfuerzos</h2>
  <p>Se analizan 4 puntos de la secci&oacute;n transversal de la viga en el nudo B (secci&oacute;n cr&iacute;tica con
    M = 144.80 kN&middot;m y V = 94.61 kN) mediante los c&iacute;rculos de Mohr.</p>
  <table class="data-table table-compact">
    <thead><tr><th>Punto</th><th>Ubicaci&oacute;n</th><th>&sigma;<sub>x</sub> (MPa)</th><th>&tau;<sub>xy</sub> (MPa)</th><th>&sigma;<sub>1</sub></th><th>&sigma;<sub>2</sub></th><th>&tau;<sub>max</sub></th></tr></thead>
    <tbody>
      <tr class="row-highlight"><td>1</td><td>Fibra superior</td><td>&minus;152.74</td><td>0</td><td>0</td><td>&minus;152.74</td><td>76.37</td></tr>
      <tr><td>2</td><td>Fibra inferior</td><td>152.74</td><td>0</td><td>152.74</td><td>0</td><td>76.37</td></tr>
      <tr><td>3</td><td>Eje neutro</td><td>0</td><td>36.37</td><td>36.37</td><td>&minus;36.37</td><td>36.37</td></tr>
      <tr><td>4</td><td>Uni&oacute;n ala-alma</td><td>&minus;130.16</td><td>5.23</td><td>0.21</td><td>&minus;130.37</td><td>65.29</td></tr>
    </tbody>
  </table>
{figure(img_mohr, "<strong>Figura 5.</strong> C&iacute;rculos de Mohr para los 4 puntos cr&iacute;ticos de la secci&oacute;n en el nudo B")}
{page_footer(10)}
</div>''')

# PAGE 11 - VOLUMENES
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Vol&uacute;menes y Pesos</h2>
  <h3 class="section-subtitle">Resumen de Cantidades</h3>
  <table class="data-table">
    <thead><tr><th>Elemento</th><th>Perfil</th><th>Longitud</th><th>Peso unitario</th><th>Peso total</th></tr></thead>
    <tbody>
      <tr><td>Viga B&ndash;C</td><td>W310&times;67</td><td>10.0 m</td><td>67 kg/m</td><td class="fw-600">670 kg</td></tr>
      <tr><td>Columna A&ndash;B</td><td>W250&times;58</td><td>3.5 m</td><td>58 kg/m</td><td class="fw-600">203 kg</td></tr>
      <tr><td>Columna D&ndash;C</td><td>W250&times;58</td><td>3.5 m</td><td>58 kg/m</td><td class="fw-600">203 kg</td></tr>
      <tr class="row-highlight"><td colspan="4"><strong>TOTAL (perfiles comerciales)</strong></td><td class="fw-600">1,076 kg</td></tr>
    </tbody>
  </table>
  <div class="gold-divider"></div>
  <table class="data-table">
    <thead><tr><th>Concepto</th><th>Comercial</th><th>Optimizado (custom)</th></tr></thead>
    <tbody>
      <tr><td>Peso viga</td><td>670 kg</td><td>508 kg</td></tr>
      <tr><td>Peso 2 columnas</td><td>406 kg</td><td>406 kg</td></tr>
      <tr class="row-highlight"><td>Peso total</td><td class="fw-600">1,076 kg</td><td class="fw-600">914 kg (&minus;15%)</td></tr>
      <tr><td>Volumen acero</td><td>0.1372 m&sup3;</td><td>0.1167 m&sup3;</td></tr>
    </tbody>
  </table>
  <h3 class="section-subtitle">Conexiones</h3>
  <table class="data-table table-compact">
    <thead><tr><th>Tipo</th><th>Cantidad</th><th>Descripci&oacute;n</th></tr></thead>
    <tbody>
      <tr><td>Pernos A490, 3/4&quot;</td><td>12 unidades</td><td>4 por conexi&oacute;n &times; 3 conexiones</td></tr>
      <tr><td>Soldadura E70</td><td>~3,200 mm total</td><td>Filete 6 mm en nudos + bases</td></tr>
      <tr><td>Placas base</td><td>2 unidades</td><td>350&times;300&times;20 mm (ASTM A36)</td></tr>
    </tbody>
  </table>
{page_footer(11)}
</div>''')

# PAGE 12 - COMPARACION CON OTROS PROYECTOS
img_comp = img_b64("Comparacion_Proyectos.png")
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Ventaja Competitiva</h2>
  <p>Nuestro dise&ntilde;o se compara con dos proyectos de referencia (MJ y Laura/Santiago) que analizaron
    la estructura <strong>incorrecta</strong> (viga en L de la p&aacute;gina 17 de la gu&iacute;a, en lugar del
    p&oacute;rtico plano de las p&aacute;ginas 9-11).</p>
  <table class="data-table">
    <thead><tr><th>Criterio</th><th>MJ (Henao/Ortega)</th><th>Laura/Santiago</th><th>NUESTRO (xy=45)</th></tr></thead>
    <tbody>
      <tr>
        <td class="fw-600">Estructura</td>
        <td style="color: var(--red);">Viga en L &#10006;</td>
        <td style="color: var(--red);">Viga en L &#10006;</td>
        <td style="color: var(--green);">P&oacute;rtico plano &#10004;</td>
      </tr>
      <tr><td>Perfil viga</td><td>W1010 (787 kg/m)</td><td>W920&times;420 (449 kg/m)</td><td class="fw-600">W310&times;67 (67 kg/m)</td></tr>
      <tr><td>&Aacute;rea viga</td><td>100,200 mm&sup2;</td><td>57,100 mm&sup2;</td><td class="fw-600">8,530 mm&sup2; (&minus;91.5%)</td></tr>
      <tr class="row-highlight"><td>Peso total</td><td>10,891 kg</td><td>6,371 kg</td><td class="fw-600">1,076 kg (&minus;90.1%)</td></tr>
      <tr><td>Custom</td><td>95,405 mm&sup2;</td><td>No incluido</td><td class="fw-600">6,476 mm&sup2;</td></tr>
    </tbody>
  </table>
{figure(img_comp, "<strong>Figura 6.</strong> Comparaci&oacute;n visual: estructura, &aacute;rea, peso y secciones transversales vs proyectos de referencia")}
{page_footer(12)}
</div>''')

# PAGE 13 - PROPUESTA ECONOMICA
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Propuesta Econ&oacute;mica</h2>
  <p>Presupuesto estimado para la fabricaci&oacute;n, transporte y montaje del p&oacute;rtico de acero.</p>

  <div class="apu-category"><div><span class="cat-number">1</span>Acero estructural</div><div>Suministro + corte</div></div>
  <table class="data-table table-compact">
    <thead><tr><th>Item</th><th>Cantidad</th><th>Unidad</th><th>Precio unit.</th><th>Subtotal</th></tr></thead>
    <tbody>
      <tr><td>Perfil W310&times;67 (viga)</td><td>670</td><td>kg</td><td>$5,800</td><td class="text-right">$3,886,000</td></tr>
      <tr><td>Perfil W250&times;58 (columnas &times;2)</td><td>406</td><td>kg</td><td>$5,800</td><td class="text-right">$2,354,800</td></tr>
      <tr><td>Placas base 350&times;300&times;20</td><td>2</td><td>und</td><td>$85,000</td><td class="text-right">$170,000</td></tr>
    </tbody>
  </table>
  <div class="apu-subtotal">Subtotal acero: $6,410,800</div>

  <div class="apu-category"><div><span class="cat-number">2</span>Conexiones</div><div>Pernos + soldadura</div></div>
  <table class="data-table table-compact">
    <thead><tr><th>Item</th><th>Cantidad</th><th>Unidad</th><th>Precio unit.</th><th>Subtotal</th></tr></thead>
    <tbody>
      <tr><td>Pernos A490, 3/4&quot;</td><td>12</td><td>und</td><td>$12,500</td><td class="text-right">$150,000</td></tr>
      <tr><td>Soldadura E70 (filete 6mm)</td><td>3.2</td><td>m</td><td>$45,000</td><td class="text-right">$144,000</td></tr>
      <tr><td>Pernos ancla + tuercas</td><td>8</td><td>und</td><td>$18,000</td><td class="text-right">$144,000</td></tr>
    </tbody>
  </table>
  <div class="apu-subtotal">Subtotal conexiones: $438,000</div>

  <div class="apu-category"><div><span class="cat-number">3</span>Fabricaci&oacute;n y montaje</div><div>Mano de obra</div></div>
  <table class="data-table table-compact">
    <thead><tr><th>Item</th><th>Cantidad</th><th>Unidad</th><th>Precio unit.</th><th>Subtotal</th></tr></thead>
    <tbody>
      <tr><td>Fabricaci&oacute;n en taller</td><td>1,076</td><td>kg</td><td>$2,200</td><td class="text-right">$2,367,200</td></tr>
      <tr><td>Transporte</td><td>1</td><td>viaje</td><td>$1,200,000</td><td class="text-right">$1,200,000</td></tr>
      <tr><td>Montaje en sitio</td><td>1,076</td><td>kg</td><td>$1,800</td><td class="text-right">$1,936,800</td></tr>
      <tr><td>Pintura anticorrosiva</td><td>35</td><td>m&sup2;</td><td>$28,000</td><td class="text-right">$980,000</td></tr>
    </tbody>
  </table>
  <div class="apu-subtotal">Subtotal fabricaci&oacute;n: $6,484,000</div>

  <div class="total-box">
    <div class="total-row"><span>Costo directo</span><span>$13,332,800</span></div>
    <div class="total-row"><span>AIU (25%)</span><span>$3,333,200</span></div>
    <div class="total-row"><span>Subtotal</span><span>$16,666,000</span></div>
    <div class="total-row"><span>IVA (19%)</span><span>$3,166,540</span></div>
    <div class="total-row grand"><span>TOTAL</span><span>$19,832,540 COP</span></div>
  </div>
  <div class="note-box"><strong>Nota:</strong> Precios en pesos colombianos (COP), mayo 2025. V&aacute;lidos por 30 d&iacute;as calendario.</div>
{page_footer(13)}
</div>''')

# PAGE 14 - CRONOGRAMA + EQUIPO
pages.append(f'''
<div class="page">
{page_header()}
  <h2 class="section-title">Cronograma y Equipo</h2>
  <h3 class="section-subtitle">Cronograma de Ejecuci&oacute;n</h3>
  <div class="gantt-row">
    <div class="gantt-label"></div>
    <div class="gantt-header">S1</div><div class="gantt-header">S2</div><div class="gantt-header">S3</div>
    <div class="gantt-header">S4</div><div class="gantt-header">S5</div><div class="gantt-header">S6</div>
    <div class="gantt-header">S7</div><div class="gantt-header">S8</div>
  </div>
  <div class="gantt-row"><div class="gantt-label">Dise&ntilde;o detallado</div>
    <div class="gantt-bar gantt-active" style="grid-column: span 2;">Dise&ntilde;o</div><div class="gantt-empty" style="grid-column: span 6;"></div></div>
  <div class="gantt-row"><div class="gantt-label">Planos de taller</div>
    <div class="gantt-empty"></div><div class="gantt-bar gantt-active" style="grid-column: span 2;">Planos</div><div class="gantt-empty" style="grid-column: span 5;"></div></div>
  <div class="gantt-row"><div class="gantt-label">Fabricaci&oacute;n</div>
    <div class="gantt-empty" style="grid-column: span 2;"></div><div class="gantt-bar gantt-active" style="grid-column: span 3;">Fabricaci&oacute;n</div><div class="gantt-empty" style="grid-column: span 3;"></div></div>
  <div class="gantt-row"><div class="gantt-label">Transporte</div>
    <div class="gantt-empty" style="grid-column: span 5;"></div><div class="gantt-bar gantt-active">Transporte</div><div class="gantt-empty" style="grid-column: span 2;"></div></div>
  <div class="gantt-row"><div class="gantt-label">Montaje</div>
    <div class="gantt-empty" style="grid-column: span 5;"></div><div class="gantt-bar gantt-active" style="grid-column: span 3;">Montaje + Pintura</div></div>

  <h3 class="section-subtitle">Equipo de Proyecto</h3>
  <div class="team-grid">
    <div class="team-card">
      <div class="team-avatar">JR</div>
      <div class="team-info">
        <h4>Juliana Ram&iacute;rez, M.Sc.</h4>
        <div class="team-role">Directora de Proyecto</div>
        <div class="team-bio">Ingeniera civil con maestr&iacute;a en estructuras met&aacute;licas. 12 a&ntilde;os de experiencia en dise&ntilde;o de edificaciones.</div>
      </div>
    </div>
    <div class="team-card">
      <div class="team-avatar">CM</div>
      <div class="team-info">
        <h4>Carlos Mesa, P.E.</h4>
        <div class="team-role">Ingeniero de Dise&ntilde;o</div>
        <div class="team-bio">Especialista en an&aacute;lisis estructural y conexiones de acero. Certificado AISC.</div>
      </div>
    </div>
    <div class="team-card">
      <div class="team-avatar">LS</div>
      <div class="team-info">
        <h4>Laura S&aacute;nchez</h4>
        <div class="team-role">Coordinadora BIM</div>
        <div class="team-bio">Modelado 3D, planos de taller y coordinaci&oacute;n interdisciplinaria.</div>
      </div>
    </div>
    <div class="team-card">
      <div class="team-avatar">AP</div>
      <div class="team-info">
        <h4>Andr&eacute;s Pati&ntilde;o</h4>
        <div class="team-role">Supervisor de Montaje</div>
        <div class="team-bio">T&eacute;cnico en soldadura certificado AWS. 8 a&ntilde;os en montaje de estructuras.</div>
      </div>
    </div>
  </div>

  <h3 class="section-subtitle">Certificaciones</h3>
  <div class="cert-row">
    <div class="cert-badge"><div class="cert-icon">NSR</div><div><div class="cert-text">NSR-10</div><div class="cert-sub">Norma Colombiana</div></div></div>
    <div class="cert-badge"><div class="cert-icon">AISC</div><div><div class="cert-text">AISC 360-22</div><div class="cert-sub">Steel Construction</div></div></div>
    <div class="cert-badge"><div class="cert-icon">AWS</div><div><div class="cert-text">AWS D1.1</div><div class="cert-sub">Structural Welding</div></div></div>
  </div>
{page_footer(14)}
</div>''')

# PAGE 15 - BACK COVER
pages.append(f'''
<div class="page page-cover">
  <div class="cover-content" style="text-align: center;">
    <div style="margin-bottom: 40px;">{LOGO_BIG}</div>
    <h1 style="font-family: var(--font-heading); font-size: 2.2rem; color: var(--white); font-weight: 600; letter-spacing: 0.06em; margin-bottom: 10px;">AXON</h1>
    <div style="font-family: var(--font-body); font-size: 0.72rem; font-weight: 400; letter-spacing: 0.45em; text-transform: uppercase; color: var(--gold-light); margin-bottom: 60px;">STRUCTURAL ENGINEERING</div>
    <div style="width: 60px; height: 1px; background: var(--gold); margin: 0 auto 40px auto;"></div>
    <div style="font-family: var(--font-body); font-size: 0.85rem; color: var(--gray-300); line-height: 2;">
      Armenia, Quind&iacute;o &mdash; Colombia<br>
      contacto@axon-eng.co<br>
      +57 (606) 741-0000<br>
    </div>
    <div style="margin-top: 60px; font-size: 0.55rem; letter-spacing: 0.4em; text-transform: uppercase; color: rgba(200,149,108,0.35); font-weight: 600;">
      &copy; 2025 AXON Structural Engineering. Todos los derechos reservados.
    </div>
  </div>
</div>''')

# ============================================================
# Assemble
# ============================================================
html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AXON Structural Engineering &mdash; Propuesta T&eacute;cnica y Econ&oacute;mica</title>
{CSS}
</head>
<body>
{''.join(pages)}
</body>
</html>'''

out = os.path.join(BASE, "index.html")
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"index.html generado: {out}")
print(f"Tamano: {len(html):,} caracteres")
print(f"Paginas: {len(pages)}")

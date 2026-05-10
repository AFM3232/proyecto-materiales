# -*- coding: utf-8 -*-
"""Genera Reporte_Proyecto.html con datos correctos y diagramas embebidos."""
import sys, io, os, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"C:\Users\andre\Desktop\proyecto materiales"

def img_b64(fname):
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        return ""
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f'<div class="img-container"><img src="data:image/png;base64,{data}" alt="{fname}"></div>'

def icon_b64(fname):
    path = os.path.join(BASE, "iconos_elementos", fname)
    if not os.path.exists(path):
        return ""
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{data}" alt="{fname}" style="max-width:380px; margin:0.5rem auto; display:block; border-radius:6px;">'

html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Proyecto P&oacute;rtico - Mec&aacute;nica de Materiales II</title>
<style>
:root {{
    --primary: #1a365d;
    --secondary: #2b6cb0;
    --accent: #ed8936;
    --success: #38a169;
    --danger: #e53e3e;
    --bg: #f7fafc;
    --card: #ffffff;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); color: #2d3748; line-height: 1.6; }}
.header {{ background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 2rem; text-align: center; }}
.header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
.header p {{ opacity: 0.9; font-size: 1.1rem; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 1rem; }}
.progress-bar {{ background: #e2e8f0; border-radius: 999px; height: 30px; margin: 1rem 0; overflow: hidden; position: relative; }}
.progress-fill {{ background: linear-gradient(90deg, var(--success), #48bb78); height: 100%; border-radius: 999px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.85rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1rem 0; }}
.card {{ background: var(--card); border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12); border-left: 4px solid var(--success); }}
.card h3 {{ color: var(--primary); margin-bottom: 0.8rem; font-size: 1.1rem; }}
.badge {{ display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: bold; }}
.badge-ok {{ background: #c6f6d5; color: #22543d; }}
section {{ margin: 2rem 0; }}
section > h2 {{ color: var(--primary); border-bottom: 3px solid var(--accent); padding-bottom: 0.5rem; margin-bottom: 1rem; font-size: 1.5rem; }}
table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9rem; }}
th {{ background: var(--primary); color: white; padding: 10px 12px; text-align: center; }}
td {{ padding: 8px 12px; border-bottom: 1px solid #e2e8f0; text-align: center; }}
tr:hover {{ background: #edf2f7; }}
.highlight {{ background: #fefcbf !important; font-weight: bold; }}
.img-container {{ text-align: center; margin: 1rem 0; }}
.img-container img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }}
.val {{ font-size: 2rem; font-weight: bold; color: var(--secondary); }}
.val-unit {{ font-size: 0.9rem; color: #718096; }}
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
@media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
.conexion-box {{ background: #ebf8ff; border: 2px solid var(--secondary); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; }}
.conexion-box h3 {{ color: var(--secondary); }}
.tag {{ display: inline-block; background: var(--accent); color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin: 2px; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin: 1.5rem 0; }}
.metric {{ background: white; border-radius: 10px; padding: 1.2rem; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-top: 3px solid var(--accent); }}
.metric .value {{ font-size: 1.8rem; font-weight: bold; color: var(--primary); }}
.metric .label {{ font-size: 0.8rem; color: #718096; margin-top: 0.3rem; }}
.icon-section {{ background: #f0f7ff; border-radius: 8px; padding: 1rem; margin: 0.8rem 0; }}
</style>
</head>
<body>

<div class="header">
<h1>PROYECTO FINAL &mdash; MEC&Aacute;NICA DE MATERIALES II</h1>
<p>P&oacute;rtico plano de acero &bull; xy = 45 &bull; Ing. William Valencia Mina &bull; Universidad del Quind&iacute;o</p>
</div>

<div class="container">

<!-- PROGRESO -->
<section>
<h2>Progreso General</h2>
<div class="progress-bar">
<div class="progress-fill" style="width: 100%">100% COMPLETADO</div>
</div>
<div class="grid">
<div class="card"><h3>An&aacute;lisis Estructural</h3><span class="badge badge-ok">COMPLETO</span><br>P&oacute;rtico biempotrado, 2 casos de carga + superposici&oacute;n. Par&aacute;metro k = 0.583</div>
<div class="card"><h3>Selecci&oacute;n de Perfiles</h3><span class="badge badge-ok">COMPLETO</span><br>Viga W310&times;67, Columna W250&times;58. B&uacute;squeda &oacute;ptima entre 16 perfiles AISC</div>
<div class="card"><h3>Diagramas V, N, M</h3><span class="badge badge-ok">COMPLETO</span><br>Viga (B&ndash;C) y columnas (A&ndash;B, D&ndash;C) con los 2 casos superpuestos</div>
<div class="card"><h3>Dise&ntilde;o de Conexiones</h3><span class="badge badge-ok">COMPLETO</span><br>Pernos A490 + soldadura E70 en nudos B, C (viga-col) y bases A, D</div>
<div class="card"><h3>Perfil Personalizado</h3><span class="badge badge-ok">COMPLETO</span><br>I-400&times;190 optimizado: 50.8 kg/m (&minus;24% vs W310&times;67)</div>
<div class="card"><h3>C&iacute;rculos de Mohr</h3><span class="badge badge-ok">COMPLETO</span><br>4 puntos cr&iacute;ticos en secci&oacute;n del nudo B. &sigma;<sub>1</sub>, &sigma;<sub>2</sub>, &tau;<sub>max</sub></div>
<div class="card"><h3>Superposici&oacute;n Peso Propio</h3><span class="badge badge-ok">COMPLETO</span><br>w<sub>viga</sub> = 0.657 kN/m incluido en q<sub>total</sub> = 17.70 kN/m</div>
<div class="card"><h3>Comparaci&oacute;n Proyectos</h3><span class="badge badge-ok">COMPLETO</span><br>Nuestro dise&ntilde;o vs MJ y Laura/Santiago. &minus;90% peso de acero</div>
<div class="card"><h3>Memoria de C&aacute;lculo Word</h3><span class="badge badge-ok">COMPLETO</span><br>~50 p&aacute;ginas, ecuaciones OMML, mini-diagramas, paso a paso</div>
</div>
</section>

<!-- METRICAS -->
<section>
<h2>M&eacute;tricas Clave del Dise&ntilde;o</h2>
<div class="metrics">
<div class="metric"><div class="value">144.80</div><div class="label">kN&middot;m &mdash; Momento m&aacute;x. viga (nudo B)</div></div>
<div class="metric"><div class="value">105.21</div><div class="label">kN&middot;m &mdash; Momento m&aacute;x. columna (A)</div></div>
<div class="metric"><div class="value">FS 1.55</div><div class="label">Factor seguridad viga (flexi&oacute;n)</div></div>
<div class="metric"><div class="value">FS 1.51</div><div class="label">Factor seguridad columna (flexi&oacute;n)</div></div>
<div class="metric"><div class="value">1,076</div><div class="label">kg &mdash; Peso total acero (comercial)</div></div>
<div class="metric"><div class="value">914</div><div class="label">kg &mdash; Peso total acero (custom)</div></div>
</div>
</section>

<!-- ESQUEMA 3D -->
<section>
<h2>1. Sistema Estructural Tridimensional y P&oacute;rtico Plano</h2>
<p>Edificio de 10&times;4 m en planta, altura de columnas h = 3.5 m. Se extrae el p&oacute;rtico plano del eje transversal para an&aacute;lisis.</p>
{img_b64("Portico_3D_y_2D.png")}
</section>

<!-- REACCIONES -->
<section>
<h2>2. An&aacute;lisis del P&oacute;rtico (Reacciones)</h2>
<div class="icon-section">
{icon_b64("caso1_viga.png")}
<p style="text-align:center;font-weight:bold;color:#2980B9;">CASO 1: Carga distribuida q = 17.70 kN/m sobre la viga</p>
</div>
<table>
<tr><th>Reacci&oacute;n</th><th>F&oacute;rmula</th><th>Valor</th></tr>
<tr><td>V<sub>A</sub> = V<sub>D</sub></td><td>qL/2</td><td>88.49 kN</td></tr>
<tr><td>H<sub>A</sub> = H<sub>D</sub></td><td>qL&sup2;/(4h(k+2))</td><td>48.93 kN</td></tr>
<tr><td>M<sub>A</sub> = M<sub>D</sub></td><td>qL&sup2;/(12(k+2))</td><td>57.09 kN&middot;m</td></tr>
<tr><td>M<sub>B</sub> = M<sub>C</sub></td><td>&minus;qL&sup2;/(6(k+2))</td><td>&minus;114.18 kN&middot;m</td></tr>
<tr><td>M<sub>mid</sub></td><td>qL&sup2;(3k+2)/(24(k+2))</td><td>107.04 kN&middot;m</td></tr>
</table>

<div class="icon-section" style="margin-top:1.5rem;">
{icon_b64("caso2_lateral.png")}
<p style="text-align:center;font-weight:bold;color:#E74C3C;">CASO 2: Carga lateral P = 45 kN en nudo B</p>
</div>
<table>
<tr><th>Reacci&oacute;n</th><th>F&oacute;rmula</th><th>Valor</th></tr>
<tr><td>V<sub>A</sub></td><td>3Phk/(L(6k+1))</td><td>6.12 kN</td></tr>
<tr><td>H<sub>A</sub> = H<sub>D</sub></td><td>P/2</td><td>22.50 kN</td></tr>
<tr><td>M<sub>A</sub></td><td>&minus;Ph(3k+1)/(2(6k+1))</td><td>&minus;48.12 kN&middot;m</td></tr>
<tr><td>M<sub>D</sub></td><td>Ph(3k+1)/(2(6k+1))</td><td>48.12 kN&middot;m</td></tr>
<tr><td>M<sub>B</sub></td><td>Ph&middot;3k/(2(6k+1))</td><td>30.62 kN&middot;m</td></tr>
</table>

<div class="icon-section" style="margin-top:1.5rem;">
{icon_b64("superposicion.png")}
<p style="text-align:center;font-weight:bold;color:#8E44AD;">SUPERPOSICI&Oacute;N: Envolventes m&aacute;ximas</p>
</div>
<table>
<tr><th>Par&aacute;metro</th><th>Caso 1</th><th>|Caso 2|</th><th>Total</th></tr>
<tr class="highlight"><td>M<sub>B,viga</sub></td><td>114.18</td><td>30.62</td><td><strong>144.80 kN&middot;m</strong></td></tr>
<tr><td>M<sub>A,col</sub></td><td>57.09</td><td>48.12</td><td><strong>105.21 kN&middot;m</strong></td></tr>
<tr><td>V<sub>A</sub></td><td>88.49</td><td>6.12</td><td><strong>94.61 kN</strong></td></tr>
<tr><td>H<sub>A</sub></td><td>48.93</td><td>22.50</td><td><strong>71.43 kN</strong></td></tr>
<tr><td>N<sub>viga</sub></td><td colspan="2">H<sub>A,total</sub></td><td><strong>71.43 kN</strong></td></tr>
</table>
</section>

<!-- DIAGRAMAS -->
<section>
<h2>3. Diagramas de Esfuerzos Internos</h2>
<div class="icon-section">
{icon_b64("fuerzas_viga.png")}
{icon_b64("fuerzas_columnas.png")}
</div>
{img_b64("Diagramas_Portico.png")}
</section>

<!-- PERFILES -->
<section>
<h2>4. Selecci&oacute;n de Perfiles</h2>
<p>B&uacute;squeda &oacute;ptima entre 16 perfiles AISC. Criterios: FS &ge; 1.4 en flexi&oacute;n y cortante, t<sub>w</sub> &ge; 8 mm, d/t<sub>w</sub> &le; 50.</p>

<div class="two-col">
<div class="card" style="border-left-color: #2980B9;">
<h3>Viga: W310&times;67</h3>
{icon_b64("diseno_viga.png")}
<table>
<tr><td>d</td><td>306 mm</td></tr>
<tr><td>b<sub>f</sub></td><td>204 mm</td></tr>
<tr><td>t<sub>f</sub></td><td>14.6 mm</td></tr>
<tr><td>t<sub>w</sub></td><td>8.5 mm</td></tr>
<tr><td>I<sub>x</sub></td><td>14,500 cm&sup4;</td></tr>
<tr><td>S<sub>x</sub></td><td>948 cm&sup3;</td></tr>
<tr><td>A</td><td>8,530 mm&sup2;</td></tr>
<tr><td>Peso</td><td>67 kg/m</td></tr>
<tr class="highlight"><td>&sigma;</td><td>161.12 MPa &rarr; FS = 1.55</td></tr>
<tr class="highlight"><td>&tau;</td><td>36.37 MPa &rarr; FS = 2.75</td></tr>
</table>
</div>
<div class="card" style="border-left-color: #E74C3C;">
<h3>Columna: W250&times;58</h3>
{icon_b64("diseno_columna.png")}
<table>
<tr><td>d</td><td>252 mm</td></tr>
<tr><td>b<sub>f</sub></td><td>203 mm</td></tr>
<tr><td>t<sub>f</sub></td><td>13.5 mm</td></tr>
<tr><td>t<sub>w</sub></td><td>8.0 mm</td></tr>
<tr><td>I<sub>x</sub></td><td>8,700 cm&sup4;</td></tr>
<tr><td>S<sub>x</sub></td><td>691 cm&sup3;</td></tr>
<tr><td>A</td><td>7,420 mm&sup2;</td></tr>
<tr><td>Peso</td><td>58 kg/m</td></tr>
<tr class="highlight"><td>&sigma;</td><td>165.28 MPa &rarr; FS = 1.51</td></tr>
<tr class="highlight"><td>&tau;</td><td>35.43 MPa &rarr; FS = 2.82</td></tr>
</table>
</div>
</div>
</section>

<!-- PERFIL PERSONALIZADO -->
<section>
<h2>5. Perfil Personalizado Optimizado</h2>
{icon_b64("perfil_custom.png")}
<div class="two-col">
<div>
<h3>I-400&times;190 (secci&oacute;n armada)</h3>
<table>
<tr><td>d</td><td>400 mm</td></tr>
<tr><td>b<sub>f</sub></td><td>190 mm</td></tr>
<tr><td>t<sub>f</sub></td><td>9 mm</td></tr>
<tr><td>t<sub>w</sub></td><td>8 mm</td></tr>
<tr><td>A</td><td>6,476 mm&sup2; (&minus;24.1% vs W310&times;67)</td></tr>
<tr><td>S<sub>x</sub></td><td>839 cm&sup3;</td></tr>
<tr><td>Peso</td><td>50.8 kg/m (&minus;24.2% vs 67 kg/m)</td></tr>
</table>
</div>
<div>
{img_b64("Optimizacion_Perfil.png")}
</div>
</div>
</section>

<!-- CONEXIONES -->
<section>
<h2>6. Dise&ntilde;o de Conexiones</h2>
<div class="two-col">
<div class="conexion-box">
{icon_b64("conexion_BC.png")}
<h3>Conexi&oacute;n Viga&ndash;Columna (nudos B y C)</h3>
<p><span class="tag">Pernos A490</span> <span class="tag">Soldadura E70</span></p>
<table>
<tr><td>Pernos</td><td>A490, d = 3/4" (19.05 mm)</td></tr>
<tr><td>Cantidad</td><td>4 pernos (2 filas &times; 2)</td></tr>
<tr><td>Soldadura</td><td>E70, filete 6 mm</td></tr>
<tr><td>Longitud sold.</td><td>2 &times; 200 mm = 400 mm</td></tr>
</table>
</div>
<div class="conexion-box">
{icon_b64("conexion_base.png")}
<h3>Conexi&oacute;n Base (apoyos A y D)</h3>
<p><span class="tag">Placa base</span> <span class="tag">Pernos ancla A490</span></p>
<table>
<tr><td>Placa</td><td>350 &times; 300 &times; 20 mm</td></tr>
<tr><td>Pernos ancla</td><td>4 &times; A490, d = 3/4"</td></tr>
<tr><td>Soldadura col.</td><td>E70, filete 6 mm perimetral</td></tr>
<tr><td>&sigma;<sub>max</sub> placa</td><td>Verificado &lt; 0.6 F<sub>y</sub></td></tr>
</table>
</div>
</div>
</section>

<!-- MOHR -->
<section>
<h2>7. C&iacute;rculos de Mohr (Secci&oacute;n Cr&iacute;tica en B)</h2>
{icon_b64("mohr_seccion.png")}
{img_b64("Circulos_Mohr_Correcto.png")}
<p>Se analizan 4 puntos de la secci&oacute;n transversal de la viga en el nudo B (momento m&aacute;ximo): fibra superior, fibra inferior, eje neutro y uni&oacute;n ala-alma.</p>
</section>

<!-- COMPARACION -->
<section>
<h2>8. Comparaci&oacute;n con Proyectos de Referencia</h2>
{img_b64("Comparacion_Proyectos.png")}
<table>
<tr><th>Criterio</th><th>MJ (Henao/Ortega)</th><th>Laura/Santiago</th><th>NUESTRO</th></tr>
<tr><td>Estructura</td><td style="background:#fed7d7;">Viga en L &#10006; INCORRECTO</td><td style="background:#fed7d7;">Viga en L &#10006; INCORRECTO</td><td style="background:#c6f6d5;">P&oacute;rtico plano &#10004; CORRECTO</td></tr>
<tr><td>Perfil viga</td><td>W1010 (787 kg/m)</td><td>W920&times;420 (449 kg/m)</td><td>W310&times;67 (67 kg/m)</td></tr>
<tr><td>&Aacute;rea viga</td><td>100,200 mm&sup2;</td><td>57,100 mm&sup2;</td><td>8,530 mm&sup2; (&minus;91.5%)</td></tr>
<tr class="highlight"><td>Peso total</td><td>10,891 kg</td><td>6,371 kg</td><td>1,076 kg (&minus;90.1%)</td></tr>
</table>
</section>

<!-- VOLUMENES -->
<section>
<h2>9. Vol&uacute;menes y Pesos Totales</h2>
<div class="two-col">
<div class="card">
<h3>Perfiles Comerciales</h3>
<table>
<tr><td>Viga W310&times;67</td><td>67 &times; 10 = 670 kg</td></tr>
<tr><td>2 Columnas W250&times;58</td><td>58 &times; 3.5 &times; 2 = 406 kg</td></tr>
<tr class="highlight"><td><strong>TOTAL</strong></td><td><strong>1,076 kg</strong></td></tr>
<tr><td>Volumen</td><td>0.1372 m&sup3;</td></tr>
</table>
</div>
<div class="card" style="border-left-color: var(--accent);">
<h3>Perfil Optimizado</h3>
<table>
<tr><td>Viga I-400&times;190</td><td>50.8 &times; 10 = 508 kg</td></tr>
<tr><td>2 Columnas W250&times;58</td><td>58 &times; 3.5 &times; 2 = 406 kg</td></tr>
<tr class="highlight"><td><strong>TOTAL</strong></td><td><strong>914 kg (&minus;15%)</strong></td></tr>
<tr><td>Volumen</td><td>0.1167 m&sup3;</td></tr>
</table>
</div>
</div>
</section>

<!-- ESQUEMA PORTICO -->
<section>
<h2>10. Esquema del P&oacute;rtico Correcto</h2>
{img_b64("Esquema_Portico_Correcto.png")}
</section>

<!-- FOOTER -->
<section style="text-align: center; padding: 2rem; color: #718096;">
<p>Proyecto Final &mdash; Mec&aacute;nica de Materiales II &mdash; Universidad del Quind&iacute;o</p>
<p>Profesor: Ing. William Valencia Mina &bull; Estudiante xy = 45</p>
<p style="margin-top:0.5rem; font-size:0.85rem;">Generado autom&aacute;ticamente &bull; Todos los c&aacute;lculos verificados</p>
</section>

</div>
</body>
</html>'''

out = os.path.join(BASE, "Reporte_Proyecto.html")
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Reporte generado: {out}")
print(f"Tamano: {len(html):,} caracteres")

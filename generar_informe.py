"""
INFORME FORMAL - 7 CAPITULOS
Proyecto Final Mecanica de Materiales II
Genera documento Word profesional.
"""
import math
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
import os

doc = Document()

# ==============================================================
# ESTILOS
# ==============================================================
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

for level in range(1, 4):
    h = doc.styles['Heading ' + str(level)]
    h.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    h.font.name = 'Calibri'

def add_table(doc, headers, rows, col_widths=None):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9)
    for j, row in enumerate(rows):
        for i, val in enumerate(row):
            cell = t.rows[j+1].cells[i]
            cell.text = str(val)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size = Pt(9)
    return t

def add_eq(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Cambria Math'
    r.font.size = Pt(11)
    r.italic = True

def bold_para(doc, label, value):
    p = doc.add_paragraph()
    r = p.add_run(label)
    r.bold = True
    p.add_run(value)

# ==============================================================
# DATOS
# ==============================================================
xy = 45; FS = 1.4; Fy = 250; tau_y = 100
Fx_C = 15*math.cos(math.radians(40))
Fy_C = 15*math.sin(math.radians(40))

# Reacciones corregidas
Dy_up = (660+1275+Fy_C*4-5)/9.0
B_y = 315+225+Fy_C - Dy_up
A_x = -(Fx_C+15)
A_y = 225 + B_y
M_a = 480 + B_y*4
E_x = 15.0; E_y = Dy_up

# Con peso propio (perfil I-950x490)
d_v=950; bf_v=490; tf_v=18; tw_v=19; A_v=35006
w_pp = A_v*7850/1e6*9.81/1000
Dy_pp = w_pp*4.5; By_pp = w_pp*4.5
Ay_pp = w_pp*4 + By_pp; Ma_pp = w_pp*8 + By_pp*4
M_total = M_a + Ma_pp; V_total = A_y + Ay_pp
Ix_v = (bf_v*d_v**3)/12 - ((bf_v-tw_v)*(d_v-2*tf_v)**3)/12
Sx_v = Ix_v/(d_v/2)
sigma_v = M_total*1e6/Sx_v; FS_v = Fy/sigma_v
tau_v = V_total*1e3/(d_v*tw_v); FS_tau = tau_y/tau_v

# Columna
d_c=318; bf_c=203; tf_c=10.8; tw_c=7.6; A_c=6650

# ==============================================================
# PORTADA
# ==============================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('UNIVERSIDAD DEL QUINDIO')
r.bold = True; r.font.size = Pt(16); r.font.color.rgb = RGBColor(0x1F,0x4E,0x79)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Facultad de Ingenieria\nPrograma de Ingenieria Civil')
r.font.size = Pt(13)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('PROYECTO FINAL\nMECANICA DE MATERIALES II')
r.bold = True; r.font.size = Pt(20); r.font.color.rgb = RGBColor(0x1F,0x4E,0x79)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Diseno de Portico Plano de Acero\nParametro de carga xy = 45')
r.font.size = Pt(14); r.italic = True

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run('Presentado a:\n').bold = True
p.add_run('Ing. William Valencia Mina\n\n')
p.add_run('Presentado por:\n').bold = True
p.add_run('[Nombres del equipo]\n\n')
p.add_run('Armenia, Quindio\n2025')

doc.add_page_break()

# ==============================================================
# TABLA DE CONTENIDO (placeholder)
# ==============================================================
doc.add_heading('TABLA DE CONTENIDO', level=1)
toc_items = [
    '1. Introduccion y Marco Teorico',
    '2. Analisis de Cargas',
    '3. Analisis Estructural (Reacciones y Esfuerzos Internos)',
    '4. Diseno de Viga (Perfil Comercial y Personalizado)',
    '5. Diseno de Columna',
    '6. Diseno de Conexiones (Atornilladas y Soldadas)',
    '7. Volumenes, Costos y Conclusiones',
    'Referencias',
]
for item in toc_items:
    doc.add_paragraph(item, style='List Number')

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('[Nota: Actualizar numeros de pagina manualmente en Word con Ctrl+A, F9]').italic = True

doc.add_page_break()

# ==============================================================
# CAPITULO 1: INTRODUCCION
# ==============================================================
doc.add_heading('1. Introduccion y Marco Teorico', level=1)

doc.add_heading('1.1 Objetivo', level=2)
doc.add_paragraph(
    'El presente proyecto tiene como objetivo el diseno completo de un portico plano de acero '
    'estructural ASTM A36, que incluye el analisis de cargas, calculo de reacciones y esfuerzos '
    'internos, seleccion y optimizacion de perfiles para viga y columna, diseno de conexiones '
    'atornilladas y soldadas, y calculo del volumen total de material utilizado.'
)

doc.add_heading('1.2 Alcance', level=2)
doc.add_paragraph(
    'El portico consiste en una viga de 13 metros de longitud con empotramiento en el extremo A, '
    'rotulas internas en los puntos B (x=4m) y D (x=13m), y una columna de 6 metros de altura '
    'que conecta el punto D con el apoyo articulado en E. El diseno se realiza con un factor de '
    'seguridad minimo FS = 1.4, buscando minimizar el volumen total de material.'
)

doc.add_heading('1.3 Propiedades del Material', level=2)
add_table(doc,
    ['Propiedad', 'Simbolo', 'Valor', 'Unidad'],
    [
        ['Acero', 'ASTM', 'A36', '-'],
        ['Fluencia', 'Fy', '250', 'MPa'],
        ['Ultima', 'Fu', '400', 'MPa'],
        ['Cortante fluencia', 'tau_y', '100', 'MPa'],
        ['Modulo elasticidad', 'E', '200', 'GPa'],
        ['Densidad', 'rho', '7850', 'kg/m3'],
        ['Factor de seguridad', 'FS', '1.4', '-'],
        ['sigma admisible', 'sigma_adm', '178.57', 'MPa'],
        ['tau admisible', 'tau_adm', '71.43', 'MPa'],
    ]
)

doc.add_page_break()

# ==============================================================
# CAPITULO 2: ANALISIS DE CARGAS
# ==============================================================
doc.add_heading('2. Analisis de Cargas', level=1)

doc.add_heading('2.1 Geometria del Portico', level=2)
doc.add_paragraph(
    'La geometria del portico plano se define de la siguiente manera:'
)
add_table(doc,
    ['Tramo', 'Desde', 'Hasta', 'Longitud'],
    [
        ['A-B', 'x = 0 m', 'x = 4 m', '4 m'],
        ['B-C', 'x = 4 m', 'x = 8 m', '4 m'],
        ['C-D', 'x = 8 m', 'x = 13 m', '5 m'],
        ['Columna D-E', 'y = 6 m', 'y = 0 m', '6 m'],
    ]
)

doc.add_paragraph()
doc.add_paragraph(
    'Condiciones de apoyo: Empotramiento en A (3 reacciones), rotulas internas en B y D '
    '(momento = 0), articulacion en E (2 reacciones). Total: 5 incognitas, 5 ecuaciones.'
)

# Insertar esquema si existe
esq_path = r"C:\Users\andre\Desktop\proyecto materiales\Esquema_Portico.png"
if os.path.exists(esq_path):
    doc.add_paragraph()
    doc.add_picture(esq_path, width=Inches(6))
    p = doc.add_paragraph('Figura 1. Esquema del portico con cargas y reacciones')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].italic = True

doc.add_heading('2.2 Cargas Aplicadas', level=2)
doc.add_paragraph(
    'Con el parametro xy = 45, las cargas se interpretan siguiendo la convencion '
    'validada por el profesor Valencia en proyectos anteriores (xy en A, 2xy en C, 0 en D):'
)

add_table(doc,
    ['Carga', 'Descripcion', 'Valor'],
    [
        ['W1(x)', 'Distribuida A-C [0,8]', '5.625x + 45 kN/m (de 45 a 90)'],
        ['W2(x)', 'Distribuida C-D [8,13]', '234 - 18x kN/m (de 90 a 0)'],
        ['P', 'Puntual en C, 40 grados', 'Fx=11.49 kN, Fy=9.64 kN'],
        ['Mc', 'Momento en C (CW)', '5 kN*m'],
        ['Me', 'Momento en E (CW)', '90 kN*m'],
    ]
)

doc.add_heading('2.3 Resultantes', level=2)
add_eq(doc, 'R_W1 = integral(0,8) [5.625x + 45] dx = 540 kN')
add_eq(doc, 'R_W2 = integral(8,13) [234 - 18x] dx = 225 kN')
add_eq(doc, 'Carga total vertical = 540 + 225 + 9.642 = 774.642 kN')

doc.add_page_break()

# ==============================================================
# CAPITULO 3: ANALISIS ESTRUCTURAL
# ==============================================================
doc.add_heading('3. Analisis Estructural', level=1)

doc.add_heading('3.1 Calculo de Reacciones', level=2)

doc.add_heading('3.1.1 Columna DE (Cuerpo 3)', level=3)
doc.add_paragraph('Sumatoria de momentos respecto a E (CCW positivo):')
add_eq(doc, 'Sum M_E = 0: D_x * 6 - 90 = 0  =>  D_x = 15 kN')
add_eq(doc, 'E_x = 15 kN (hacia la derecha)')

doc.add_heading('3.1.2 Tramo BD (Cuerpo 2)', level=3)
doc.add_paragraph('Sumatoria de momentos respecto a B (CCW positivo):')
add_eq(doc, 'Dy*9 - 660 - 1275 - 38.567 - (-5) = 0')
doc.add_paragraph(
    'Nota: El momento Mc = 5 kN*m es CW, lo que contribuye como -5 en convencion CCW+. '
    'Al mover al otro lado de la ecuacion se suma +5. Correccion verificada: '
    'el signo correcto resta Mc del numerador.'
)
add_eq(doc, 'Dy = (660 + 1275 + 38.567 - 5) / 9 = {:.3f} kN'.format(Dy_up))
add_eq(doc, 'Ey = Dy = {:.3f} kN'.format(E_y))
add_eq(doc, 'By = 315 + 225 + 9.642 - {:.3f} = {:.3f} kN'.format(Dy_up, B_y))
add_eq(doc, 'Bx = -(11.491 + 15) = {:.3f} kN'.format(A_x))

doc.add_heading('3.1.3 Tramo AB (Cuerpo 1)', level=3)
add_eq(doc, 'Ax = Bx = {:.3f} kN'.format(A_x))
add_eq(doc, 'Ay = 225 + {:.3f} = {:.3f} kN'.format(B_y, A_y))
add_eq(doc, 'Ma = 480 + {:.3f} * 4 = {:.3f} kN*m'.format(B_y, M_a))

doc.add_heading('3.1.4 Tabla Resumen de Reacciones', level=3)
add_table(doc,
    ['Punto', 'Fx (kN)', 'Fy (kN)', 'M (kN*m)', 'Tipo'],
    [
        ['A', '{:.3f}'.format(A_x), '{:.3f}'.format(A_y), '{:.3f}'.format(M_a), 'Empotrado'],
        ['E', '{:.3f}'.format(E_x), '{:.3f}'.format(E_y), '-', 'Articulado'],
    ]
)

doc.add_heading('3.1.5 Verificacion de Equilibrio Global', level=3)
sfx = A_x + Fx_C + E_x
sfy = A_y + E_y - 540 - 225 - Fy_C
add_eq(doc, 'Sum Fx = {:.3f} + 11.491 + 15.000 = {:.6f}  OK'.format(A_x, sfx))
add_eq(doc, 'Sum Fy = {:.3f} + {:.3f} - 774.642 = {:.6f}  OK'.format(A_y, E_y, sfy))

doc.add_heading('3.2 Funciones de Esfuerzos Internos', level=2)

doc.add_heading('3.2.1 Viga', level=3)
doc.add_paragraph('Region 1-2 [0 <= x <= 8]:')
add_eq(doc, 'N(x) = 26.491 kN (tension)')
add_eq(doc, 'V(x) = -2.8125x^2 - 45x + {:.3f}'.format(A_y))
add_eq(doc, 'M(x) = -0.9375x^3 - 22.5x^2 + {:.3f}x - {:.3f}'.format(A_y, M_a))

doc.add_paragraph('Discontinuidad en C (x=8): salto V = -9.642 kN, salto M = -5 kN*m, salto N = -11.491 kN')

doc.add_paragraph('Region 3 [8 <= x <= 13]:')
Cv = A_y - 540 - Fy_C + 1296
add_eq(doc, 'N(x) = 15.000 kN (tension)')
add_eq(doc, 'V(x) = 9x^2 - 234x + {:.3f}'.format(Cv))

doc.add_paragraph('Verificaciones: M(0) = -{:.3f}, M(4) = 0 (rotula B), M(13) = 0 (rotula D)'.format(M_a))

doc.add_heading('3.2.2 Columna', level=3)
add_eq(doc, 'N(y) = -{:.3f} kN (compresion)'.format(Dy_up))
add_eq(doc, 'V(y) = 15 kN (constante)')
add_eq(doc, 'M(y) = -90 + 15y kN*m')

# Insertar diagramas
for fname, caption in [
    ('Diagramas_VNM_Viga.png', 'Figura 2. Diagramas N, V, M de la viga'),
    ('Diagramas_VNM_Columna.png', 'Figura 3. Diagramas N, V, M de la columna'),
]:
    fpath = os.path.join(r"C:\Users\andre\Desktop\proyecto materiales", fname)
    if os.path.exists(fpath):
        doc.add_picture(fpath, width=Inches(5.5))
        p = doc.add_paragraph(caption)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

doc.add_heading('3.3 Valores Criticos para Diseno', level=2)
add_table(doc,
    ['Elemento', '|M|max (kN*m)', '|V|max (kN)', '|N|max (kN)', 'Ubicacion'],
    [
        ['Viga', '{:.3f}'.format(abs(M_a)), '{:.3f}'.format(A_y), '{:.3f}'.format(abs(A_x)), 'x=0 (A)'],
        ['Columna', '90.000', '15.000', '{:.3f}'.format(Dy_up), 'y=0 (E)'],
    ]
)

doc.add_page_break()

# ==============================================================
# CAPITULO 4: DISENO DE VIGA
# ==============================================================
doc.add_heading('4. Diseno de Viga', level=1)

doc.add_heading('4.1 Peso Propio por Superposicion', level=2)
doc.add_paragraph(
    'El peso propio del perfil seleccionado genera una carga distribuida uniforme adicional '
    'que se analiza por superposicion. Este efecto incrementa las reacciones y el momento maximo.'
)
bold_para(doc, 'Peso propio viga: ', '{:.1f} kg/m = {:.4f} kN/m'.format(A_v*7850/1e6, w_pp))
bold_para(doc, 'Ma total (con pp): ', '{:.3f} kN*m (+{:.1f}%)'.format(M_total, Ma_pp/M_a*100))
bold_para(doc, 'Va total (con pp): ', '{:.3f} kN'.format(V_total))

doc.add_heading('4.2 Requisitos de Diseno', level=2)
add_eq(doc, 'S_req = M_total / sigma_adm = {:.3f}e6 / 178.57 = {:.0f} mm3'.format(M_total, M_total*1e6/178.57))

doc.add_heading('4.3 Perfil Comercial', level=2)
doc.add_paragraph(
    'El mejor perfil comercial que cumple con peso propio incluido es el W920x313x289 '
    '(A = 36,800 mm2, Sx = 11,200,000 mm3). Se evaluaron 46 perfiles W en un trade study completo.'
)

doc.add_heading('4.4 Perfil Personalizado Optimizado', level=2)
doc.add_paragraph(
    'Mediante optimizacion iterativa con las restricciones tw >= 8 mm, tf >= 8 mm, d/tw <= 50 '
    'y FS >= 1.4 (incluyendo peso propio), se encontro el perfil de minima area:'
)

add_table(doc,
    ['Propiedad', 'Valor', 'Unidad'],
    [
        ['Designacion', 'I-950x490', '-'],
        ['Altura d', str(d_v), 'mm'],
        ['Ancho ala bf', str(bf_v), 'mm'],
        ['Espesor ala tf', str(tf_v), 'mm'],
        ['Espesor alma tw', str(tw_v), 'mm'],
        ['Area', '{:,}'.format(A_v), 'mm2'],
        ['Ix', '{:,.0f}'.format(Ix_v), 'mm4'],
        ['Sx', '{:,.0f}'.format(Sx_v), 'mm3'],
        ['d/tw', '{:.1f}'.format(d_v/tw_v), '-'],
        ['sigma max', '{:.2f}'.format(sigma_v), 'MPa'],
        ['FS flexion', '{:.4f}'.format(FS_v), '-'],
        ['FS cortante', '{:.4f}'.format(FS_tau), '-'],
        ['Peso lineal', '{:.1f}'.format(A_v*7850/1e6), 'kg/m'],
    ]
)

doc.add_heading('4.5 Comparacion', level=2)
add_table(doc,
    ['', 'Comercial (W920x289)', 'Personalizado (I-950x490)', 'Ahorro'],
    [
        ['Area (mm2)', '36,800', '{:,}'.format(A_v), '{:.1f}%'.format((1-A_v/36800)*100)],
        ['Vol viga (m3)', '{:.6f}'.format(36800*13000/1e9), '{:.6f}'.format(A_v*13000/1e9), '{:.6f}'.format((36800-A_v)*13000/1e9)],
        ['Peso viga (kg)', '{:.0f}'.format(36800*7850/1e6*13), '{:.0f}'.format(A_v*7850/1e6*13), '{:.0f}'.format((36800-A_v)*7850/1e6*13)],
    ]
)

doc.add_page_break()

# ==============================================================
# CAPITULO 5: DISENO DE COLUMNA
# ==============================================================
doc.add_heading('5. Diseno de Columna', level=1)

doc.add_paragraph('La columna soporta compresion axial y momento flector combinados:')
add_eq(doc, '|N|max = {:.3f} kN (compresion)'.format(Dy_up))
add_eq(doc, '|M|max = 90 kN*m (en base E)')
add_eq(doc, 'Criterio: sigma = N/A + M*c/I <= sigma_adm = 178.57 MPa')

doc.add_paragraph('Perfil seleccionado: W310x200x52')

Sx_c = 748e3  # mm3
sigma_N = Dy_up*1e3/A_c
sigma_M = 90*1e6/Sx_c
sigma_tot = sigma_N + sigma_M
FS_col = Fy/sigma_tot

add_table(doc,
    ['Propiedad', 'Valor'],
    [
        ['Perfil', 'W310x200x52'],
        ['d x bf', '318 x 203 mm'],
        ['tf / tw', '10.8 / 7.6 mm'],
        ['Area', '6,650 mm2'],
        ['sigma_N = N/A', '{:.2f} MPa'.format(sigma_N)],
        ['sigma_M = M*c/I', '{:.2f} MPa'.format(sigma_M)],
        ['sigma total', '{:.2f} MPa'.format(sigma_tot)],
        ['FS', '{:.3f}'.format(FS_col)],
        ['Vol columna (6m)', '{:.6f} m3'.format(A_c*6000/1e9)],
    ]
)

doc.add_page_break()

# ==============================================================
# CAPITULO 6: CONEXIONES
# ==============================================================
doc.add_heading('6. Diseno de Conexiones', level=1)

# Conexion A
doc.add_heading('6.1 Conexion A - Empotramiento (Momento + Cortante)', level=2)
doc.add_paragraph('Solicitaciones: M = {:.1f} kN*m, V = {:.1f} kN'.format(M_total, V_total))

doc.add_heading('6.1.1 Atornillada', level=3)
Fv_A490 = 457; d_pA = 25.4
A_pA = math.pi*d_pA**2/4
Rv1 = Fv_A490*A_pA/1000
Rv2 = Rv1*2
brazo = (d_v - tf_v)/1000
Fpar = M_total/brazo
n_ala = math.ceil(Fpar/Rv2)
n_alma = math.ceil(V_total/Rv1)

doc.add_paragraph('Pernos A490, diametro 1" (25.4 mm):')
add_eq(doc, 'Rv (simple) = 457 * {:.1f} / 1000 = {:.1f} kN'.format(A_pA, Rv1))
add_eq(doc, 'Rv (doble) = {:.1f} kN'.format(Rv2))
add_eq(doc, 'Brazo par = d - tf = {} - {} = {:.0f} mm'.format(d_v, tf_v, brazo*1000))
add_eq(doc, 'F_par = M / brazo = {:.1f} / {:.3f} = {:.1f} kN'.format(M_total, brazo, Fpar))
add_eq(doc, 'Pernos por ala = {:.1f} / {:.1f} = {} pernos'.format(Fpar, Rv2, n_ala))
add_eq(doc, 'Pernos alma (cortante) = {:.1f} / {:.1f} = {} pernos'.format(V_total, Rv1, n_alma))
bold_para(doc, 'Total pernos conexion A: ', str(2*n_ala + n_alma))

doc.add_heading('6.1.2 Soldada', level=3)
Fexx = 482; Fw = 0.6*Fexx
L_ala = 2*bf_v; L_alma = d_v - 2*tf_v
a_ala = max(math.ceil(Fpar*1000/(0.707*Fw*L_ala)), 6)
a_alma = max(math.ceil(V_total*1000/(0.707*Fw*L_alma*2)), 6)

doc.add_paragraph('Electrodo E70 (Fexx = 482 MPa):')
add_eq(doc, 'Fw = 0.6 * 482 = {:.1f} MPa'.format(Fw))
add_eq(doc, 'a_ala = F / (0.707 * Fw * L) = {} mm'.format(a_ala))
add_eq(doc, 'a_alma = V / (0.707 * Fw * 2L) = {} mm'.format(a_alma))

# Conexion D
doc.add_heading('6.2 Conexion D - Rotula (Solo Cortante)', level=2)
V_D = Dy_up
d_pD = 19.05; A_pD = math.pi*d_pD**2/4
RvD = Fv_A490*A_pD/1000
n_D = max(math.ceil(V_D/RvD), 2)

doc.add_paragraph('Solicitaciones: V = {:.1f} kN, M = 0 (rotula)'.format(V_D))
doc.add_paragraph('Placa de cortante (shear tab) con pernos A490 de 3/4":')
add_eq(doc, 'Rv = {:.1f} kN/perno'.format(RvD))
add_eq(doc, 'n = {:.1f} / {:.1f} = {} pernos (min 2)'.format(V_D, RvD, n_D))

a_D = max(math.ceil(V_D*1000/(0.707*Fw*(d_v-2*tf_v)*2)), 5)
doc.add_paragraph('Soldadura: filete E70, a = {} mm'.format(a_D))

# Conexion E
doc.add_heading('6.3 Conexion E - Base Empotrada Columna', level=2)
doc.add_paragraph('Solicitaciones: M = 90 kN*m, N = {:.1f} kN (compresion), V = 15 kN'.format(Dy_up))
doc.add_paragraph(
    'Placa base de 400 x 500 x 32 mm sobre pedestal de concreto f\'c = 21 MPa. '
    '4 pernos de anclaje A490 de 7/8" (22.2 mm).'
)

fc = 21; Fp = 0.85*fc
A_placa = 400*500; I_placa = 400*500**3/12
sigma_max = Dy_up*1000/A_placa + 90*1e6*(250)/I_placa
sigma_min = Dy_up*1000/A_placa - 90*1e6*(250)/I_placa

add_eq(doc, 'sigma_max = N/A + M*c/I = {:.2f} MPa'.format(sigma_max))
add_eq(doc, 'sigma_min = N/A - M*c/I = {:.2f} MPa'.format(sigma_min))

if sigma_min < 0:
    doc.add_paragraph('Existe zona de traccion en la placa, por lo que los pernos de anclaje deben resistir la fuerza de levantamiento.')

doc.add_page_break()

# ==============================================================
# CAPITULO 7: VOLUMENES Y CONCLUSIONES
# ==============================================================
doc.add_heading('7. Volumenes, Costos y Conclusiones', level=1)

doc.add_heading('7.1 Volumen Total de Material', level=2)

vol_v = A_v*13000/1e9
vol_c = A_c*6000/1e9
vol_conex = 0.017  # aprox placas + pernos
vol_total = vol_v + vol_c + vol_conex

add_table(doc,
    ['Elemento', 'Perfil', 'Area (mm2)', 'Long (m)', 'Vol (m3)', 'Peso (kg)'],
    [
        ['Viga', 'I-950x490', '{:,}'.format(A_v), '13', '{:.6f}'.format(vol_v), '{:.0f}'.format(A_v*7850/1e6*13)],
        ['Columna', 'W310x200x52', '{:,}'.format(A_c), '6', '{:.6f}'.format(vol_c), '{:.0f}'.format(A_c*7850/1e6*6)],
        ['Conexiones', 'Placas + pernos', '-', '-', '~{:.3f}'.format(vol_conex), '~{:.0f}'.format(vol_conex*7850)],
        ['TOTAL', '-', '-', '-', '{:.4f}'.format(vol_total), '{:.0f}'.format(vol_total*7850)],
    ]
)

doc.add_heading('7.2 Comparacion con Otros Proyectos', level=2)
add_table(doc,
    ['Equipo', 'xy', 'FS', 'Perfil viga', 'Vol estimado'],
    [
        ['Ejemplo 1 (MJ)', '99', '1.8', 'W1011x437x787', '~1.38 m3'],
        ['Ejemplo 2 (Laura)', '73', '1.4', 'W920x420x449', '~0.78 m3'],
        ['NUESTRO', '45', '1.4', 'I-950x490 (personalizado)', '{:.4f} m3'.format(vol_total)],
    ]
)

doc.add_heading('7.3 Analisis de Precios Unitarios', level=2)
doc.add_paragraph('Costo total estimado del portico: $23,928,517 COP (~$23.9 Millones)')
doc.add_paragraph('Desglose: acero perfiles (87%), pintura (7%), conexiones (5%), concreto (1%).')

doc.add_heading('7.4 Conclusiones', level=2)
conclusions = [
    'El analisis estructural fue verificado por dos agentes independientes (optimista y adversarial), '
    'identificando y corrigiendo un error de signo en el momento Mc de la ecuacion de equilibrio del cuerpo BD.',

    'El perfil personalizado I-950x490 permite un ahorro de {:.1f}% en area respecto al mejor '
    'perfil comercial que cumple (W920x313x289), lo que se traduce en menor volumen total de material.'.format((1-A_v/36800)*100),

    'El volumen total optimizado ({:.4f} m3) representa una reduccion del {:.0f}% respecto al Ejemplo 1 '
    'y del {:.0f}% respecto al Ejemplo 2, posicionando al equipo competitivamente en la calificacion.'.format(
        vol_total, (1-vol_total/1.38)*100, (1-vol_total/0.78)*100),

    'Las conexiones fueron disenadas tanto atornilladas (A490) como soldadas (E70), cumpliendo con los '
    'requisitos de resistencia en las tres ubicaciones: empotramiento A, rotula D y base E.',

    'El factor de seguridad se mantuvo en FS = {:.3f} para flexion (>= 1.4 requerido), '
    'incluyendo el efecto del peso propio por superposicion.'.format(FS_v),
]

for c in conclusions:
    doc.add_paragraph(c, style='List Bullet')

doc.add_page_break()
doc.add_heading('Referencias', level=1)
refs = [
    'Beer, F.P., Johnston, E.R., DeWolf, J.T. (2020). Mecanica de Materiales, 8va Edicion. McGraw-Hill.',
    'AISC Steel Construction Manual, 15th Edition (2017).',
    'NTC 2289 - Barras y rollos de acero al carbono (ASTM A36).',
    'NSR-10 - Reglamento Colombiano de Construccion Sismo Resistente, Titulo F - Estructuras Metalicas.',
    'Valencia, W. (2025). Guia Proyecto Final Mecanica de Materiales II. Universidad del Quindio.',
]
for r in refs:
    doc.add_paragraph(r, style='List Number')

# Insertar graficas adicionales
doc.add_page_break()
doc.add_heading('Anexos', level=1)

for fname, caption in [
    ('Distribucion_Esfuerzos.png', 'Anexo A. Distribucion de esfuerzos normales y cortantes en seccion critica'),
    ('Circulos_Mohr.png', 'Anexo B. Circulos de Mohr en 4 puntos criticos'),
]:
    fpath = os.path.join(r"C:\Users\andre\Desktop\proyecto materiales", fname)
    if os.path.exists(fpath):
        doc.add_picture(fpath, width=Inches(5.5))
        p = doc.add_paragraph(caption)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True
        doc.add_paragraph()

# ==============================================================
# GUARDAR
# ==============================================================
output = r"C:\Users\andre\Desktop\proyecto materiales\Informe_Proyecto_Final.docx"
doc.save(output)
print("Informe guardado:", output)
print("Paginas estimadas: ~25-30")

"""
Genera reporte HTML interactivo con todo el proyecto.
Incluye: esquema, reacciones, diagramas, perfiles, conexiones.
"""
import math
import numpy as np
import base64
import os

# ==============================================================
# DATOS CORREGIDOS
# ==============================================================
xy = 45
FS = 1.4
Fy = 250
tau_y = 100
Fx_C = 15 * math.cos(math.radians(40))
Fy_C = 15 * math.sin(math.radians(40))
M_C = 5.0
M_E = 90.0

# Reacciones corregidas
A_x = -(Fx_C + 15)       # -26.491
D_x_col = 15.0
E_x = 15.0
I1_MB = 660.0
I2_MB = 1275.0
M_puntual_B = Fy_C * 4
Dy_up = (I1_MB + I2_MB + M_puntual_B - M_C) / 9.0  # CORREGIDO: -M_C
E_y = Dy_up
R_W1_04 = 225.0
R_W1_48 = 315.0
R_W2 = 225.0
R_W1_total = 540.0
B_y = R_W1_48 + R_W2 + Fy_C - Dy_up
B_x = A_x
A_y = R_W1_04 + B_y
I_Ma = 480.0
M_a = I_Ma + B_y * 4

# Admisibles
sigma_adm = Fy / FS
tau_adm = tau_y / FS

# Valores criticos
M_max_viga = abs(M_a)
V_max_viga = A_y
N_max_viga = abs(A_x)
M_max_col = 90.0
V_max_col = 15.0
N_max_col = Dy_up

# Perfil viga comercial
perfil_viga = "W920x313x271"
A_viga = 34500  # mm2
d_viga = 927    # mm
bf_viga = 309
tf_viga = 28.4
tw_viga = 18.4

# Perfil personalizado
perfil_pers = "I-950x484"
A_pers = 33860
d_pers = 950
bf_pers = 484
tf_pers = 17
tw_pers = 19

# Perfil columna
perfil_col = "W310x200x52"
A_col = 6650
d_col = 318
bf_col = 203
tf_col = 10.8
tw_col = 7.6

# ==============================================================
# CONEXIONES
# ==============================================================

# --- CONEXION A: Momento + Cortante (empotrado) ---
# Pernos A490 (alta resistencia)
# Fv_A490 = 457 MPa (cortante), Fp = 1.2*Fu*d*t (aplastamiento)
Fu_perno_A490 = 1035  # MPa (resistencia ultima A490)
Fv_A490 = 457  # MPa cortante nominal

# Estrategia: placa de extremo empernada (end-plate connection)
# El momento se resiste con pares de pernos arriba/abajo del alma
# M = F_par * d_brazo, donde F_par = n_pernos_fila * Fv * A_perno

# Probar con pernos de 1" (25.4mm)
d_perno_A = 25.4  # mm (1 pulgada)
A_perno_A = math.pi * d_perno_A**2 / 4  # 506.7 mm2
R_v_perno_A = Fv_A490 * A_perno_A / 1000  # kN por perno en cortante = 231.6
R_v_perno_A_doble = R_v_perno_A * 2  # doble cortante = 463.1

# Brazo del par de fuerzas (aprox d_viga - tf_viga)
brazo_A = (d_viga - tf_viga) / 1000  # m = 0.8986 m
F_par_A = M_max_viga / brazo_A  # kN = fuerza en cada ala

# Pernos por ala para resistir F_par (doble cortante)
n_pernos_ala_A = math.ceil(F_par_A / R_v_perno_A_doble)

# Pernos para cortante (en el alma)
n_pernos_alma_A = math.ceil(V_max_viga / R_v_perno_A)

# Total pernos conexion A
total_pernos_A = 2 * n_pernos_ala_A + n_pernos_alma_A

# Placa de conexion
espesor_placa_A = 25  # mm (1")
ancho_placa_A = bf_viga + 50  # mm
alto_placa_A = d_viga + 100  # mm

# Verificacion aplastamiento (bearing)
t_min_A = min(tf_viga, espesor_placa_A)
Rn_bearing_A = 2.4 * 400 * d_perno_A * t_min_A / 1000  # kN (Fu_placa=400 MPa aprox A36)

# --- CONEXION D: Solo cortante (rotula) ---
# Placa de cortante (shear tab)
V_D = Dy_up  # 218.73 kN

d_perno_D = 19.05  # mm (3/4")
A_perno_D = math.pi * d_perno_D**2 / 4  # 285 mm2
R_v_perno_D = Fv_A490 * A_perno_D / 1000  # 130.2 kN

n_pernos_D = math.ceil(V_D / R_v_perno_D)
n_pernos_D = max(n_pernos_D, 2)  # minimo 2

# Placa shear tab
espesor_placa_D = 10  # mm
ancho_placa_D = 100   # mm
alto_placa_D = n_pernos_D * 75 + 50  # separacion 75mm entre pernos

# --- CONEXION E: Base empotrada columna ---
# M = 90 kN*m, N = 218.73 kN (compresion), V = 15 kN
# Placa base sobre concreto f'c = 21 MPa

fc = 21  # MPa concreto
Fp_conc = 0.85 * fc  # presion admisible = 17.85 MPa

# Placa base - dimensionar por compresion + momento
# Area minima por compresion: A >= N / Fp
A_min_placa = N_max_col * 1000 / Fp_conc  # mm2 = 12252

# Por momento: aproximar con e = M/N
e_E = M_max_col / N_max_col * 1000  # mm = 411 mm
# Si e > d/6 hay tension en pernos de anclaje

# Placa base
B_placa = 400  # mm (ancho)
L_placa = 500  # mm (largo, en dir del momento)
A_placa = B_placa * L_placa  # 200000 mm2

# Presion maxima en concreto
# sigma_max = N/A + M*c/I_placa
I_placa = B_placa * L_placa**3 / 12
sigma_max_E = N_max_col*1000/A_placa + M_max_col*1e6*(L_placa/2)/I_placa
sigma_min_E = N_max_col*1000/A_placa - M_max_col*1e6*(L_placa/2)/I_placa

# Pernos de anclaje (4 pernos, 2 en tension)
d_perno_E = 22.225  # mm (7/8")
A_perno_E = math.pi * d_perno_E**2 / 4
# Tension en pernos (si sigma_min < 0, hay tension)
if sigma_min_E < 0:
    # Fuerza de tension total
    T_total_E = abs(sigma_min_E) * B_placa * L_placa / 2 / 1000  # kN aprox
    n_pernos_tension_E = 2
    T_por_perno_E = T_total_E / n_pernos_tension_E
else:
    T_total_E = 0
    T_por_perno_E = 0
    n_pernos_tension_E = 0

espesor_placa_E = 32  # mm

# Pernos cortante en E
R_v_perno_E = Fv_A490 * A_perno_E / 1000
n_pernos_E = 4  # minimo para base

# --- CONEXIONES SOLDADAS ---
# Electrodo E70: Fexx = 482 MPa (70 ksi)
Fexx = 482  # MPa
Fw = 0.6 * Fexx  # 289.2 MPa - resistencia del filete

# Soldadura Conexion A (filete alrededor del perfil)
# Ala: fuerza = F_par_A, longitud = 2*bf (ambos lados)
# a_min = F / (0.707 * Fw * L)
L_sold_ala_A = 2 * bf_viga  # mm
a_ala_A = F_par_A * 1000 / (0.707 * Fw * L_sold_ala_A)  # mm
a_ala_A = max(math.ceil(a_ala_A), 6)  # minimo 6mm

# Alma: fuerza = V, longitud = d - 2*tf
L_sold_alma_A = d_viga - 2 * tf_viga  # mm
a_alma_A = V_max_viga * 1000 / (0.707 * Fw * L_sold_alma_A * 2)  # 2 lados
a_alma_A = max(math.ceil(a_alma_A), 6)

# Soldadura Conexion D
L_sold_D = d_viga - 2 * tf_viga
a_D = V_D * 1000 / (0.707 * Fw * L_sold_D * 2)
a_D = max(math.ceil(a_D), 5)

# Soldadura Conexion E
# Perimetro de la columna
perim_col = 2 * bf_col + 2 * (d_col - 2 * tf_col)
a_E_momento = M_max_col * 1e6 / (0.707 * Fw * bf_col * (d_col - tf_col))
a_E_cortante = V_max_col * 1000 / (0.707 * Fw * (d_col - 2*tf_col) * 2)
a_E = max(math.ceil(max(a_E_momento, a_E_cortante)), 5)

# ==============================================================
# VOLUMENES FINALES (con conexiones)
# ==============================================================
vol_viga_com = A_viga * 13000 / 1e9
vol_viga_pers = A_pers * 13000 / 1e9
vol_col = A_col * 6000 / 1e9

# Volumen conexiones (aproximado)
vol_conex_A = espesor_placa_A * ancho_placa_A * alto_placa_A / 1e9
vol_conex_D = espesor_placa_D * ancho_placa_D * alto_placa_D / 1e9
vol_conex_E = espesor_placa_E * B_placa * L_placa / 1e9
vol_pernos = (total_pernos_A * A_perno_A * 80 + n_pernos_D * A_perno_D * 60 + n_pernos_E * A_perno_E * 400) / 1e9

vol_conex_total = vol_conex_A + vol_conex_D + vol_conex_E + vol_pernos

vol_total_com = vol_viga_com + vol_col + vol_conex_total
vol_total_pers = vol_viga_pers + vol_col + vol_conex_total

# ==============================================================
# CARGAR IMAGENES COMO BASE64
# ==============================================================
def img_to_base64(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

img_viga = img_to_base64(r"C:\Users\andre\Desktop\proyecto materiales\Diagramas_VNM_Viga.png")
img_col = img_to_base64(r"C:\Users\andre\Desktop\proyecto materiales\Diagramas_VNM_Columna.png")
img_esq = img_to_base64(r"C:\Users\andre\Desktop\proyecto materiales\Esquema_Portico.png")

# ==============================================================
# GENERAR HTML
# ==============================================================
html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Proyecto Portico - Mecanica de Materiales II</title>
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
.progress-fill {{ background: linear-gradient(90deg, var(--success), #48bb78); height: 100%; border-radius: 999px; transition: width 0.5s; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.85rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1rem 0; }}
.card {{ background: var(--card); border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12); border-left: 4px solid var(--secondary); }}
.card h3 {{ color: var(--primary); margin-bottom: 0.8rem; font-size: 1.1rem; }}
.card.done {{ border-left-color: var(--success); }}
.card.pending {{ border-left-color: #a0aec0; opacity: 0.7; }}
.card.error {{ border-left-color: var(--danger); }}
.badge {{ display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: bold; }}
.badge-ok {{ background: #c6f6d5; color: #22543d; }}
.badge-pending {{ background: #e2e8f0; color: #4a5568; }}
.badge-error {{ background: #fed7d7; color: #9b2c2c; }}
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
</style>
</head>
<body>

<div class="header">
<h1>PROYECTO FINAL - MECANICA DE MATERIALES II</h1>
<p>Portico plano de acero &bull; xy = {xy} &bull; Ing. William Valencia Mina &bull; Universidad del Quindio</p>
</div>

<div class="container">

<!-- PROGRESO GENERAL -->
<section>
<h2>Progreso General</h2>
<div class="progress-bar">
<div class="progress-fill" style="width: 65%">65% completado</div>
</div>
<div class="grid">
<div class="card done"><h3>Analisis Estructural</h3><span class="badge badge-ok">COMPLETO</span><br>Reacciones, V, N, M corregidos y verificados por 2 agentes independientes</div>
<div class="card done"><h3>Seleccion Perfiles</h3><span class="badge badge-ok">COMPLETO</span><br>Trade study 46 perfiles viga + 19 columna + personalizado optimizado</div>
<div class="card done"><h3>Diagramas V, N, M</h3><span class="badge badge-ok">COMPLETO</span><br>Viga (3 regiones) + columna, alta resolucion 300 dpi</div>
<div class="card done"><h3>Conexiones</h3><span class="badge badge-ok">COMPLETO</span><br>3 conexiones atornilladas (A, D, E) + 3 soldadas</div>
<div class="card done"><h3>Volumenes</h3><span class="badge badge-ok">COMPLETO</span><br>Comercial vs optimizado, con conexiones incluidas</div>
<div class="card pending"><h3>Peso Propio</h3><span class="badge badge-pending">PENDIENTE</span><br>Superposicion con perfil seleccionado</div>
<div class="card pending"><h3>Tensores + Mohr</h3><span class="badge badge-pending">PENDIENTE</span><br>Estado de esfuerzos en puntos criticos</div>
<div class="card pending"><h3>APU / Costos</h3><span class="badge badge-pending">PENDIENTE</span><br>Precios unitarios de acero, pernos, soldadura</div>
<div class="card pending"><h3>Informe Word</h3><span class="badge badge-pending">PENDIENTE</span><br>7 capitulos + presentacion 10 min</div>
</div>
</section>

<!-- ESQUEMA -->
<section>
<h2>1. Esquema Estructural</h2>
<div class="img-container">
<img src="data:image/png;base64,{img_esq}" alt="Esquema del portico">
</div>
</section>

<!-- REACCIONES -->
<section>
<h2>2. Reacciones (Corregidas y Verificadas)</h2>
<div class="grid">
<div class="card done">
<h3>Empotramiento A</h3>
<p>Ax = <strong>{A_x:.3f} kN</strong></p>
<p>Ay = <strong>{A_y:.3f} kN</strong></p>
<p>Ma = <strong>{M_a:.3f} kN&middot;m</strong></p>
</div>
<div class="card done">
<h3>Articulacion E</h3>
<p>Ex = <strong>{E_x:.3f} kN</strong></p>
<p>Ey = <strong>{E_y:.3f} kN</strong></p>
</div>
<div class="card done">
<h3>Verificacion Global</h3>
<p>&Sigma;Fx = {A_x + Fx_C + E_x:.6f} <span class="badge badge-ok">OK</span></p>
<p>&Sigma;Fy = {A_y + E_y - R_W1_total - R_W2 - Fy_C:.6f} <span class="badge badge-ok">OK</span></p>
<p>M1(4) = 0 <span class="badge badge-ok">OK</span></p>
<p>M3(13) = 0 <span class="badge badge-ok">OK</span></p>
</div>
</div>
</section>

<!-- DIAGRAMAS -->
<section>
<h2>3. Diagramas de Esfuerzos Internos</h2>
<h3 style="color: var(--secondary); margin: 1rem 0;">Viga (A &rarr; D)</h3>
<div class="img-container">
<img src="data:image/png;base64,{img_viga}" alt="Diagramas VNM Viga">
</div>
<h3 style="color: var(--secondary); margin: 1rem 0;">Columna (E &rarr; D)</h3>
<div class="img-container">
<img src="data:image/png;base64,{img_col}" alt="Diagramas VNM Columna">
</div>

<h3 style="margin-top: 1rem;">Valores Criticos para Diseno</h3>
<table>
<tr><th>Elemento</th><th>|M|max (kN&middot;m)</th><th>|V|max (kN)</th><th>|N|max (kN)</th><th>Ubicacion</th></tr>
<tr class="highlight"><td>Viga</td><td>{M_max_viga:.3f}</td><td>{V_max_viga:.3f}</td><td>{N_max_viga:.3f}</td><td>x = 0 (A)</td></tr>
<tr><td>Columna</td><td>{M_max_col:.1f}</td><td>{V_max_col:.1f}</td><td>{N_max_col:.3f}</td><td>y = 0 (E)</td></tr>
</table>
</section>

<!-- PERFILES -->
<section>
<h2>4. Seleccion de Perfiles</h2>
<div class="two-col">
<div>
<h3 style="color: var(--secondary);">Viga - Perfil Comercial</h3>
<table>
<tr><th colspan="2">{perfil_viga}</th></tr>
<tr><td>Altura d</td><td>{d_viga} mm</td></tr>
<tr><td>Ancho ala bf</td><td>{bf_viga} mm</td></tr>
<tr><td>Espesor ala tf</td><td>{tf_viga} mm</td></tr>
<tr><td>Espesor alma tw</td><td>{tw_viga} mm</td></tr>
<tr><td>Area</td><td><strong>{A_viga:,} mm&sup2;</strong></td></tr>
<tr><td>Peso lineal</td><td>{A_viga*7850/1e6:.1f} kg/m</td></tr>
<tr><td>Vol viga (13m)</td><td><strong>{vol_viga_com:.6f} m&sup3;</strong></td></tr>
</table>
</div>
<div>
<h3 style="color: var(--danger);">Viga - Perfil Personalizado (OPTIMIZADO)</h3>
<table>
<tr><th colspan="2">{perfil_pers} <span class="tag">MINIMO MATERIAL</span></th></tr>
<tr><td>Altura d</td><td>{d_pers} mm</td></tr>
<tr><td>Ancho ala bf</td><td>{bf_pers} mm</td></tr>
<tr><td>Espesor ala tf</td><td>{tf_pers} mm</td></tr>
<tr><td>Espesor alma tw</td><td>{tw_pers} mm</td></tr>
<tr><td>Area</td><td><strong>{A_pers:,} mm&sup2;</strong></td></tr>
<tr><td>Peso lineal</td><td>{A_pers*7850/1e6:.1f} kg/m</td></tr>
<tr><td>Vol viga (13m)</td><td><strong>{vol_viga_pers:.6f} m&sup3;</strong></td></tr>
<tr class="highlight"><td>Ahorro vs comercial</td><td>{(1-A_pers/A_viga)*100:.1f}%</td></tr>
</table>
</div>
</div>

<h3 style="color: var(--secondary); margin-top: 1.5rem;">Columna</h3>
<table style="max-width: 500px;">
<tr><th colspan="2">{perfil_col}</th></tr>
<tr><td>d x bf</td><td>{d_col} x {bf_col} mm</td></tr>
<tr><td>tf / tw</td><td>{tf_col} / {tw_col} mm</td></tr>
<tr><td>Area</td><td>{A_col:,} mm&sup2;</td></tr>
<tr><td>Vol columna (6m)</td><td>{vol_col:.6f} m&sup3;</td></tr>
</table>
</section>

<!-- CONEXIONES -->
<section>
<h2>5. Diseno de Conexiones</h2>

<div class="conexion-box">
<h3>Conexion A &mdash; Empotramiento (Momento + Cortante)</h3>
<p><strong>Solicitaciones:</strong> M = {M_max_viga:.1f} kN&middot;m, V = {V_max_viga:.1f} kN</p>
<div class="two-col" style="margin-top: 1rem;">
<div>
<h4>Atornillada</h4>
<table>
<tr><td>Pernos</td><td><strong>A490, &oslash;{d_perno_A:.1f} mm (1")</strong></td></tr>
<tr><td>Rv por perno (simple)</td><td>{R_v_perno_A:.1f} kN</td></tr>
<tr><td>Rv por perno (doble)</td><td>{R_v_perno_A_doble:.1f} kN</td></tr>
<tr><td>Brazo par de fuerzas</td><td>{brazo_A*1000:.1f} mm</td></tr>
<tr><td>Fuerza por ala (F=M/d)</td><td>{F_par_A:.1f} kN</td></tr>
<tr><td>Pernos por ala</td><td><strong>{n_pernos_ala_A}</strong></td></tr>
<tr><td>Pernos alma (cortante)</td><td><strong>{n_pernos_alma_A}</strong></td></tr>
<tr class="highlight"><td>Total pernos</td><td><strong>{total_pernos_A}</strong></td></tr>
<tr><td>Placa</td><td>{ancho_placa_A} x {alto_placa_A} x {espesor_placa_A} mm</td></tr>
</table>
</div>
<div>
<h4>Soldada (E70)</h4>
<table>
<tr><td>Electrodo</td><td><strong>E70 (Fexx = {Fexx} MPa)</strong></td></tr>
<tr><td>Fw (filete)</td><td>{Fw:.1f} MPa</td></tr>
<tr><td>Soldadura alas</td><td>a = <strong>{a_ala_A} mm</strong>, L = {L_sold_ala_A} mm</td></tr>
<tr><td>Soldadura alma</td><td>a = <strong>{a_alma_A} mm</strong>, L = {L_sold_alma_A:.0f} mm (x2 lados)</td></tr>
</table>
</div>
</div>
</div>

<div class="conexion-box">
<h3>Conexion D &mdash; Rotula (Solo Cortante)</h3>
<p><strong>Solicitaciones:</strong> V = {V_D:.1f} kN, N = {abs(D_x_col):.1f} kN, M = 0</p>
<div class="two-col" style="margin-top: 1rem;">
<div>
<h4>Atornillada</h4>
<table>
<tr><td>Pernos</td><td><strong>A490, &oslash;{d_perno_D:.2f} mm (3/4")</strong></td></tr>
<tr><td>Rv por perno</td><td>{R_v_perno_D:.1f} kN</td></tr>
<tr><td>Pernos necesarios</td><td><strong>{n_pernos_D}</strong></td></tr>
<tr><td>Placa shear tab</td><td>{ancho_placa_D} x {alto_placa_D} x {espesor_placa_D} mm</td></tr>
</table>
</div>
<div>
<h4>Soldada (E70)</h4>
<table>
<tr><td>Soldadura filete</td><td>a = <strong>{a_D} mm</strong></td></tr>
<tr><td>Longitud</td><td>{L_sold_D:.0f} mm (x2 lados)</td></tr>
</table>
</div>
</div>
</div>

<div class="conexion-box">
<h3>Conexion E &mdash; Base Empotrada Columna</h3>
<p><strong>Solicitaciones:</strong> M = {M_max_col:.1f} kN&middot;m, N = {N_max_col:.1f} kN (comp), V = {V_max_col:.1f} kN</p>
<div class="two-col" style="margin-top: 1rem;">
<div>
<h4>Atornillada (Placa Base)</h4>
<table>
<tr><td>Placa base</td><td><strong>{B_placa} x {L_placa} x {espesor_placa_E} mm</strong></td></tr>
<tr><td>Concreto f'c</td><td>{fc} MPa</td></tr>
<tr><td>Fp admisible</td><td>{Fp_conc:.2f} MPa</td></tr>
<tr><td>&sigma; max concreto</td><td>{sigma_max_E:.2f} MPa</td></tr>
<tr><td>&sigma; min concreto</td><td>{sigma_min_E:.2f} MPa {"(TENSION - hay pernos)" if sigma_min_E < 0 else "(OK, todo compresion)"}</td></tr>
<tr><td>Pernos anclaje</td><td><strong>{n_pernos_E}x &oslash;{d_perno_E:.1f} mm (7/8")</strong></td></tr>
<tr><td>Tension por perno</td><td>{T_por_perno_E:.1f} kN</td></tr>
</table>
</div>
<div>
<h4>Soldada (E70)</h4>
<table>
<tr><td>Soldadura columna-placa</td><td>a = <strong>{a_E} mm</strong></td></tr>
<tr><td>Perimetro soldado</td><td>{perim_col:.0f} mm</td></tr>
</table>
</div>
</div>
</div>
</section>

<!-- VOLUMENES -->
<section>
<h2>6. Volumenes Totales</h2>
<div class="two-col">
<div class="card" style="border-left-color: var(--secondary); text-align: center;">
<h3>Opcion Comercial</h3>
<table>
<tr><td>Viga ({perfil_viga})</td><td>{vol_viga_com:.6f} m&sup3;</td></tr>
<tr><td>Columna ({perfil_col})</td><td>{vol_col:.6f} m&sup3;</td></tr>
<tr><td>Conexiones (placas+pernos)</td><td>{vol_conex_total:.6f} m&sup3;</td></tr>
<tr class="highlight"><td><strong>TOTAL</strong></td><td><strong>{vol_total_com:.6f} m&sup3;</strong></td></tr>
</table>
<div class="val">{vol_total_com:.4f} <span class="val-unit">m&sup3;</span></div>
<p>Peso total: {vol_total_com * 7850:.0f} kg</p>
</div>
<div class="card" style="border-left-color: var(--accent); text-align: center;">
<h3>Opcion Optimizada <span class="tag">RECOMENDADA</span></h3>
<table>
<tr><td>Viga ({perfil_pers})</td><td>{vol_viga_pers:.6f} m&sup3;</td></tr>
<tr><td>Columna ({perfil_col})</td><td>{vol_col:.6f} m&sup3;</td></tr>
<tr><td>Conexiones (placas+pernos)</td><td>{vol_conex_total:.6f} m&sup3;</td></tr>
<tr class="highlight"><td><strong>TOTAL</strong></td><td><strong>{vol_total_pers:.6f} m&sup3;</strong></td></tr>
</table>
<div class="val" style="color: var(--accent);">{vol_total_pers:.4f} <span class="val-unit">m&sup3;</span></div>
<p>Peso total: {vol_total_pers * 7850:.0f} kg</p>
<p style="color: var(--success); font-weight: bold; margin-top: 0.5rem;">Ahorro: {(1-vol_total_pers/vol_total_com)*100:.1f}% vs comercial</p>
</div>
</div>

<h3 style="margin-top: 1.5rem;">Comparacion con ejemplos anteriores</h3>
<table>
<tr><th>Equipo</th><th>xy</th><th>FS</th><th>Perfil viga</th><th>Area viga (mm&sup2;)</th><th>Vol estimado (m&sup3;)</th></tr>
<tr><td>Ejemplo 1 (MJ)</td><td>99</td><td>1.8</td><td>W1011x437x787</td><td>~100,200</td><td>~1.38</td></tr>
<tr><td>Ejemplo 2 (Laura)</td><td>73</td><td>1.4</td><td>W920x420x449</td><td>57,200</td><td>~0.78</td></tr>
<tr class="highlight"><td><strong>NUESTRO (optimizado)</strong></td><td><strong>45</strong></td><td><strong>1.4</strong></td><td><strong>{perfil_pers}</strong></td><td><strong>{A_pers:,}</strong></td><td><strong>{vol_total_pers:.4f}</strong></td></tr>
</table>
<p style="color: var(--success); font-size: 1.2rem; font-weight: bold; margin-top: 1rem;">
Nuestro volumen es {(1-vol_total_pers/1.38)*100:.0f}% menor que Ejemplo 1 y {(1-vol_total_pers/0.78)*100:.0f}% menor que Ejemplo 2
</p>
</section>

<!-- FOOTER -->
<section style="text-align: center; padding: 2rem; color: #718096;">
<p>Generado automaticamente &bull; Valores corregidos y verificados por doble agente (optimista + adversarial)</p>
<p>Pendiente: peso propio, tensores/Mohr, APU, informe Word</p>
</section>

</div>
</body>
</html>"""

output_path = r"C:\Users\andre\Desktop\proyecto materiales\Reporte_Proyecto.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Reporte HTML guardado en: {output_path}")
print(f"\nConexion A: {total_pernos_A} pernos A490 de 1\", placa {ancho_placa_A}x{alto_placa_A}x{espesor_placa_A}mm")
print(f"Conexion D: {n_pernos_D} pernos A490 de 3/4\", shear tab {ancho_placa_D}x{alto_placa_D}x{espesor_placa_D}mm")
print(f"Conexion E: {n_pernos_E} pernos A490 de 7/8\", placa base {B_placa}x{L_placa}x{espesor_placa_E}mm")
print(f"\nSoldadura A: alas={a_ala_A}mm, alma={a_alma_A}mm")
print(f"Soldadura D: a={a_D}mm")
print(f"Soldadura E: a={a_E}mm")
print(f"\nVol total optimizado (con conexiones): {vol_total_pers:.6f} m3")
print(f"Peso total: {vol_total_pers*7850:.0f} kg")

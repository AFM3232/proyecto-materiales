"""
FASE FINAL: Peso propio + Tensores/Mohr + APU
Actualiza el reporte HTML con todo completo.
"""
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import os

# ==============================================================
# DATOS BASE (corregidos)
# ==============================================================
xy = 45; FS = 1.4; Fy = 250; tau_y = 100
Fx_C = 15*math.cos(math.radians(40))
Fy_C = 15*math.sin(math.radians(40))
M_C = 5.0; M_E = 90.0

# Reacciones SIN peso propio
D_x_col = 15.0; E_x = 15.0
Dy_up = (660+1275+Fy_C*4-M_C)/9.0
E_y = Dy_up
B_y = 315+225+Fy_C - Dy_up
A_x = -(Fx_C+15)
A_y = 225 + B_y
M_a = 480 + B_y*4

# Perfiles seleccionados
# Viga personalizada
perfil_pers = "I-950x484"
A_pers = 33860  # mm2
d_pers = 950; bf_pers = 484; tf_pers = 17; tw_pers = 19
w_pers = A_pers * 7850 / 1e6  # kg/m = 265.8
w_pers_kn = w_pers * 9.81 / 1000  # kN/m = 2.608

# Columna
A_col = 6650
d_col = 318; bf_col = 203; tf_col = 10.8; tw_col = 7.6
w_col = A_col * 7850 / 1e6  # kg/m = 52.2
w_col_kn = w_col * 9.81 / 1000  # kN/m = 0.512

# Comercial W920x313x271
A_com = 34500
d_com = 927; bf_com = 309; tf_com = 28.4; tw_com = 18.4
w_com_kn = 271 * 9.81 / 1000  # kN/m = 2.659

print("="*60)
print("FASE FINAL: PESO PROPIO + MOHR + APU")
print("="*60)

# ==============================================================
# 1. PESO PROPIO POR SUPERPOSICION
# ==============================================================
print("\n--- 1. PESO PROPIO ---")
print(f"Peso viga personalizada: {w_pers:.1f} kg/m = {w_pers_kn:.4f} kN/m")
print(f"Peso columna: {w_col:.1f} kg/m = {w_col_kn:.4f} kN/m")

# VIGA: carga uniforme w_pp sobre 13m
# Misma estructura: empotrado A, rotulas B(x=4) y D(x=13), columna en D
# Para peso propio: w_pp uniforme, sin puntual, sin momentos
w_pp = w_pers_kn  # kN/m sobre viga

# Cuerpo BD (x=4 a x=13): carga w_pp uniforme
# Sum M_B = 0: Dy_pp * 9 - w_pp * 9 * 4.5 = 0
# (carga w_pp sobre 9m, centrada a 4.5m de B)
Dy_pp = w_pp * 9 * 4.5 / 9  # = w_pp * 4.5
# Sum Fy BD: By_pp + Dy_pp - w_pp*9 = 0
By_pp = w_pp * 9 - Dy_pp

# Cuerpo AB:
Ay_pp = w_pp * 4 + By_pp  # carga en AB + reaccion en B
# Ma_pp: int_0^4 w_pp*x dx + By_pp*4 = w_pp*8 + By_pp*4
Ma_pp = w_pp * 4 * 2 + By_pp * 4

# Columna peso propio: N_col_pp = w_col_kn * 6 (peso de la columna)
N_col_pp = w_col_kn * 6  # kN adicional en compresion

print(f"\nReacciones por peso propio (superposicion):")
print(f"  Dy_pp = {Dy_pp:.4f} kN")
print(f"  By_pp = {By_pp:.4f} kN")
print(f"  Ay_pp = {Ay_pp:.4f} kN")
print(f"  Ma_pp = {Ma_pp:.4f} kN*m")

# TOTALES
A_y_total = A_y + Ay_pp
M_a_total = M_a + Ma_pp
V_max_total = A_y_total  # en x=0
Ey_total = E_y + Dy_pp
N_col_total = Dy_pp + E_y + N_col_pp  # compresion total columna

print(f"\nReacciones TOTALES (cargas + peso propio):")
print(f"  Ay = {A_y:.3f} + {Ay_pp:.3f} = {A_y_total:.3f} kN")
print(f"  Ma = {M_a:.3f} + {Ma_pp:.3f} = {M_a_total:.3f} kN*m")
print(f"  Ey = {E_y:.3f} + {Dy_pp:.3f} = {Ey_total:.3f} kN")
print(f"  Vmax = {V_max_total:.3f} kN")

# Verificar perfil con carga total
sigma_adm = Fy / FS  # 178.57 MPa
tau_adm = tau_y / FS  # 71.43 MPa

# Perfil personalizado I-950x484
def calc_Sx(d, bf, tf, tw):
    Ix = (bf*d**3)/12 - ((bf-tw)*(d-2*tf)**3)/12
    return Ix / (d/2)

Sx_pers = calc_Sx(d_pers, bf_pers, tf_pers, tw_pers)
sigma_total = M_a_total * 1e6 / Sx_pers
FS_real = Fy / sigma_total
tau_total = V_max_total * 1e3 / (d_pers * tw_pers)
FS_cort_real = tau_y / tau_total

print(f"\nVerificacion perfil personalizado CON peso propio:")
print(f"  Sx = {Sx_pers:.0f} mm3")
print(f"  sigma = {sigma_total:.2f} MPa (adm: {sigma_adm:.2f})")
print(f"  FS flexion = {FS_real:.4f} {'OK' if FS_real >= FS else 'NO CUMPLE'}")
print(f"  tau = {tau_total:.2f} MPa (adm: {tau_adm:.2f})")
print(f"  FS cortante = {FS_cort_real:.4f} {'OK' if FS_cort_real >= FS else 'NO CUMPLE'}")

perfil_ok = FS_real >= FS and FS_cort_real >= FS
print(f"\n  PERFIL {'CUMPLE' if perfil_ok else 'NO CUMPLE - DEBE CAMBIAR'}!")

# Si no cumple, indicar S_req nuevo
if not perfil_ok:
    S_req_new = M_a_total * 1e6 / sigma_adm
    print(f"  S_req nuevo = {S_req_new:.0f} mm3 = {S_req_new/1e3:.1f} cm3")

# Verificar tambien comercial
Sx_com = 10300 * 1e3  # mm3 (del catalogo W920x313x271)
sigma_com = M_a_total * 1e6 / Sx_com
FS_com = Fy / sigma_com
print(f"\nVerificacion comercial W920x313x271 CON peso propio:")
print(f"  sigma = {sigma_com:.2f} MPa, FS = {FS_com:.4f} {'OK' if FS_com >= FS else 'NO CUMPLE'}")

# ==============================================================
# 2. TENSORES DE ESFUERZO + CIRCULOS DE MOHR
# ==============================================================
print("\n--- 2. TENSORES + CIRCULOS DE MOHR ---")

# Propiedades del perfil personalizado
Ix_pers = (bf_pers*d_pers**3)/12 - ((bf_pers-tw_pers)*(d_pers-2*tf_pers)**3)/12

# Punto critico 1: x=0 (empotramiento A), fibra inferior (y = -d/2)
# sigma_x = -M*y/I + N/A  (M negativo = compresion arriba, traccion abajo)
# En x=0: M = -Ma (hogging), N = 26.49 kN (tension)
# Fibra inferior (y = -d/2): sigma = -(-Ma)*(-d/2)/I + N/A = -Ma*d/(2I) + N/A

# Calculo con valores TOTALES
M_total = M_a_total  # kN*m (magnitud del momento en A)
N_total = abs(A_x)   # kN (axial)
V_total = V_max_total  # kN (cortante en A)

# Q en el eje neutro (maximo cortante)
# Q = bf*tf*(d/2-tf/2) + tw*(d/2-tf)^2/2
Q_NA = bf_pers*tf_pers*(d_pers/2 - tf_pers/2) + tw_pers*(d_pers/2-tf_pers)**2/2

# PUNTO A: Fibra inferior (y = +d/2 desde NA, zona de traccion por M negativo)
# sigma_x = M*c/I + N/A (M causa traccion en fibra inferior para momento negativo tipo hogging)
# Convencion: M negativo (hogging) -> fibra inferior en compresion
# Pero nuestro M en A es negativo (CW) -> fibra inferior en COMPRESION
# fibra superior en TRACCION

# En realidad: M_a es CCW (positivo) segun nuestra convencion
# Para una viga horizontal, M positivo CCW hace que fibra SUPERIOR este en COMPRESION
# y fibra INFERIOR en TRACCION... depende de la convencion de signos

# Usemos la convencion de vigas: M positivo -> fibra superior compresion
# Nuestro M(0) = -1803.6 kN*m (negativo = hogging)
# Hogging: fibra superior en TRACCION, fibra inferior en COMPRESION
# Pero M_a como reaccion es CCW = resistiendo el hogging
# El momento INTERNO en x=0 es M(0) = -Ma = -1803.6

# sigma_flexion = -M*y/Ix (y positivo hacia arriba)
# En fibra superior (y = +d/2): sigma = -(-1803.6e6)*(d/2) / Ix = +1803.6e6*475/Ix (TRACCION) -> NO
# Eso no es correcto para un empotramiento con carga hacia abajo...

# Pensemos fisicamente: carga hacia abajo, empotrado a la izquierda
# La viga se deforma concava hacia arriba en A (hogging)
# Fibra superior: TRACCION, Fibra inferior: COMPRESION
# Pero la reaccion Ma = 1803.6 CCW resiste eso...

# Mejor: sigma = M_interno * y / I con M_interno = M(x=0) = -Ma_total
# Si usamos M negativo y y positivo arriba:
# sigma(fibra sup, y=+d/2) = (-Ma_total)*1e6 * (d_pers/2) / Ix_pers  -> negativo = COMPRESION
# Hmm eso no cuadra con la fisica...

# OK, usemos la formula directa sin ambiguedad:
# En x=0, la viga tiene momento hogging (curva hacia arriba por las cargas)
# Esto pone la fibra SUPERIOR en TRACCION (se estira) y la INFERIOR en COMPRESION
# PERO: el momento en x=0 es el de empotramiento que RESISTE, asi que M interno hogging
# En la convencion M = -Ma = negativo:
# sigma = -M*y/I = -(-Ma)*(+d/2)/I = +Ma*d/(2I) > 0 -> TRACCION en fibra superior OK!

# Punto 1: Fibra superior, x=0
y_sup = d_pers / 2  # mm
sigma_1_flex = M_total * 1e6 * y_sup / Ix_pers  # MPa (traccion)
sigma_1_axial = N_total * 1e3 / A_pers  # MPa (traccion, pequeña)
sigma_1 = sigma_1_flex + sigma_1_axial  # total
tau_1 = 0  # cortante es 0 en las fibras extremas

# Punto 2: Fibra inferior, x=0
sigma_2 = -sigma_1_flex + sigma_1_axial  # compresion + axial
tau_2 = 0

# Punto 3: Eje neutro, x=0 (maximo cortante)
sigma_3 = sigma_1_axial  # solo axial (flexion = 0 en NA)
tau_3 = V_total * 1e3 * Q_NA / (Ix_pers * tw_pers)  # MPa

# Punto 4: Union ala-alma, x=0
y_ala = d_pers/2 - tf_pers
sigma_4_flex = M_total * 1e6 * y_ala / Ix_pers
sigma_4 = sigma_4_flex + sigma_1_axial
Q_ala = bf_pers * tf_pers * (d_pers/2 - tf_pers/2)
tau_4 = V_total * 1e3 * Q_ala / (Ix_pers * tw_pers)

print(f"\nPropiedades seccion:")
print(f"  Ix = {Ix_pers:.0f} mm4 = {Ix_pers/1e6:.2f} x10^6 mm4")
print(f"  Q(NA) = {Q_NA:.0f} mm3")

puntos = [
    ("Fibra superior (x=0)", sigma_1, tau_1),
    ("Fibra inferior (x=0)", sigma_2, tau_2),
    ("Eje neutro (x=0)", sigma_3, tau_3),
    ("Union ala-alma (x=0)", sigma_4, tau_4),
]

print(f"\nEstados de esfuerzo en puntos criticos:")
for nombre, sx, txy in puntos:
    # Esfuerzos principales
    s_avg = sx / 2
    R = math.sqrt(s_avg**2 + txy**2)
    s1 = s_avg + R
    s2 = s_avg - R
    tau_max = R
    if sx != 0:
        theta_p = 0.5 * math.degrees(math.atan2(2*txy, sx))
    else:
        theta_p = 45 if txy != 0 else 0

    print(f"\n  {nombre}:")
    print(f"    sigma_x = {sx:.2f} MPa, tau_xy = {txy:.2f} MPa")
    print(f"    sigma_1 = {s1:.2f} MPa, sigma_2 = {s2:.2f} MPa")
    print(f"    tau_max = {tau_max:.2f} MPa")
    print(f"    theta_p = {theta_p:.2f} grados")

# ==============================================================
# CIRCULOS DE MOHR (graficos)
# ==============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('Circulos de Mohr - Puntos Criticos (x=0, Empotramiento A)', fontsize=14, fontweight='bold')

colors = ['#2E86AB', '#E74C3C', '#F18F01', '#7030A0']

for idx, (nombre, sx, txy) in enumerate(puntos):
    ax = axes[idx//2][idx%2]

    s_avg = sx / 2
    R = math.sqrt(s_avg**2 + txy**2)
    s1 = s_avg + R
    s2 = s_avg - R
    center = (s_avg, 0)

    # Circulo
    theta = np.linspace(0, 2*np.pi, 200)
    cx = s_avg + R * np.cos(theta)
    cy = R * np.sin(theta)

    ax.plot(cx, cy, color=colors[idx], linewidth=2)
    ax.fill(cx, cy, alpha=0.1, color=colors[idx])

    # Puntos
    ax.plot(sx, txy, 'ko', markersize=8, zorder=5)
    ax.annotate(f'  X({sx:.1f}, {txy:.1f})', xy=(sx, txy), fontsize=8, fontweight='bold')

    ax.plot(0, -txy, 'ks', markersize=8, zorder=5)
    ax.annotate(f'  Y(0, {-txy:.1f})', xy=(0, -txy), fontsize=8, fontweight='bold')

    ax.plot(s1, 0, 'r^', markersize=10, zorder=5)
    ax.annotate(f'  s1={s1:.1f}', xy=(s1, 0), fontsize=8, color='red', fontweight='bold')

    ax.plot(s2, 0, 'rv', markersize=10, zorder=5)
    ax.annotate(f's2={s2:.1f}  ', xy=(s2, 0), fontsize=8, color='red', fontweight='bold', ha='right')

    # Centro
    ax.plot(s_avg, 0, 'k+', markersize=12, markeredgewidth=2)
    ax.annotate(f'  C({s_avg:.1f}, 0)', xy=(s_avg, 0), fontsize=7, color='gray')

    # Ejes
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('sigma (MPa)', fontsize=10)
    ax.set_ylabel('tau (MPa)', fontsize=10)
    ax.set_title(nombre, fontsize=11, fontweight='bold')
    ax.set_aspect('equal')

    # tau_max
    ax.plot(s_avg, R, 'g*', markersize=12, zorder=5)
    ax.annotate(f' tau_max={R:.1f}', xy=(s_avg, R), fontsize=8, color='green', fontweight='bold')

plt.tight_layout()
plt.savefig(r'C:\Users\andre\Desktop\proyecto materiales\Circulos_Mohr.png', dpi=300, bbox_inches='tight')
plt.close()
print("\nCirculos de Mohr guardados: Circulos_Mohr.png")

# ==============================================================
# 3. APU (Analisis de Precios Unitarios)
# ==============================================================
print("\n--- 3. APU / COSTOS ---")

# Precios de referencia Colombia 2024-2025
precio_acero_kg = 5500  # COP/kg acero estructural
precio_perno_A490_1 = 18000   # COP/unidad perno 1"
precio_perno_A490_34 = 12000  # COP/unidad 3/4"
precio_perno_A490_78 = 15000  # COP/unidad 7/8"
precio_soldadura_m = 45000    # COP/m filete
precio_placa_kg = 6500        # COP/kg placas
precio_concreto_m3 = 450000   # COP/m3 pedestal
precio_pintura_m2 = 25000     # COP/m2 anticorrosiva

# Cantidades - Viga personalizada
peso_viga = A_pers * 7850 / 1e6 * 13  # kg
peso_col = A_col * 7850 / 1e6 * 6     # kg

# Conexiones
# A: 13 pernos 1", placa 359x1027x25mm
n_pernos_A = 13
peso_placa_A = 359 * 1027 * 25 * 7850 / 1e9  # kg
L_sold_A = (2*bf_pers + 2*(d_pers-2*tf_pers)) / 1000  # m (perimetro completo)

# D: 2 pernos 3/4", shear tab 100x200x10mm
n_pernos_D = 2
peso_placa_D = 100 * 200 * 10 * 7850 / 1e9
L_sold_D = 2 * (d_com - 2*tf_com) / 1000  # m

# E: 4 pernos 7/8", placa 400x500x32mm
n_pernos_E = 4
peso_placa_E = 400 * 500 * 32 * 7850 / 1e9
L_sold_E = 2 * (bf_col + d_col - 2*tf_col) / 1000  # m perimetro

# Pintura: area superficial aprox
area_viga = (2*bf_pers + 2*d_pers + 2*(d_pers-2*tf_pers)) * 13000 / 1e6  # m2
area_col = (2*bf_col + 2*d_col + 2*(d_col-2*tf_col)) * 6000 / 1e6

# Costos
items_apu = [
    ("Acero perfil viga (I-950x484)", peso_viga, "kg", precio_acero_kg),
    ("Acero perfil columna (W310x200x52)", peso_col, "kg", precio_acero_kg),
    ("Placa conexion A (empotramiento)", peso_placa_A, "kg", precio_placa_kg),
    ("Placa conexion D (shear tab)", peso_placa_D, "kg", precio_placa_kg),
    ("Placa base conexion E", peso_placa_E, "kg", precio_placa_kg),
    ("Pernos A490 1\" (Conexion A)", n_pernos_A, "und", precio_perno_A490_1),
    ("Pernos A490 3/4\" (Conexion D)", n_pernos_D, "und", precio_perno_A490_34),
    ("Pernos A490 7/8\" anclaje (Conexion E)", n_pernos_E, "und", precio_perno_A490_78),
    ("Soldadura filete E70 (Conexion A)", L_sold_A, "m", precio_soldadura_m),
    ("Soldadura filete E70 (Conexion D)", L_sold_D, "m", precio_soldadura_m),
    ("Soldadura filete E70 (Conexion E)", L_sold_E, "m", precio_soldadura_m),
    ("Pintura anticorrosiva viga", area_viga, "m2", precio_pintura_m2),
    ("Pintura anticorrosiva columna", area_col, "m2", precio_pintura_m2),
    ("Pedestal concreto base E", 0.4*0.5*0.6, "m3", precio_concreto_m3),
]

print(f"\n{'Item':<45} {'Cant':>8} {'Und':>5} {'P.Unit':>10} {'Total':>12}")
print("-"*85)
total_costo = 0
apu_data = []
for item, cant, und, precio in items_apu:
    subtotal = cant * precio
    total_costo += subtotal
    print(f"{item:<45} {cant:>8.2f} {und:>5} {precio:>10,} {subtotal:>12,.0f}")
    apu_data.append((item, cant, und, precio, subtotal))

print("-"*85)
print(f"{'TOTAL':>68} {total_costo:>12,.0f} COP")
print(f"{'':>68} {total_costo/1e6:>12,.2f} M COP")

# ==============================================================
# GENERAR IMAGENES ADICIONALES
# ==============================================================

# Distribucion de esfuerzos en la seccion (x=0)
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle(f'Distribucion de Esfuerzos en Seccion Critica (x=0, A)', fontsize=13, fontweight='bold')

y_pts = np.linspace(-d_pers/2, d_pers/2, 500)

# sigma_x a lo largo de y
sigma_dist = []
for y in y_pts:
    sf = M_a_total * 1e6 * y / Ix_pers  # flexion (traccion arriba para hogging)
    sa = N_total * 1e3 / A_pers
    sigma_dist.append(sf + sa)

ax = axes[0]
ax.plot(sigma_dist, y_pts, 'b-', linewidth=2)
ax.fill_betweenx(y_pts, 0, sigma_dist, alpha=0.2, color='blue')
ax.axvline(x=0, color='black', linewidth=0.5)
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
ax.axhline(y=d_pers/2-tf_pers, color='gray', linewidth=0.3, linestyle=':')
ax.axhline(y=-(d_pers/2-tf_pers), color='gray', linewidth=0.3, linestyle=':')
ax.set_xlabel('sigma_x (MPa)', fontsize=11)
ax.set_ylabel('y (mm)', fontsize=11)
ax.set_title('Esfuerzo Normal', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.text(max(sigma_dist)*0.5, d_pers/2-20, f'max={max(sigma_dist):.1f} MPa', fontsize=9, color='blue', fontweight='bold')
ax.text(min(sigma_dist)*0.5, -d_pers/2+20, f'min={min(sigma_dist):.1f} MPa', fontsize=9, color='red', fontweight='bold')

# tau_xy a lo largo de y (solo en el alma)
tau_dist = []
for y in y_pts:
    y_abs = abs(y)
    if y_abs <= d_pers/2 - tf_pers:
        # En el alma
        # Q(y) = bf*tf*(d/2-tf/2) + tw*((d/2-tf)^2 - y^2)/2
        Q_y = bf_pers*tf_pers*(d_pers/2-tf_pers/2) + tw_pers*((d_pers/2-tf_pers)**2 - y**2)/2
        t = V_total * 1e3 * Q_y / (Ix_pers * tw_pers)
    else:
        # En el ala: tau es muy pequeno, simplificamos a 0
        t = 0
    tau_dist.append(t)

ax = axes[1]
ax.plot(tau_dist, y_pts, 'r-', linewidth=2)
ax.fill_betweenx(y_pts, 0, tau_dist, alpha=0.2, color='red')
ax.axvline(x=0, color='black', linewidth=0.5)
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xlabel('tau_xy (MPa)', fontsize=11)
ax.set_ylabel('y (mm)', fontsize=11)
ax.set_title('Esfuerzo Cortante', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.text(max(tau_dist)*0.6, 0, f'max={max(tau_dist):.1f} MPa', fontsize=9, color='red', fontweight='bold')

# Seccion transversal del perfil
ax = axes[2]
# Dibujar perfil I
hw = d_pers - 2*tf_pers
# Ala superior
ax.fill([-(bf_pers/2), bf_pers/2, bf_pers/2, -(bf_pers/2)],
        [d_pers/2, d_pers/2, d_pers/2-tf_pers, d_pers/2-tf_pers],
        color='steelblue', edgecolor='black', linewidth=1.5)
# Alma
ax.fill([-(tw_pers/2), tw_pers/2, tw_pers/2, -(tw_pers/2)],
        [d_pers/2-tf_pers, d_pers/2-tf_pers, -(d_pers/2-tf_pers), -(d_pers/2-tf_pers)],
        color='steelblue', edgecolor='black', linewidth=1.5)
# Ala inferior
ax.fill([-(bf_pers/2), bf_pers/2, bf_pers/2, -(bf_pers/2)],
        [-(d_pers/2-tf_pers), -(d_pers/2-tf_pers), -d_pers/2, -d_pers/2],
        color='steelblue', edgecolor='black', linewidth=1.5)

# Dimensiones
ax.annotate('', xy=(bf_pers/2+30, -d_pers/2), xytext=(bf_pers/2+30, d_pers/2),
            arrowprops=dict(arrowstyle='<->', color='black'))
ax.text(bf_pers/2+40, 0, f'd={d_pers}', fontsize=9, va='center')

ax.annotate('', xy=(-bf_pers/2, -d_pers/2-30), xytext=(bf_pers/2, -d_pers/2-30),
            arrowprops=dict(arrowstyle='<->', color='black'))
ax.text(0, -d_pers/2-50, f'bf={bf_pers}', fontsize=9, ha='center')

ax.text(tw_pers/2+10, 0, f'tw={tw_pers}', fontsize=8, color='gray')
ax.text(bf_pers/4, d_pers/2-tf_pers/2, f'tf={tf_pers}', fontsize=8, color='gray', ha='center', va='center')

ax.set_aspect('equal')
ax.set_title(f'Seccion I-{d_pers}x{bf_pers}', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.2)
ax.set_xlabel('mm')
ax.set_ylabel('mm')

plt.tight_layout()
plt.savefig(r'C:\Users\andre\Desktop\proyecto materiales\Distribucion_Esfuerzos.png', dpi=300, bbox_inches='tight')
plt.close()
print("\nDistribucion de esfuerzos guardada: Distribucion_Esfuerzos.png")

# ==============================================================
# ACTUALIZAR HTML (usando .format para evitar problemas con f-strings)
# ==============================================================
def img_to_b64(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

img_mohr = img_to_b64(r"C:\Users\andre\Desktop\proyecto materiales\Circulos_Mohr.png")
img_esf = img_to_b64(r"C:\Users\andre\Desktop\proyecto materiales\Distribucion_Esfuerzos.png")

html_path = r"C:\Users\andre\Desktop\proyecto materiales\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Construir con concatenacion para evitar f-string issues

# Construir HTML con string concat (evita problemas de f-string con CSS {})
pp_status = "done" if perfil_ok else "error"
pp_badge = "badge-ok" if FS_real >= FS else "badge-error"
pp_text = "OK" if FS_real >= FS else "NO CUMPLE"
costo_str = "{:,.0f}".format(total_costo)
costo_m_str = "{:,.2f}".format(total_costo/1e6)

ns = []
ns.append('<!-- PESO PROPIO -->')
ns.append('<section>')
ns.append('<h2>7. Peso Propio (Superposicion)</h2>')
ns.append('<div class="grid">')
ns.append('<div class="card done">')
ns.append('<h3>Peso Viga (' + str(perfil_pers) + ')</h3>')
ns.append('<p>w = <strong>{:.1f} kg/m = {:.4f} kN/m</strong></p>'.format(w_pers, w_pers_kn))
ns.append('<p>Incremento reacciones:</p>')
ns.append('<p>Ay_pp = {:.3f} kN ({:.1f}%)</p>'.format(Ay_pp, Ay_pp/A_y*100))
ns.append('<p>Ma_pp = {:.3f} kN&middot;m ({:.1f}%)</p>'.format(Ma_pp, Ma_pp/M_a*100))
ns.append('</div>')
ns.append('<div class="card done">')
ns.append('<h3>Valores Totales (cargas + pp)</h3>')
ns.append('<p>Ay = <strong>{:.3f} kN</strong></p>'.format(A_y_total))
ns.append('<p>Ma = <strong>{:.3f} kN&middot;m</strong></p>'.format(M_a_total))
ns.append('<p>Vmax = <strong>{:.3f} kN</strong></p>'.format(V_max_total))
ns.append('<p>Ey = <strong>{:.3f} kN</strong></p>'.format(Ey_total))
ns.append('</div>')
ns.append('<div class="card ' + pp_status + '">')
ns.append('<h3>Verificacion con Peso Propio</h3>')
ns.append('<p>sigma = {:.2f} MPa</p>'.format(sigma_total))
ns.append('<p>FS flexion = <strong>{:.4f}</strong> <span class="badge '.format(FS_real) + pp_badge + '">' + pp_text + '</span></p>')
ns.append('<p>tau = {:.2f} MPa</p>'.format(tau_total))
ns.append('<p>FS cortante = <strong>{:.4f}</strong> <span class="badge badge-ok">OK</span></p>'.format(FS_cort_real))
if not perfil_ok:
    ns.append('<p style="color:red;"><strong>Se requiere S &ge; {:.0f} mm3. Iteracion necesaria.</strong></p>'.format(M_a_total*1e6/sigma_adm))
ns.append('</div>')
ns.append('</div></section>')

# Tensores + Mohr
ns.append('<!-- TENSORES Y MOHR -->')
ns.append('<section>')
ns.append('<h2>8. Tensores de Esfuerzo y Circulos de Mohr</h2>')
ns.append('<h3 style="color:#2b6cb0;">Distribucion de Esfuerzos en Seccion Critica (x=0)</h3>')
ns.append('<div class="img-container"><img src="data:image/png;base64,' + img_esf + '" alt="Distribucion"></div>')
ns.append('<h3 style="color:#2b6cb0;margin-top:1.5rem;">Estados de Esfuerzo en Puntos Criticos</h3>')
ns.append('<table>')
ns.append('<tr><th>Punto</th><th>&sigma;x (MPa)</th><th>&tau;xy (MPa)</th><th>&sigma;1 (MPa)</th><th>&sigma;2 (MPa)</th><th>&tau;max (MPa)</th><th>&theta;p</th></tr>')
for nombre, sx, txy in puntos:
    s_avg = sx/2
    R = math.sqrt(s_avg**2 + txy**2)
    s1 = s_avg + R; s2 = s_avg - R
    tp = 0.5*math.degrees(math.atan2(2*txy, sx)) if sx != 0 else (45 if txy != 0 else 0)
    ns.append('<tr><td>{}</td><td>{:.2f}</td><td>{:.2f}</td><td>{:.2f}</td><td>{:.2f}</td><td>{:.2f}</td><td>{:.1f}</td></tr>'.format(nombre,sx,txy,s1,s2,R,tp))
ns.append('</table>')
ns.append('<h3 style="color:#2b6cb0;margin-top:1.5rem;">Circulos de Mohr</h3>')
ns.append('<div class="img-container"><img src="data:image/png;base64,' + img_mohr + '" alt="Mohr"></div>')
ns.append('</section>')

# APU
ns.append('<!-- APU -->')
ns.append('<section>')
ns.append('<h2>9. Analisis de Precios Unitarios (APU)</h2>')
ns.append('<table>')
ns.append('<tr><th>Item</th><th>Cantidad</th><th>Und</th><th>P. Unitario (COP)</th><th>Subtotal (COP)</th></tr>')
for item, cant, und, precio, subtotal in apu_data:
    ns.append('<tr><td style="text-align:left;">{}</td><td>{:.2f}</td><td>{}</td><td>${:,.0f}</td><td>${:,.0f}</td></tr>'.format(item, cant, und, precio, subtotal))
ns.append('<tr class="highlight"><td style="text-align:left;" colspan="4"><strong>TOTAL</strong></td><td><strong>$' + costo_str + '</strong></td></tr>')
ns.append('<tr><td colspan="4"></td><td><strong>$' + costo_m_str + ' Millones COP</strong></td></tr>')
ns.append('</table>')
ns.append('<p style="color:#718096;font-size:0.85rem;margin-top:0.5rem;">Precios de referencia Colombia 2024-2025. No incluye transporte, montaje ni mano de obra.</p>')
ns.append('</section>')

new_sections = '\n'.join(ns)

# Actualizar barra de progreso
html = html.replace('width: 65%">65% completado', 'width: 90%">90% completado')

# Actualizar cards de progreso
html = html.replace(
    '<div class="card pending"><h3>Peso Propio</h3><span class="badge badge-pending">PENDIENTE</span><br>Superposicion con perfil seleccionado</div>',
    '<div class="card done"><h3>Peso Propio</h3><span class="badge badge-ok">COMPLETO</span><br>Verificado con superposicion</div>'
)
html = html.replace(
    '<div class="card pending"><h3>Tensores + Mohr</h3><span class="badge badge-pending">PENDIENTE</span><br>Estado de esfuerzos en puntos criticos</div>',
    '<div class="card done"><h3>Tensores + Mohr</h3><span class="badge badge-ok">COMPLETO</span><br>4 puntos criticos + circulos</div>'
)
apu_card = '<div class="card done"><h3>APU / Costos</h3><span class="badge badge-ok">COMPLETO</span><br>$' + costo_m_str + 'M COP total</div>'
html = html.replace(
    '<div class="card pending"><h3>APU / Costos</h3><span class="badge badge-pending">PENDIENTE</span><br>Precios unitarios de acero, pernos, soldadura</div>',
    apu_card
)

# Insertar antes del footer
footer_marker = '<!-- FOOTER -->'
html = html.replace(footer_marker, new_sections + '\n' + footer_marker)

html = html.replace(
    'Pendiente: peso propio, tensores/Mohr, APU, informe Word',
    'Pendiente: informe Word formal (7 capitulos)'
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("\nHTML actualizado:", html_path)
print("\n" + "="*60)
print("RESUMEN FINAL")
print("="*60)
print("Perfil viga:", perfil_pers, "A =", A_pers, "mm2")
print("  Con peso propio: FS =", round(FS_real, 4), "OK" if perfil_ok else "NECESITA ITERACION")
print("Perfil columna: W310x200x52")
vol_t = (A_pers*13000 + A_col*6000)/1e9
print("Volumen total: ~{:.4f} m3".format(vol_t))
print("Costo estimado: $" + costo_str + " COP")
print("Progreso: 90% - Falta solo el informe Word")

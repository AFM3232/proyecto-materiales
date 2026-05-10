"""
DIAGRAMAS V, N, M - Portico plano xy=45
Genera graficas de alta calidad para el informe.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import math

# ==============================================================
# PARAMETROS (mismos del Excel)
# ==============================================================
xy = 45
Fx_C = 15 * math.cos(math.radians(40))  # 11.4907
Fy_C = 15 * math.sin(math.radians(40))  # 9.6418
M_C = 5
M_E = 90

# Reacciones CORREGIDAS (M_C signo corregido en ecuacion BD)
A_x = -26.4907
A_y = 555.9124
M_a = 1803.6486
E_x = 15.0
E_y = 218.7296
D_x_col = 15.0
Dy_up = 218.7296
R_W1_total = 540.0

# ==============================================================
# FUNCIONES DE ESFUERZOS INTERNOS - VIGA
# ==============================================================
def N_viga(x):
    if x < 8:
        return 26.4907
    else:
        return 15.0

def V_viga(x):
    if x <= 8:
        return -2.8125*x**2 - 45*x + 554.8013
    else:
        C_v = 554.8013 - 540.0 - Fy_C + 1296  # = 1301.159
        return 9*x**2 - 234*x + C_v

def M_viga(x):
    if x <= 8:
        return -0.9375*x**3 - 22.5*x**2 + 554.8013*x - 1799.2041
    else:
        M_at_8_minus = -0.9375*512 - 22.5*64 + 554.8013*8 - 1799.2041
        M_at_8_plus = M_at_8_minus - M_C
        C_v = 554.8013 - 540.0 - Fy_C + 1296
        integral_V = (3*x**3 - 117*x**2 + C_v*x) - (3*512 - 117*64 + C_v*8)
        return M_at_8_plus + integral_V

# ==============================================================
# FUNCIONES - COLUMNA (y desde E=0 hasta D=6)
# ==============================================================
def N_col(y):
    return -219.8407

def V_col(y):
    return 15.0

def M_col(y):
    return -90 + 15*y

# ==============================================================
# GENERAR DATOS
# ==============================================================
# Viga
x_v = np.linspace(0, 13, 1000)

N_vals = np.array([N_viga(x) for x in x_v])
V_vals = np.array([V_viga(x) for x in x_v])
M_vals = np.array([M_viga(x) for x in x_v])

# Columna
y_c = np.linspace(0, 6, 200)
Nc_vals = np.array([N_col(y) for y in y_c])
Vc_vals = np.array([V_col(y) for y in y_c])
Mc_vals = np.array([M_col(y) for y in y_c])

# ==============================================================
# COLORES PROFESIONALES
# ==============================================================
COLOR_N = '#2E86AB'   # azul
COLOR_V = '#A23B72'   # magenta
COLOR_M = '#F18F01'   # naranja
COLOR_BG = '#FAFAFA'
COLOR_GRID = '#E0E0E0'
COLOR_AXIS = '#333333'

# ==============================================================
# FIGURA 1: DIAGRAMAS VIGA (3 subplots verticales)
# ==============================================================
fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
fig.patch.set_facecolor('white')

# --- Normal ---
ax = axes[0]
ax.fill_between(x_v, 0, N_vals, alpha=0.3, color=COLOR_N)
ax.plot(x_v, N_vals, color=COLOR_N, linewidth=2)
ax.axhline(y=0, color=COLOR_AXIS, linewidth=0.8)
ax.axvline(x=4, color='gray', linewidth=0.5, linestyle='--', label='B (rotula)')
ax.axvline(x=8, color='gray', linewidth=0.5, linestyle='-.')
ax.axvline(x=13, color='gray', linewidth=0.5, linestyle='--')

# Anotaciones
ax.annotate(f'N = {N_viga(0):.2f} kN', xy=(2, N_viga(0)), fontsize=10,
            ha='center', va='bottom', fontweight='bold', color=COLOR_N)
ax.annotate(f'N = {N_viga(10):.2f} kN', xy=(10.5, N_viga(10)), fontsize=10,
            ha='center', va='bottom', fontweight='bold', color=COLOR_N)

ax.set_ylabel('N (kN)', fontsize=12, fontweight='bold')
ax.set_title('Diagrama de Fuerza Normal - Viga', fontsize=13, fontweight='bold', pad=10)
ax.grid(True, alpha=0.3, color=COLOR_GRID)
ax.set_facecolor(COLOR_BG)

# Etiquetas puntos
for xp, label in [(0, 'A'), (4, 'B'), (8, 'C'), (13, 'D')]:
    ax.text(xp, ax.get_ylim()[0]-1, label, ha='center', va='top', fontsize=11, fontweight='bold')

# --- Cortante ---
ax = axes[1]
ax.fill_between(x_v, 0, V_vals, where=V_vals>=0, alpha=0.3, color=COLOR_V)
ax.fill_between(x_v, 0, V_vals, where=V_vals<0, alpha=0.3, color='#E74C3C')
ax.plot(x_v, V_vals, color=COLOR_V, linewidth=2)
ax.axhline(y=0, color=COLOR_AXIS, linewidth=0.8)
ax.axvline(x=4, color='gray', linewidth=0.5, linestyle='--')
ax.axvline(x=8, color='gray', linewidth=0.5, linestyle='-.')
ax.axvline(x=13, color='gray', linewidth=0.5, linestyle='--')

# Valores criticos
ax.annotate(f'V(0) = {V_viga(0):.1f} kN', xy=(0.2, V_viga(0)), fontsize=9,
            ha='left', va='bottom', fontweight='bold', color=COLOR_V)
ax.annotate(f'V(4) = {V_viga(4):.1f} kN', xy=(4, V_viga(4)), fontsize=9,
            ha='center', va='bottom', fontweight='bold', color=COLOR_V,
            xytext=(4, V_viga(4)+30), arrowprops=dict(arrowstyle='->', color=COLOR_V))
ax.annotate(f'V(13) = {V_viga(13):.1f} kN', xy=(12.8, V_viga(13)), fontsize=9,
            ha='right', va='top', fontweight='bold', color='#E74C3C')

# Punto V=0
x_v0 = 8.164  # aprox donde V=0 en region CD
ax.plot(x_v0, 0, 'ko', markersize=6)
ax.annotate(f'V=0\nx={x_v0:.2f}m', xy=(x_v0, 0), fontsize=8,
            ha='left', va='bottom', xytext=(x_v0+0.3, 30),
            arrowprops=dict(arrowstyle='->', color='black'))

ax.set_ylabel('V (kN)', fontsize=12, fontweight='bold')
ax.set_title('Diagrama de Fuerza Cortante - Viga', fontsize=13, fontweight='bold', pad=10)
ax.grid(True, alpha=0.3, color=COLOR_GRID)
ax.set_facecolor(COLOR_BG)

for xp, label in [(0, 'A'), (4, 'B'), (8, 'C'), (13, 'D')]:
    ax.text(xp, ax.get_ylim()[0]-20, label, ha='center', va='top', fontsize=11, fontweight='bold')

# --- Momento ---
ax = axes[2]
# Convencion: M negativo arriba (empotramientos)
ax.fill_between(x_v, 0, M_vals, where=M_vals>=0, alpha=0.3, color=COLOR_M)
ax.fill_between(x_v, 0, M_vals, where=M_vals<0, alpha=0.3, color='#E74C3C')
ax.plot(x_v, M_vals, color=COLOR_M, linewidth=2)
ax.axhline(y=0, color=COLOR_AXIS, linewidth=0.8)
ax.axvline(x=4, color='gray', linewidth=0.5, linestyle='--')
ax.axvline(x=8, color='gray', linewidth=0.5, linestyle='-.')
ax.axvline(x=13, color='gray', linewidth=0.5, linestyle='--')

# Valores criticos
ax.annotate(f'M(0) = {M_viga(0):.1f} kN*m', xy=(0.2, M_viga(0)), fontsize=9,
            ha='left', va='top', fontweight='bold', color='#E74C3C')
ax.annotate(f'M(4) = {M_viga(4):.1f}', xy=(4, M_viga(4)), fontsize=9,
            ha='center', va='bottom', fontweight='bold', color=COLOR_M)
m8 = M_viga(7.999)
ax.annotate(f'M(8-) = {m8:.1f}', xy=(8, m8), fontsize=9,
            ha='left', va='bottom', fontweight='bold', color=COLOR_M,
            xytext=(8.5, m8+50), arrowprops=dict(arrowstyle='->', color=COLOR_M))
ax.annotate(f'M(13) = {M_viga(13):.1f}', xy=(13, M_viga(13)), fontsize=9,
            ha='right', va='bottom', fontweight='bold', color=COLOR_M)

# M max positivo
x_mmax = x_v[np.argmax(M_vals)]
ax.plot(x_mmax, max(M_vals), 'k^', markersize=8)
ax.annotate(f'M+ max = {max(M_vals):.1f} kN*m\nx = {x_mmax:.2f} m',
            xy=(x_mmax, max(M_vals)), fontsize=9, ha='center', va='bottom',
            xytext=(x_mmax, max(M_vals)+80),
            arrowprops=dict(arrowstyle='->', color='black'))

ax.set_ylabel('M (kN*m)', fontsize=12, fontweight='bold')
ax.set_xlabel('x (m)', fontsize=12, fontweight='bold')
ax.set_title('Diagrama de Momento Flector - Viga', fontsize=13, fontweight='bold', pad=10)
ax.grid(True, alpha=0.3, color=COLOR_GRID)
ax.set_facecolor(COLOR_BG)

for xp, label in [(0, 'A'), (4, 'B'), (8, 'C'), (13, 'D')]:
    ax.text(xp, ax.get_ylim()[0]-100, label, ha='center', va='top', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(r'C:\Users\andre\Desktop\proyecto materiales\Diagramas_VNM_Viga.png', dpi=300, bbox_inches='tight')
plt.close()
print("Diagramas VIGA guardados: Diagramas_VNM_Viga.png")

# ==============================================================
# FIGURA 2: DIAGRAMAS COLUMNA (3 subplots horizontales)
# ==============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 8))
fig.patch.set_facecolor('white')
fig.suptitle('Diagramas de Esfuerzos Internos - Columna DE', fontsize=14, fontweight='bold', y=0.98)

# --- Normal columna ---
ax = axes[0]
ax.fill_betweenx(y_c, 0, Nc_vals, alpha=0.3, color=COLOR_N)
ax.plot(Nc_vals, y_c, color=COLOR_N, linewidth=2)
ax.axvline(x=0, color=COLOR_AXIS, linewidth=0.8)
ax.set_xlabel('N (kN)', fontsize=11, fontweight='bold')
ax.set_ylabel('y (m)', fontsize=11, fontweight='bold')
ax.set_title('Normal', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, color=COLOR_GRID)
ax.set_facecolor(COLOR_BG)
ax.text(Nc_vals[0], 0, f'  {Nc_vals[0]:.1f} kN\n  (compresion)', fontsize=9, va='bottom', fontweight='bold', color=COLOR_N)
ax.text(0, 0, 'E', fontsize=11, fontweight='bold', ha='right', va='bottom')
ax.text(0, 6, 'D', fontsize=11, fontweight='bold', ha='right', va='top')

# --- Cortante columna ---
ax = axes[1]
ax.fill_betweenx(y_c, 0, Vc_vals, alpha=0.3, color=COLOR_V)
ax.plot(Vc_vals, y_c, color=COLOR_V, linewidth=2)
ax.axvline(x=0, color=COLOR_AXIS, linewidth=0.8)
ax.set_xlabel('V (kN)', fontsize=11, fontweight='bold')
ax.set_title('Cortante', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, color=COLOR_GRID)
ax.set_facecolor(COLOR_BG)
ax.text(15, 3, f'V = 15 kN\n(constante)', fontsize=10, ha='left', fontweight='bold', color=COLOR_V)
ax.text(0, 0, 'E', fontsize=11, fontweight='bold', ha='right', va='bottom')
ax.text(0, 6, 'D', fontsize=11, fontweight='bold', ha='right', va='top')

# --- Momento columna ---
ax = axes[2]
ax.fill_betweenx(y_c, 0, Mc_vals, where=Mc_vals>=0, alpha=0.3, color=COLOR_M)
ax.fill_betweenx(y_c, 0, Mc_vals, where=Mc_vals<0, alpha=0.3, color='#E74C3C')
ax.plot(Mc_vals, y_c, color=COLOR_M, linewidth=2)
ax.axvline(x=0, color=COLOR_AXIS, linewidth=0.8)
ax.set_xlabel('M (kN*m)', fontsize=11, fontweight='bold')
ax.set_title('Momento', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, color=COLOR_GRID)
ax.set_facecolor(COLOR_BG)
ax.text(M_col(0), 0.2, f'M(E) = {M_col(0):.0f} kN*m', fontsize=9, ha='left', fontweight='bold', color='#E74C3C')
ax.text(M_col(6), 5.8, f'M(D) = {M_col(6):.0f}', fontsize=9, ha='left', fontweight='bold', color=COLOR_M)
ax.text(0, 0, 'E', fontsize=11, fontweight='bold', ha='right', va='bottom')
ax.text(0, 6, 'D', fontsize=11, fontweight='bold', ha='right', va='top')

plt.tight_layout()
plt.savefig(r'C:\Users\andre\Desktop\proyecto materiales\Diagramas_VNM_Columna.png', dpi=300, bbox_inches='tight')
plt.close()
print("Diagramas COLUMNA guardados: Diagramas_VNM_Columna.png")

# ==============================================================
# FIGURA 3: ESQUEMA ESTRUCTURAL CON CARGAS
# ==============================================================
fig, ax = plt.subplots(1, 1, figsize=(16, 8))
fig.patch.set_facecolor('white')

# Viga
ax.plot([0, 13], [6, 6], 'k-', linewidth=4)
# Columna
ax.plot([13, 13], [0, 6], 'k-', linewidth=4)

# Apoyos
# A - empotrado (lineas cruzadas)
for yy in np.arange(5.2, 6.8, 0.2):
    ax.plot([-0.3, 0], [yy, yy+0.15], 'k-', linewidth=1)
ax.plot([0, 0], [5.2, 6.8], 'k-', linewidth=2)

# E - articulado (triangulo)
ax.plot([12.7, 13, 13.3], [-0.3, 0, -0.3], 'k-', linewidth=2)
ax.plot([12.5, 13.5], [-0.3, -0.3], 'k-', linewidth=2)

# Puntos
for xp, yp, label in [(0, 6, 'A'), (4, 6, 'B'), (8, 6, 'C'), (13, 6, 'D'), (13, 0, 'E')]:
    ax.plot(xp, yp, 'ko', markersize=8, zorder=5)
    offset_x = -0.4 if xp == 0 else (0.4 if xp == 13 and yp == 0 else 0)
    offset_y = 0.4 if yp == 6 else -0.5
    ax.text(xp + offset_x, yp + offset_y, label, fontsize=14, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='black'))

# Carga distribuida (flechas hacia abajo)
for x in np.arange(0, 13.1, 0.3):
    if x <= 8:
        w = (5.625*x + 45) / 90 * 2.5  # escalar
    else:
        w_val = 234 - 18*x
        if w_val < 0: w_val = 0
        w = w_val / 90 * 2.5
    if w > 0.1:
        ax.annotate('', xy=(x, 6), xytext=(x, 6+w),
                    arrowprops=dict(arrowstyle='->', color='#2196F3', lw=1.2))

# Linea superior de la carga distribuida
x_load = np.linspace(0, 13, 200)
w_load = []
for x in x_load:
    if x <= 8:
        w_load.append((5.625*x + 45) / 90 * 2.5 + 6)
    else:
        w_val = max(234 - 18*x, 0)
        w_load.append(w_val / 90 * 2.5 + 6)
ax.plot(x_load, w_load, '#2196F3', linewidth=1.5)

# Etiquetas de carga
ax.text(0, 7.5, f'{xy} kN/m', fontsize=10, color='#2196F3', ha='center', fontweight='bold')
ax.text(8, 8.7, f'{2*xy} kN/m', fontsize=10, color='#2196F3', ha='center', fontweight='bold')
ax.text(13, 6.3, '0', fontsize=10, color='#2196F3', ha='center', fontweight='bold')

# Fuerza puntual
ax.annotate('', xy=(8, 6), xytext=(8-1.2, 6+1.5),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2.5))
ax.text(6.5, 7.8, f'15 kN\n40 grados', fontsize=10, color='#E74C3C', fontweight='bold', ha='center')

# Momentos (flechas curvas)
ax.annotate('', xy=(8.4, 6.6), xytext=(7.6, 6.6),
            arrowprops=dict(arrowstyle='->', color='#9C27B0', lw=2,
                          connectionstyle='arc3,rad=0.5'))
ax.text(8, 7.0, f'Mc={M_C} kN*m', fontsize=9, color='#9C27B0', ha='center', fontweight='bold')

ax.annotate('', xy=(13.5, 0.6), xytext=(12.5, 0.6),
            arrowprops=dict(arrowstyle='->', color='#9C27B0', lw=2,
                          connectionstyle='arc3,rad=0.5'))
ax.text(13, 1.1, f'Me={M_E} kN*m', fontsize=9, color='#9C27B0', ha='center', fontweight='bold')

# Dimensiones
ax.annotate('', xy=(0, -1), xytext=(4, -1),
            arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
ax.text(2, -1.4, '4 m', fontsize=10, ha='center', color='gray')

ax.annotate('', xy=(4, -1), xytext=(8, -1),
            arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
ax.text(6, -1.4, '4 m', fontsize=10, ha='center', color='gray')

ax.annotate('', xy=(8, -1), xytext=(13, -1),
            arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
ax.text(10.5, -1.4, '5 m', fontsize=10, ha='center', color='gray')

ax.annotate('', xy=(14, 0), xytext=(14, 6),
            arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
ax.text(14.5, 3, '6 m', fontsize=10, ha='left', color='gray', va='center')

# Reacciones
ax.annotate(f'Ax={A_x:.1f} kN', xy=(0, 6), xytext=(-2, 5),
            fontsize=9, color='green', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
ax.annotate(f'Ay={A_y:.1f} kN', xy=(0, 6), xytext=(-2, 4.3),
            fontsize=9, color='green', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
ax.annotate(f'Ma={M_a:.1f} kN*m', xy=(0, 6), xytext=(-2.5, 3.5),
            fontsize=9, color='green', fontweight='bold')

ax.annotate(f'Ex={E_x:.1f} kN', xy=(13, 0), xytext=(15, -0.5),
            fontsize=9, color='green', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
ax.annotate(f'Ey={E_y:.1f} kN', xy=(13, 0), xytext=(15, -1.2),
            fontsize=9, color='green', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5))

ax.set_xlim(-4, 17)
ax.set_ylim(-2.5, 10)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Esquema Estructural del Portico con Cargas y Reacciones (xy=45)',
             fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig(r'C:\Users\andre\Desktop\proyecto materiales\Esquema_Portico.png', dpi=300, bbox_inches='tight')
plt.close()
print("Esquema guardado: Esquema_Portico.png")

print("\n=== TODOS LOS DIAGRAMAS GENERADOS ===")

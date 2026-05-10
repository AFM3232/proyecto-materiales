"""
VERIFICACION FORMAL DE CALCULOS - Portico plano xy=45
=====================================================
Ingeniero estructural: verificacion paso a paso de todas las
reacciones, equilibrios y funciones de esfuerzos internos.

Cada check imprime OK o ERROR con valor esperado vs calculado.
"""

import math
from scipy.integrate import quad
import numpy as np

# ==============================================================
# TOLERANCIA
# ==============================================================
TOL = 0.05  # kN o kN*m

ok_count = 0
err_count = 0

def check(nombre, calculado, esperado, tol=TOL):
    """Verifica un valor y reporta OK/ERROR."""
    global ok_count, err_count
    diff = abs(calculado - esperado)
    if diff <= tol:
        print(f"  [OK]    {nombre}: calc = {calculado:12.4f},  esp = {esperado:12.4f},  diff = {diff:.6f}")
        ok_count += 1
    else:
        print(f"  [ERROR] {nombre}: calc = {calculado:12.4f},  esp = {esperado:12.4f},  diff = {diff:.6f}  <<<")
        err_count += 1

# ==============================================================
# DATOS DEL PROBLEMA
# ==============================================================
xy = 45
Fx_C = 15 * math.cos(math.radians(40))   # 11.4907
Fy_C = 15 * math.sin(math.radians(40))   # 9.6418
M_C  = 5.0     # kN*m CW
M_E  = 90.0    # kN*m CW

# Reacciones esperadas (del problema)
Ax_exp = -26.4907
Ay_exp = 554.8013
Ma_exp = 1799.2041
Ex_exp = 15.0
Ey_exp = 219.8407

print("=" * 72)
print("  VERIFICACION FORMAL - PORTICO PLANO xy=45")
print("=" * 72)

# ==============================================================
# 1. RESULTANTES DE CARGAS DISTRIBUIDAS
# ==============================================================
print("\n" + "=" * 72)
print("  1. RESULTANTES DE CARGAS DISTRIBUIDAS (scipy.integrate.quad)")
print("=" * 72)

def w1(x): return 5.625 * x + 45.0     # [0, 8]
def w2(x): return 234.0 - 18.0 * x     # [8, 13]

R_W1, _ = quad(w1, 0, 8)
R_W2, _ = quad(w2, 8, 13)

print(f"\n  R_W1 = integral(w1, 0, 8):")
check("R_W1", R_W1, 540.0)

print(f"  R_W2 = integral(w2, 8, 13):")
check("R_W2", R_W2, 225.0)

R_total = R_W1 + R_W2
check("R_total", R_total, 765.0)

# Brazos y momentos
mom_w1_A, _ = quad(lambda x: x * w1(x), 0, 8)      # momento de w1 resp A
mom_w2_A, _ = quad(lambda x: x * w2(x), 8, 13)     # momento de w2 resp A

x_bar_W1 = mom_w1_A / R_W1
x_bar_W2 = mom_w2_A / R_W2
print(f"\n  Brazo W1 resp A: {x_bar_W1:.4f} m")
print(f"  Brazo W2 resp A: {x_bar_W2:.4f} m")

# Parciales para cuerpo BD
R_W1_04, _    = quad(w1, 0, 4)
R_W1_48, _    = quad(w1, 4, 8)
mom_W1_04_A, _ = quad(lambda x: x * w1(x), 0, 4)
mom_W1_48_B, _ = quad(lambda x: (x - 4) * w1(x), 4, 8)
mom_W2_813_B, _ = quad(lambda x: (x - 4) * w2(x), 8, 13)

print(f"\n  R_W1 [0,4] = {R_W1_04:.4f} kN")
print(f"  R_W1 [4,8] = {R_W1_48:.4f} kN")
print(f"  Mom W1[0,4] resp A = {mom_W1_04_A:.4f} kN*m")
print(f"  Mom W1[4,8] resp B = {mom_W1_48_B:.4f} kN*m")
print(f"  Mom W2[8,13] resp B = {mom_W2_813_B:.4f} kN*m")

# ==============================================================
# 2. VERIFICACION DE REACCIONES PASO A PASO
# ==============================================================
print("\n" + "=" * 72)
print("  2. VERIFICACION DE REACCIONES")
print("=" * 72)

# ---- COLUMNA DE ----
print("\n  --- Columna DE ---")
print("  SumM_E(col, CCW+): -M_E + Dx*6 = 0  =>  Dx = 15 kN")
Dx_col = M_E / 6.0
check("Dx_col = M_E/6", Dx_col, 15.0)

print("  SumFx(col): Ex - Dx_viga_sobre_col = 0")
print("  La viga empuja la columna a la izq con 15 kN => Ex = 15 kN")
check("Ex", 15.0, Ex_exp)

# ---- CUERPO BD ----
print("\n  --- Cuerpo BD (rotula B en x=4, rotula D en x=13) ---")
print("  SumM_B(BD, CCW+) = 0:")
print("    -mom_W1[4,8]_B - mom_W2_B - Fy_C*4 - M_C + Dy_up*9 = 0")
print(f"    = -{mom_W1_48_B:.2f} - {mom_W2_813_B:.2f} - {Fy_C:.4f}*4 - {M_C:.1f} + 9*Dy_up = 0")

# NOTA: M_C = 5 CW. En CCW+, contribuye -5. Pero las reacciones del problema
# fueron calculadas con M_C = +5 (posiblemente tratado como CCW).
# Verificamos cual interpretacion reproduce las reacciones dadas:
Dy_up_with_plus = (mom_W1_48_B + mom_W2_813_B + Fy_C * 4 + M_C) / 9.0
Dy_up_with_minus = (mom_W1_48_B + mom_W2_813_B + Fy_C * 4 - M_C) / 9.0

print(f"\n    Si M_C contribuye +5 (como CCW): Dy_up = {Dy_up_with_plus:.4f}")
print(f"    Si M_C contribuye -5 (como CW):  Dy_up = {Dy_up_with_minus:.4f}")
print(f"    Valor esperado:                   Dy_up = {Ey_exp:.4f}")

# Las reacciones del problema usan M_C = +5
Dy_up_calc = Dy_up_with_plus
check("Dy_up (= Ey, con M_C=+5)", Dy_up_calc, Ey_exp)

# SumFy(BD)
By_calc = R_W1_48 + R_W2 + Fy_C - Dy_up_calc
print(f"\n  SumFy(BD) => By = {By_calc:.4f}")

# SumFx(BD): Bx + Fx_C + Dx_viga = 0
# La columna empuja la viga en D hacia la DERECHA con 15 kN
Dx_viga = 15.0
Bx_on_BD = -Fx_C - Dx_viga
Bx_on_AB = -Bx_on_BD
print(f"  SumFx(BD) => Bx(sobre BD) = {Bx_on_BD:.4f}")

# ---- CUERPO AB ----
print("\n  --- Cuerpo AB (empotrado A en x=0, rotula B en x=4) ---")

Ax_calc = Bx_on_BD  # = -26.49 (Ax = Bx_on_BD porque SumFx(AB): Ax - Bx_on_AB = 0 => Ax = -Bx_on_AB = Bx_on_BD)
check("Ax (de AB)", Ax_calc, Ax_exp)

Ay_calc = R_W1_04 + By_calc
print(f"\n  SumFy(AB): Ay = {R_W1_04:.4f} + {By_calc:.4f} = {Ay_calc:.4f}")
check("Ay (de AB)", Ay_calc, Ay_exp)

Ma_calc = mom_W1_04_A + By_calc * 4
print(f"\n  SumM_A(AB): Ma = {mom_W1_04_A:.4f} + {By_calc:.4f}*4 = {Ma_calc:.4f}")
check("Ma (de AB)", Ma_calc, Ma_exp)

# ==============================================================
# 3. EQUILIBRIO GLOBAL
# ==============================================================
print("\n" + "=" * 72)
print("  3. EQUILIBRIO GLOBAL")
print("=" * 72)

Ax = Ax_exp; Ay = Ay_exp; Ma = Ma_exp; Ex = Ex_exp; Ey = Ey_exp

# SumFx
SumFx = Ax + Fx_C + Ex
print(f"\n  SumFx = Ax + Fx_C + Ex = {Ax:.4f} + {Fx_C:.4f} + {Ex:.4f} = {SumFx:.6f}")
check("SumFx = 0", SumFx, 0.0)

# SumFy
SumFy = Ay + Ey - R_W1 - R_W2 - Fy_C
print(f"\n  SumFy = Ay + Ey - R_W1 - R_W2 - Fy_C = {SumFy:.6f}")
check("SumFy = 0", SumFy, 0.0, tol=0.01)

# SumM about A(0, 6) — CCW positivo
# Geometria: A en (0,6), E en (13,0). Viga a y=6, columna de D(13,6) a E(13,0).
#
# Ma resiste rotacion CW => Ma es CCW => contribuye +Ma.
# Cargas distribuidas hacia abajo a la derecha de A => CW => negativo.
# Fy_C hacia abajo a x=8 => CW => negativo.
# M_C = 5 CW => -5.
# Ex en E(13,0): r = (13, -6) desde A, F = (Ex, 0).
#   Momento = rx*Fy - ry*Fx = 13*0 - (-6)*Ex = +6*Ex.
# Ey en E(13,0): r = (13, -6), F = (0, Ey).
#   Momento = 13*Ey - (-6)*0 = +13*Ey.
# M_E = 90 CW => -90.

SumM_A = (+Ma
          - mom_w1_A - mom_w2_A
          - Fy_C * 8 - M_C
          + 6 * Ex
          + 13 * Ey
          - M_E)

print(f"\n  SumM_A (sobre A, CCW+):")
print(f"    +Ma (CCW, empotramiento)    = +{Ma:.4f}")
print(f"    -mom_w1_A (CW, carga dist)  = {-mom_w1_A:.4f}")
print(f"    -mom_w2_A (CW, carga dist)  = {-mom_w2_A:.4f}")
print(f"    -Fy_C*8 (CW, puntual)       = {-Fy_C*8:.4f}")
print(f"    -M_C (CW, par ext)           = {-M_C:.4f}")
print(f"    +6*Ex (CCW, react horiz E)   = +{6*Ex:.4f}")
print(f"    +13*Ey (CCW, react vert E)   = +{13*Ey:.4f}")
print(f"    -M_E (CW, par ext E)         = {-M_E:.4f}")
print(f"    -----------------------------------------")
print(f"    SumM_A = {SumM_A:.4f}")
check("SumM_A = 0", SumM_A, 0.0, tol=0.5)

# ==============================================================
# 4. FUNCIONES INTERNAS V(x), N(x), M(x) EN PUNTOS CRITICOS
# ==============================================================
print("\n" + "=" * 72)
print("  4. FUNCIONES INTERNAS EN PUNTOS CRITICOS")
print("=" * 72)

# Funciones derivadas desde equilibrio (corte a distancia x desde A, fuerzas a la izq)
# N(x) = fuerza axial = suma de fuerzas horizontales a la izquierda
# V(x) = cortante = suma de fuerzas verticales a la izquierda (arriba = +)
# M(x) = momento flector = suma de momentos de fuerzas izq. sobre el corte (CCW = +)

# Region 1: [0, 8]
# N1(x) = -Ax = 26.4907  (compresion)
# V1(x) = Ay - integral(w1, 0, x) = Ay - 2.8125*x^2 - 45*x
# M1(x) = -Ma + Ay*x - integral((x-t)*w1(t), 0, x) = -Ma + Ay*x - 0.9375*x^3 - 22.5*x^2

def N1(x): return -Ax

def V1(x): return Ay - 2.8125*x**2 - 45*x

def M1(x): return -Ma + Ay*x - 0.9375*x**3 - 22.5*x**2

# Region 2: [8, 13]
# Fuerzas adicionales en C: Fx_C (der), Fy_C (abajo), M_C (CW)
# N2(x) = -Ax - Fx_C = 15.0
# V2(x) = Ay - R_W1 - Fy_C - integral(w2, 8, x)
#        = Ay - 540 - Fy_C - (234x - 9x^2 - 234*8 + 9*64)
#        = Ay - 540 - Fy_C - 234x + 9x^2 + 1296
#        = 9x^2 - 234x + (Ay - 540 - Fy_C + 1296)
C_V = Ay - R_W1 - Fy_C + 1296

def N2(x): return -Ax - Fx_C

def V2(x): return 9*x**2 - 234*x + C_V

# M2(x) = -Ma + Ay*x - integral((x-t)*w1(t), 0, 8) - Fy_C*(x-8) - M_C - integral((x-t)*w2(t), 8, x)
# integral((x-t)*w1(t), 0, 8) = x*R_W1 - mom_w1_A = 540*x - 2400
# integral((x-t)*w2(t), 8, x) = -3x^3 + 117x^2 - 1296x + 4416
def M2(x):
    int_w1 = 540*x - mom_w1_A
    int_w2 = -3*x**3 + 117*x**2 - 1296*x + 4416
    return -Ma + Ay*x - int_w1 - Fy_C*(x-8) - M_C - int_w2

# Polinomios dados en el problema
def V1_poly(x): return -2.8125*x**2 - 45*x + 554.8013
def V2_poly(x): return 9*x**2 - 234*x + 1301.159
def M1_poly(x): return -0.9375*x**3 - 22.5*x**2 + 554.8013*x - 1799.2041
def M2_poly(x): return 3*x**3 - 117*x**2 + 1301.159*x - 3743.068

# ---- Verificaciones puntuales ----
print("\n  --- 4a. M1(0) = -Ma (empotramiento) ---")
check("M1(0)", M1(0), -Ma_exp, tol=0.1)

print("\n  --- 4b. M1(4) = 0 (rotula B) ---")
check("M1(4) = 0 [rotula B]", M1(4), 0.0, tol=0.5)

print("\n  --- 4c. V1(0) = Ay ---")
check("V1(0)", V1(0), Ay_exp)

print("\n  --- 4d. V1(4) ---")
V1_4_exp = -2.8125*16 - 45*4 + Ay_exp
check("V1(4)", V1(4), V1_4_exp)

print("\n  --- 4e. N1 (region [0,8]) ---")
check("N1", N1(0), 26.4907)

print("\n  --- 4f. N2 (region [8,13]) ---")
check("N2", N2(10), 15.0, tol=0.1)

print("\n  --- 4g. M en C ---")
M1_8 = M1(8)
M2_8 = M2(8)
print(f"    M1(8-) = {M1_8:.4f}")
print(f"    M2(8+) = {M2_8:.4f}")
salto_M = M1_8 - M2_8
print(f"    Salto M = M1(8-) - M2(8+) = {salto_M:.4f}")
check("Salto M en C = M_C", salto_M, M_C, tol=0.5)

print("\n  *** 4h. CHECK CLAVE: M2(13) = 0 (rotula D) ***")
M2_13 = M2(13)
M2_13_poly = M2_poly(13)
print(f"    M2(13) desde equilibrio  = {M2_13:.4f}")
print(f"    M2(13) desde polinomio   = {M2_13_poly:.4f}")
check("M2(13) [rotula D] ***CLAVE***", M2_13, 0.0, tol=0.5)

if abs(M2_13) > 0.5:
    print(f"\n    >>> DIAGNOSTICO: M2(13) = {M2_13:.4f} != 0")
    print(f"    >>> Algebraicamente: M2(13) = -2*M_C = -2*{M_C} = {-2*M_C}")
    print(f"    >>> Esto indica que en la ecuacion SumM_B(BD) se uso M_C = +{M_C} (como CCW)")
    print(f"    >>> cuando M_C = {M_C} kN*m CW deberia contribuir -{M_C} (en convencion CCW+).")
    print(f"    >>> Si se corrige el signo de M_C en SumM_B(BD):")
    Dy_correcto = (mom_W1_48_B + mom_W2_813_B + Fy_C * 4 - M_C) / 9.0
    By_correcto = R_W1_48 + R_W2 + Fy_C - Dy_correcto
    Ay_correcto = R_W1_04 + By_correcto
    Ma_correcto = mom_W1_04_A + By_correcto * 4
    print(f"    >>>   Dy_up (corregido) = {Dy_correcto:.4f} kN")
    print(f"    >>>   Ay (corregido)    = {Ay_correcto:.4f} kN")
    print(f"    >>>   Ma (corregido)    = {Ma_correcto:.4f} kN*m")
    M2_13_corr = -Ma_correcto + Ay_correcto*13 - (540*13 - mom_w1_A) - Fy_C*5 - M_C - (-3*13**3 + 117*13**2 - 1296*13 + 4416)
    print(f"    >>>   M2(13) corregido  = {M2_13_corr:.4f} (debe ser ~0)")

print("\n  --- 4i. V2(13) ---")
V2_13 = V2(13)
V2_13_global = Ay - R_W1 - Fy_C - R_W2  # = -(Ey)
print(f"    V2(13) = {V2_13:.4f}")
print(f"    Ay - R_W1 - Fy_C - R_W2 = {V2_13_global:.4f} (= -Ey)")
check("V2(13)", V2_13, V2_13_global)

# ==============================================================
# 5. CONTINUIDAD DE V EN C (salto = Fy_C)
# ==============================================================
print("\n" + "=" * 72)
print("  5. CONTINUIDAD DE V EN C (salto = Fy_C = {:.4f})".format(Fy_C))
print("=" * 72)

V1_8 = V1(8)
V2_8 = V2(8)
salto_V = V1_8 - V2_8
print(f"\n  V1(8-) = {V1_8:.4f}")
print(f"  V2(8+) = {V2_8:.4f}")
print(f"  Salto V = V1(8-) - V2(8+) = {salto_V:.4f}")
check("Salto V en C = Fy_C", salto_V, Fy_C, tol=0.1)

# ==============================================================
# 6. CONTINUIDAD DE M EN C (salto = M_C = 5)
# ==============================================================
print("\n" + "=" * 72)
print("  6. CONTINUIDAD DE M EN C (salto = M_C = 5)")
print("=" * 72)

print(f"\n  M1(8-) = {M1_8:.4f}")
print(f"  M2(8+) = {M2_8:.4f}")
print(f"  Salto M = {salto_M:.4f}")
check("Salto M en C = 5", salto_M, M_C, tol=0.5)

# ==============================================================
# 7. VERIFICACION dM/dx = V y dV/dx = -w(x)
# ==============================================================
print("\n" + "=" * 72)
print("  7. VERIFICACION RELACIONES DIFERENCIALES")
print("=" * 72)

h = 1e-6

print("\n  --- dM/dx = V, Region 1: [0, 8] ---")
pts1 = [0.5, 1, 2, 3, 4, 5, 6, 7, 7.5]
all_ok_1 = True
for xp in pts1:
    dMdx = (M1(xp + h) - M1(xp - h)) / (2 * h)
    diff = abs(dMdx - V1(xp))
    if diff >= 0.01:
        print(f"  [ERROR] x={xp}: dM/dx = {dMdx:.4f}, V = {V1(xp):.4f}, diff = {diff:.6f}  <<<")
        err_count += 1; all_ok_1 = False
    else:
        ok_count += 1
if all_ok_1:
    print(f"  [OK]    dM/dx = V verificado en {len(pts1)} puntos")

print("\n  --- dM/dx = V, Region 2: [8, 13] ---")
pts2 = [8.5, 9, 10, 11, 12, 12.5]
all_ok_2 = True
for xp in pts2:
    dMdx = (M2(xp + h) - M2(xp - h)) / (2 * h)
    diff = abs(dMdx - V2(xp))
    if diff >= 0.01:
        print(f"  [ERROR] x={xp}: dM/dx = {dMdx:.4f}, V = {V2(xp):.4f}, diff = {diff:.6f}  <<<")
        err_count += 1; all_ok_2 = False
    else:
        ok_count += 1
if all_ok_2:
    print(f"  [OK]    dM/dx = V verificado en {len(pts2)} puntos")

print("\n  --- dV/dx = -w(x), Region 1: [0, 8] ---")
pts_dv1 = [1, 3, 5, 7]
all_ok_dv1 = True
for xp in pts_dv1:
    dVdx = (V1(xp + h) - V1(xp - h)) / (2 * h)
    diff = abs(dVdx - (-w1(xp)))
    if diff >= 0.1:
        print(f"  [ERROR] x={xp}: dV/dx = {dVdx:.4f}, -w = {-w1(xp):.4f}, diff = {diff:.6f}  <<<")
        err_count += 1; all_ok_dv1 = False
    else:
        ok_count += 1
if all_ok_dv1:
    print(f"  [OK]    dV/dx = -w(x) verificado en {len(pts_dv1)} puntos")

print("\n  --- dV/dx = -w(x), Region 2: [8, 13] ---")
pts_dv2 = [9, 10, 11, 12]
all_ok_dv2 = True
for xp in pts_dv2:
    dVdx = (V2(xp + h) - V2(xp - h)) / (2 * h)
    diff = abs(dVdx - (-w2(xp)))
    if diff >= 0.1:
        print(f"  [ERROR] x={xp}: dV/dx = {dVdx:.4f}, -w = {-w2(xp):.4f}, diff = {diff:.6f}  <<<")
        err_count += 1; all_ok_dv2 = False
    else:
        ok_count += 1
if all_ok_dv2:
    print(f"  [OK]    dV/dx = -w(x) verificado en {len(pts_dv2)} puntos")

# ==============================================================
# 8. VERIFICACION COLUMNA DE
# ==============================================================
print("\n" + "=" * 72)
print("  8. VERIFICACION COLUMNA DE")
print("=" * 72)

print("\n  N_col = -Ey (compresion)")
check("N_col", -Ey_exp, -219.8407)

print("\n  V_col = Ex = 15.0 (constante)")
check("V_col", Ex_exp, 15.0)

print("\n  M_col(0) = -M_E = -90 (en E)")
check("M_col(0)", -M_E, -90.0)

print("\n  M_col(6) = -M_E + Ex*6 = 0 (en D, rotula)")
M_col_6 = -M_E + Ex_exp * 6
check("M_col(6) [rotula D]", M_col_6, 0.0)

# ==============================================================
# 9. COMPARACION CON POLINOMIOS DADOS
# ==============================================================
print("\n" + "=" * 72)
print("  9. COMPARACION FUNCIONES DERIVADAS vs POLINOMIOS DADOS")
print("=" * 72)

print(f"\n  C_V calculado = {C_V:.4f}, dado = 1301.159")
check("C_V", C_V, 1301.159, tol=0.01)

print("\n  --- V1 ---")
for xp in [0, 2, 4, 6, 8]:
    d = abs(V1(xp) - V1_poly(xp))
    s = "OK" if d < 0.01 else "ERROR"
    print(f"  [{s:5s}] V1({xp}): {V1(xp):.4f} vs {V1_poly(xp):.4f}, diff={d:.6f}")
    ok_count += 1 if d < 0.01 else 0; err_count += 0 if d < 0.01 else 1

print("\n  --- V2 ---")
for xp in [8, 9, 10, 11, 12, 13]:
    d = abs(V2(xp) - V2_poly(xp))
    s = "OK" if d < 0.01 else "ERROR"
    print(f"  [{s:5s}] V2({xp}): {V2(xp):.4f} vs {V2_poly(xp):.4f}, diff={d:.6f}")
    ok_count += 1 if d < 0.01 else 0; err_count += 0 if d < 0.01 else 1

print("\n  --- M1 ---")
for xp in [0, 2, 4, 6, 8]:
    d = abs(M1(xp) - M1_poly(xp))
    s = "OK" if d < 0.01 else "ERROR"
    print(f"  [{s:5s}] M1({xp}): {M1(xp):.4f} vs {M1_poly(xp):.4f}, diff={d:.6f}")
    ok_count += 1 if d < 0.01 else 0; err_count += 0 if d < 0.01 else 1

print("\n  --- M2 ---")
for xp in [8, 9, 10, 11, 12, 13]:
    d = abs(M2(xp) - M2_poly(xp))
    s = "OK" if d < 0.5 else "ERROR"
    print(f"  [{s:5s}] M2({xp}): {M2(xp):.4f} vs {M2_poly(xp):.4f}, diff={d:.6f}")
    ok_count += 1 if d < 0.5 else 0; err_count += 0 if d < 0.5 else 1

# ==============================================================
# 10. TABLA RESUMEN
# ==============================================================
print("\n" + "=" * 72)
print("  10. TABLA RESUMEN DE VALORES CRITICOS")
print("=" * 72)

print(f"\n  {'Punto':<12} {'x(m)':<7} {'N(kN)':<12} {'V(kN)':<14} {'M(kN*m)':<14}")
print(f"  {'-'*59}")
datos = [
    ("A",      0, N1(0),  V1(0),   M1(0)),
    ("B",      4, N1(4),  V1(4),   M1(4)),
    ("C (8-)", 8, N1(8),  V1(8),   M1(8)),
    ("C (8+)", 8, N2(8),  V2(8),   M2(8)),
    ("x=10",  10, N2(10), V2(10),  M2(10)),
    ("D (13)",13, N2(13), V2(13),  M2(13)),
]
for nm, x, N, V, M in datos:
    print(f"  {nm:<12} {x:<7.1f} {N:<12.4f} {V:<14.4f} {M:<14.4f}")

# ==============================================================
# RESUMEN FINAL
# ==============================================================
print("\n" + "=" * 72)
print("  RESUMEN FINAL")
print("=" * 72)
print(f"\n  Checks OK:    {ok_count}")
print(f"  Checks ERROR: {err_count}")
print(f"  Total:        {ok_count + err_count}")

if err_count == 0:
    print("\n  *** TODOS LOS CALCULOS VERIFICADOS CORRECTAMENTE ***")
else:
    print(f"\n  *** {err_count} ERROR(ES) ENCONTRADO(S) ***")
    if abs(M2_13) > 0.5:
        print(f"\n  HALLAZGO PRINCIPAL:")
        print(f"    M2(13) = {M2_13:.4f} kN*m (deberia ser 0 en rotula D).")
        print(f"    Error = -2*M_C = -2*5 = -10 kN*m.")
        print(f"    Causa: el momento M_C = 5 kN*m CW se sumo como +5 (CCW)")
        print(f"    en la ecuacion de momentos del cuerpo BD respecto a B,")
        print(f"    cuando debio restarse como -5 (CW en convencion CCW+).")
        print(f"    Esto afecta a Ey (y por tanto a Ay y Ma) en ~1.11 kN.")

print("\n" + "=" * 72)

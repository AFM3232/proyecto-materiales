# -*- coding: utf-8 -*-
"""Diagrama de optimizacion del perfil de viga - comparacion con otros perfiles."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ── Datos ──
com = {'name': 'W310x67', 'd': 306, 'bf': 204, 'tf': 14.6, 'tw': 8.5,
       'A': 8530, 'Ix': 14500, 'Sx': 948, 'w_kg': 67, 'FS': 1.55}

cus = {'name': 'I-400x190', 'd': 400, 'bf': 190, 'tf': 9, 'tw': 8,
       'A': 6476, 'Ix': 16790, 'Sx': 839, 'w_kg': 50.8, 'FS': 1.40}

otros = [
    {'name': 'W250x89',  'A': 11400, 'w_kg': 89,  'FS': 1.85},
    {'name': 'W310x86',  'A': 11000, 'w_kg': 86,  'FS': 2.10},
    {'name': 'W360x79',  'A': 10100, 'w_kg': 79,  'FS': 2.30},
    {'name': 'W310x74',  'A': 9480,  'w_kg': 74,  'FS': 1.74},
    {'name': 'W310x67',  'A': 8530,  'w_kg': 67,  'FS': 1.55},
    {'name': 'W250x67',  'A': 8560,  'w_kg': 67,  'FS': 1.60},
]

fig = plt.figure(figsize=(20, 14))

# ═══════════════════════════════════════════════════════════
# PANEL 1: Secciones transversales a escala
# ═══════════════════════════════════════════════════════════
ax1 = fig.add_subplot(2, 2, 1)
ax1.set_title('Secciones Transversales a Escala', fontsize=14, fontweight='bold', pad=15)

def draw_I(ax, cx, cy, d, bf, tf, tw, color, label_lines, scale=0.4):
    ds = d * scale
    bfs = bf * scale
    tfs = tf * scale
    tws = tw * scale
    # Ala superior
    ax.add_patch(patches.Rectangle((cx-bfs/2, cy+ds/2-tfs), bfs, tfs,
                 fc=color, ec='black', lw=1.5, alpha=0.85))
    # Ala inferior
    ax.add_patch(patches.Rectangle((cx-bfs/2, cy-ds/2), bfs, tfs,
                 fc=color, ec='black', lw=1.5, alpha=0.85))
    # Alma
    hws = ds - 2*tfs
    ax.add_patch(patches.Rectangle((cx-tws/2, cy-ds/2+tfs), tws, hws,
                 fc=color, ec='black', lw=1.5, alpha=0.85))
    # Cotas
    ax.annotate('', xy=(cx+bfs/2+5, cy-ds/2), xytext=(cx+bfs/2+5, cy+ds/2),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    ax.text(cx+bfs/2+10, cy, f'd={d}', fontsize=8, va='center', color='gray')
    ax.annotate('', xy=(cx-bfs/2, cy-ds/2-5), xytext=(cx+bfs/2, cy-ds/2-5),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    ax.text(cx, cy-ds/2-12, f'bf={bf}', fontsize=8, ha='center', color='gray')
    # Label
    y_label = cy - ds/2 - 28
    for i, line in enumerate(label_lines):
        ax.text(cx, y_label - i*12, line, ha='center', va='top', fontsize=10,
                fontweight='bold' if i == 0 else 'normal')

draw_I(ax1, 90, 130, com['d'], com['bf'], com['tf'], com['tw'], '#4A90D9',
       [com['name'], f"A = {com['A']} mm\u00B2", f"{com['w_kg']} kg/m", f"FS = {com['FS']}"])
draw_I(ax1, 260, 130, cus['d'], cus['bf'], cus['tf'], cus['tw'], '#2ECC71',
       [cus['name'], f"A = {cus['A']} mm\u00B2", f"{cus['w_kg']:.1f} kg/m", f"FS = {cus['FS']}"])

# Flecha de reduccion
ax1.annotate('', xy=(210, 130), xytext=(160, 130),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=4))
ax1.text(185, 150, f"-{(1-cus['A']/com['A'])*100:.1f}%\nmaterial",
         ha='center', fontsize=14, fontweight='bold', color='#E74C3C')

ax1.set_xlim(0, 360)
ax1.set_ylim(20, 230)
ax1.set_aspect('equal')
ax1.axis('off')

# ═══════════════════════════════════════════════════════════
# PANEL 2: Barras de peso por metro
# ═══════════════════════════════════════════════════════════
ax2 = fig.add_subplot(2, 2, 2)
ax2.set_title('Peso por Metro Lineal de Viga (10 m)', fontsize=14, fontweight='bold', pad=15)

all_profiles = otros + [cus]
all_profiles.sort(key=lambda x: x['w_kg'], reverse=True)

names = [p['name'] for p in all_profiles]
pesos = [p['w_kg'] for p in all_profiles]
colors2 = []
for p in all_profiles:
    if p['name'] == cus['name']:
        colors2.append('#2ECC71')
    elif p['name'] == com['name']:
        colors2.append('#4A90D9')
    else:
        colors2.append('#BDC3C7')

bars = ax2.barh(range(len(names)), pesos, color=colors2, edgecolor='black', lw=0.8, height=0.65)
ax2.set_yticks(range(len(names)))
ax2.set_yticklabels(names, fontsize=11)
ax2.set_xlabel('Peso (kg/m)', fontsize=12)

for i, (bar, peso) in enumerate(zip(bars, pesos)):
    total_10m = peso * 10
    ahorro = (1 - cus['w_kg'] / peso) * 100
    label = f"  {peso} kg/m = {total_10m:.0f} kg en 10m"
    if all_profiles[i]['name'] == cus['name']:
        label += "  \u2190 OPTIMIZADO"
    elif all_profiles[i]['name'] == com['name']:
        label += f"  \u2190 seleccionado (-{ahorro:.0f}% vs custom)"
    else:
        label += f"  (-{ahorro:.0f}% vs custom)"
    ax2.text(peso + 0.5, i, label, va='center', fontsize=9)

ax2.set_xlim(0, 120)
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

# ═══════════════════════════════════════════════════════════
# PANEL 3: FS vs Peso (eficiencia)
# ═══════════════════════════════════════════════════════════
ax3 = fig.add_subplot(2, 2, 3)
ax3.set_title('Eficiencia: Factor de Seguridad vs Peso', fontsize=14, fontweight='bold', pad=15)

# Zona no cumple
ax3.fill_between([40, 100], 0.8, 1.4, color='#FADBD8', alpha=0.5)
ax3.axhline(y=1.4, color='red', linestyle='--', linewidth=2, alpha=0.8)
ax3.text(95, 1.25, 'NO CUMPLE\nFS < 1.4', fontsize=10, color='#E74C3C',
         ha='right', fontstyle='italic', fontweight='bold')

# Zona sobredimensionado
ax3.fill_between([40, 100], 2.0, 2.8, color='#FEF9E7', alpha=0.5)
ax3.text(95, 2.2, 'SOBREDIMENSIONADO', fontsize=10, color='#F39C12',
         ha='right', fontstyle='italic')

# Zona optima
ax3.fill_between([40, 60], 1.4, 1.7, color='#D5F5E3', alpha=0.5)
ax3.text(50, 1.55, 'ZONA\nOPTIMA', fontsize=11, color='#27AE60',
         ha='center', fontweight='bold', alpha=0.7)

for p in otros:
    c = '#4A90D9' if p['name'] == com['name'] else '#95A5A6'
    s = 200 if p['name'] == com['name'] else 100
    mk = 's' if p['name'] == com['name'] else 'o'
    ax3.scatter(p['w_kg'], p['FS'], s=s, c=c, marker=mk, edgecolors='black',
                linewidth=1.5, zorder=4)
    offset = (2, 0.03) if p['name'] != com['name'] else (2, -0.08)
    ax3.annotate(p['name'], (p['w_kg'], p['FS']),
                xytext=(p['w_kg']+offset[0], p['FS']+offset[1]),
                fontsize=8, color='gray')

# Personalizado (estrella grande)
ax3.scatter(cus['w_kg'], cus['FS'], s=400, c='#2ECC71', marker='*',
            edgecolors='black', linewidth=1.5, zorder=5)
ax3.annotate(f"{cus['name']}\n(OPTIMIZADO)", (cus['w_kg'], cus['FS']),
            xytext=(cus['w_kg']-15, cus['FS']+0.25),
            fontsize=11, fontweight='bold', color='#27AE60',
            arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2.5))

ax3.set_xlabel('Peso (kg/m)', fontsize=12)
ax3.set_ylabel('Factor de Seguridad (FS)', fontsize=12)
ax3.set_xlim(40, 100)
ax3.set_ylim(1.0, 2.6)
ax3.grid(True, alpha=0.3)

# ═══════════════════════════════════════════════════════════
# PANEL 4: Tabla resumen
# ═══════════════════════════════════════════════════════════
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_title('Tabla Comparativa de Optimizacion', fontsize=14, fontweight='bold', pad=15)
ax4.axis('off')

tabla = [
    ['Parametro', 'W310x67\n(comercial)', 'I-400x190\n(optimizado)', 'Ahorro'],
    ['Peralte d (mm)', str(com['d']), str(cus['d']), '+31%'],
    ['Ancho ala bf (mm)', str(com['bf']), str(cus['bf']), '-7%'],
    ['Espesor ala tf (mm)', str(com['tf']), str(cus['tf']), '-38%'],
    ['Espesor alma tw (mm)', str(com['tw']), str(cus['tw']), '-6%'],
    [u'Area A (mm\u00B2)', str(com['A']), str(cus['A']), '-24.1%'],
    [u'Inercia Ix (cm\u2074)', str(com['Ix']), str(cus['Ix']), '+15.8%'],
    ['Peso (kg/m)', str(com['w_kg']), f"{cus['w_kg']:.1f}", '-24.2%'],
    ['FS flexion', f"{com['FS']:.2f}", f"{cus['FS']:.2f}", '-'],
    ['Peso total 10m (kg)', str(com['w_kg']*10), f"{cus['w_kg']*10:.0f}", f"-{(com['w_kg']-cus['w_kg'])*10:.0f} kg"],
]

t = ax4.table(cellText=tabla, loc='center', cellLoc='center',
              colWidths=[0.28, 0.22, 0.22, 0.15])
t.auto_set_font_size(False)
t.set_fontsize(9.5)
t.scale(1, 1.9)

# Colores
for j in range(4):
    t[0, j].set_facecolor('#2C3E50')
    t[0, j].set_text_props(color='white', fontweight='bold', fontsize=9)

for i in range(1, len(tabla)):
    t[i, 1].set_facecolor('#D6EAF8')
    t[i, 2].set_facecolor('#D5F5E3')
    val = tabla[i][3]
    if val.startswith('-') and '%' in val:
        t[i, 3].set_facecolor('#FADBD8')
        t[i, 3].set_text_props(fontweight='bold', color='#C0392B')
    elif val.startswith('+'):
        t[i, 3].set_facecolor('#D5F5E3')
        t[i, 3].set_text_props(fontweight='bold', color='#27AE60')
    if 'kg' in val and not '%' in val:
        t[i, 3].set_facecolor('#F9E79F')
        t[i, 3].set_text_props(fontweight='bold', color='#E67E22')

# Texto resumen abajo
ax4.text(0.5, -0.08,
    "ESTRATEGIA: Aumentar peralte (+31%) y reducir espesores al minimo permitido\n"
    f"RESULTADO: 24.1% menos material, FS = 1.40 (justo en el limite)\n"
    f"AHORRO EN VIGA COMPLETA: {(com['w_kg']-cus['w_kg'])*10:.0f} kg de acero A36",
    ha='center', va='top', fontsize=11, fontweight='bold',
    transform=ax4.transAxes,
    bbox=dict(boxstyle='round,pad=0.6', fc='#F9E79F', ec='#F39C12', lw=2))

fig.suptitle('ANALISIS DE OPTIMIZACION DEL PERFIL DE VIGA DEL PORTICO',
             fontsize=18, fontweight='bold', y=0.99, color='#2C3E50')
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig('Optimizacion_Perfil.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Diagrama guardado: Optimizacion_Perfil.png")

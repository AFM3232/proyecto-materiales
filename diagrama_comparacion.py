# -*- coding: utf-8 -*-
"""Diagrama comparativo mejorado: Nuestro diseño vs los 2 proyectos de referencia."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.gridspec import GridSpec

# ═══════════════════════════════════════════════════════════
# DATOS DE LOS 3 PROYECTOS
# ═══════════════════════════════════════════════════════════
MJ_peso = 787*13 + 110*6     # 10,891 kg
LS_peso = 449*13 + 89*6      # 6,371 kg
N_peso  = 67*10 + 58*3.5*2   # 1,076 kg
N_custom = 50.8*10 + 58*3.5*2 # 914 kg

fig = plt.figure(figsize=(24, 28), facecolor='white')
gs = GridSpec(4, 2, figure=fig, hspace=0.32, wspace=0.25,
             left=0.06, right=0.94, top=0.93, bottom=0.03)

# ═══════════════════════════════════════════════════════════
# TITULO PRINCIPAL
# ═══════════════════════════════════════════════════════════
fig.suptitle(u'COMPARACI\u00D3N: Nuestro Proyecto vs Proyectos de Referencia',
             fontsize=22, fontweight='bold', y=0.97, color='#1a1a2e',
             fontfamily='sans-serif')
fig.text(0.5, 0.945,
    u'\u00bfPor qu\u00e9 nuestro dise\u00f1o es superior? \u2014 An\u00e1lisis correcto + perfiles eficientes',
    ha='center', fontsize=13, color='#555', fontstyle='italic')

# ═══════════════════════════════════════════════════════════
# PANEL 1 (top-left): Estructura analizada
# ═══════════════════════════════════════════════════════════
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_title(u'1. Estructura Analizada', fontsize=15, fontweight='bold', pad=14,
              color='#2C3E50', loc='left')
ax1.axis('off')

# --- MJ y LS: viga en L (incorrecto) ---
ax1.text(0.35, 0.97, 'Proyectos MJ y Laura/Santiago:', fontsize=12, ha='center', va='top',
         transform=ax1.transAxes, fontweight='bold', color='#C0392B')
# Dibujar L-shape
ax1.plot([0.08, 0.08, 0.62], [0.55, 0.78, 0.78], color='#E74C3C', linewidth=5,
         transform=ax1.transAxes, solid_capstyle='round')
# Apoyo empotrado
ax1.plot([0.06, 0.10], [0.55, 0.55], color='#E74C3C', linewidth=2, transform=ax1.transAxes)
for xi in np.linspace(0.06, 0.10, 4):
    ax1.plot([xi, xi-0.015], [0.55, 0.52], color='#E74C3C', linewidth=1, transform=ax1.transAxes)
# Nodos
ax1.plot(0.08, 0.55, 'o', color='#E74C3C', markersize=8, transform=ax1.transAxes)
ax1.plot(0.08, 0.78, 'o', color='#E74C3C', markersize=8, transform=ax1.transAxes)
ax1.plot(0.62, 0.78, 'o', color='#E74C3C', markersize=8, transform=ax1.transAxes)

ax1.text(0.35, 0.82, 'Viga (13m)', ha='center', fontsize=10, color='#E74C3C',
         transform=ax1.transAxes, fontweight='bold')
ax1.text(0.02, 0.66, 'Col\n(6m)', ha='center', fontsize=9, color='#E74C3C',
         transform=ax1.transAxes)
# Cargas triangulares
for x in np.linspace(0.12, 0.58, 8):
    h_arr = 0.04 * (x - 0.08) / 0.54
    ax1.annotate('', xy=(x, 0.78), xytext=(x, 0.78 + h_arr + 0.02),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1),
                transform=ax1.transAxes)

ax1.text(0.72, 0.70, u'\u2716 INCORRECTO\nAnalizaron la estructura\nde la p\u00e1g. 17 de la gu\u00eda\n(NO es el p\u00f3rtico)',
         fontsize=10, color='#C0392B', fontweight='bold', transform=ax1.transAxes,
         bbox=dict(fc='#FADBD8', ec='#E74C3C', boxstyle='round,pad=0.4'),
         va='center')

# --- Nuestro: pórtico (correcto) ---
ax1.text(0.35, 0.42, 'Nuestro proyecto (xy = 45):', fontsize=12, ha='center', va='top',
         transform=ax1.transAxes, fontweight='bold', color='#1E8449')
# Portico
ax1.plot([0.12, 0.12, 0.58, 0.58], [0.05, 0.30, 0.30, 0.05], color='#27AE60', linewidth=5,
         transform=ax1.transAxes, solid_capstyle='round')
# Apoyos empotrados
for xb in [0.12, 0.58]:
    ax1.plot([xb-0.02, xb+0.02], [0.05, 0.05], color='#27AE60', linewidth=2, transform=ax1.transAxes)
    for xi in np.linspace(xb-0.02, xb+0.02, 4):
        ax1.plot([xi, xi-0.01], [0.05, 0.025], color='#27AE60', linewidth=1, transform=ax1.transAxes)
# Nodos
for x, y in [(0.12, 0.05), (0.12, 0.30), (0.58, 0.30), (0.58, 0.05)]:
    ax1.plot(x, y, 'o', color='#27AE60', markersize=8, transform=ax1.transAxes)
# Labels
ax1.text(0.02, 0.05, 'A', fontsize=11, color='#27AE60', fontweight='bold', transform=ax1.transAxes)
ax1.text(0.02, 0.30, 'B', fontsize=11, color='#27AE60', fontweight='bold', transform=ax1.transAxes)
ax1.text(0.63, 0.30, 'C', fontsize=11, color='#27AE60', fontweight='bold', transform=ax1.transAxes)
ax1.text(0.63, 0.05, 'D', fontsize=11, color='#27AE60', fontweight='bold', transform=ax1.transAxes)

ax1.text(0.35, 0.34, 'Viga (10m)', ha='center', fontsize=10, color='#27AE60',
         transform=ax1.transAxes, fontweight='bold')
ax1.text(0.05, 0.17, 'Col\n3.5m', ha='center', fontsize=9, color='#27AE60', transform=ax1.transAxes)
ax1.text(0.65, 0.17, 'Col\n3.5m', ha='center', fontsize=9, color='#27AE60', transform=ax1.transAxes)
# Carga distribuida
for x in np.linspace(0.15, 0.55, 10):
    ax1.annotate('', xy=(x, 0.30), xytext=(x, 0.36),
                arrowprops=dict(arrowstyle='->', color='#27AE60', lw=1),
                transform=ax1.transAxes)
ax1.text(0.35, 0.375, 'q = 17.04 kN/m', ha='center', fontsize=8, color='#27AE60',
         transform=ax1.transAxes)
# Carga lateral
ax1.annotate('', xy=(0.12, 0.28), xytext=(0.0, 0.28),
            arrowprops=dict(arrowstyle='->', color='#E67E22', lw=2),
            transform=ax1.transAxes)
ax1.text(0.0, 0.25, 'P=45kN', fontsize=8, color='#E67E22', fontweight='bold', transform=ax1.transAxes)

ax1.text(0.72, 0.18, u'\u2714 CORRECTO\nP\u00f3rtico plano\n(p\u00e1gs. 9-11 de la gu\u00eda)\nBiempotrado',
         fontsize=10, color='#1E8449', fontweight='bold', transform=ax1.transAxes,
         bbox=dict(fc='#D5F5E3', ec='#27AE60', boxstyle='round,pad=0.4'),
         va='center')

# ═══════════════════════════════════════════════════════════
# PANEL 2 (top-right): Área de viga (barras)
# ═══════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_title(u'2. \u00c1rea de Secci\u00f3n de Viga (mm\u00b2)', fontsize=15, fontweight='bold',
              pad=14, color='#2C3E50', loc='left')

names_a = ['MJ\nW1010', 'Laura/Stgo\nW920x420', 'Nuestro\nW310x67', 'Nuestro\nI-400x190\n(custom)']
areas = [100200, 57100, 8530, 6476]
colors_a = ['#E74C3C', '#F39C12', '#27AE60', '#2ECC71']

bars_a = ax2.bar(range(len(names_a)), areas, color=colors_a, edgecolor='#333', linewidth=0.8, width=0.6)
ax2.set_xticks(range(len(names_a)))
ax2.set_xticklabels(names_a, fontsize=10)
ax2.set_ylabel(u'\u00c1rea (mm\u00b2)', fontsize=12)
ax2.grid(axis='y', alpha=0.2, linestyle='--')
ax2.set_ylim(0, 120000)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for bar, area in zip(bars_a, areas):
    ax2.text(bar.get_x() + bar.get_width()/2, area + 2000,
             f'{area:,}', ha='center', fontsize=11, fontweight='bold')

# Flechas de reduccion
ax2.annotate(u'\u221291.5%\nvs MJ', xy=(2, 8530), xytext=(0, 75000),
            fontsize=12, fontweight='bold', color='#27AE60',
            arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2),
            ha='center', va='center',
            bbox=dict(fc='white', ec='#27AE60', boxstyle='round,pad=0.3'))

ax2.annotate(u'\u221293.5%\nvs MJ', xy=(3, 6476), xytext=(1, 55000),
            fontsize=12, fontweight='bold', color='#2ECC71',
            arrowprops=dict(arrowstyle='->', color='#2ECC71', lw=2),
            ha='center', va='center',
            bbox=dict(fc='white', ec='#2ECC71', boxstyle='round,pad=0.3'))

# ═══════════════════════════════════════════════════════════
# PANEL 3 (mid-left): Peso total del pórtico (barras)
# ═══════════════════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_title('3. Peso Total de Acero (kg)', fontsize=15, fontweight='bold',
              pad=14, color='#2C3E50', loc='left')

names_p = ['MJ\n(Henao/Ortega)', 'Laura/Santiago\n(Pe\u00f1a et al.)', 'Nuestro\n(comercial)', 'Nuestro\n(custom)']
pesos = [MJ_peso, LS_peso, N_peso, N_custom]
colors_p = ['#E74C3C', '#F39C12', '#27AE60', '#2ECC71']

bars_p = ax3.bar(range(len(names_p)), pesos, color=colors_p, edgecolor='#333', linewidth=0.8, width=0.6)
ax3.set_xticks(range(len(names_p)))
ax3.set_xticklabels(names_p, fontsize=10)
ax3.set_ylabel('Peso (kg)', fontsize=12)
ax3.grid(axis='y', alpha=0.2, linestyle='--')
ax3.set_ylim(0, 13500)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

for bar, peso in zip(bars_p, pesos):
    ax3.text(bar.get_x() + bar.get_width()/2, peso + 250,
             f'{peso:,.0f} kg', ha='center', fontsize=11, fontweight='bold')

# Porcentajes de reduccion
red_mj = (1 - N_peso / MJ_peso) * 100
red_ls = (1 - N_peso / LS_peso) * 100
ax3.annotate(f'\u221290.1%\nvs MJ', xy=(2, N_peso), xytext=(0.5, 7500),
            fontsize=12, fontweight='bold', color='#27AE60',
            arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2),
            ha='center', va='center',
            bbox=dict(fc='white', ec='#27AE60', boxstyle='round,pad=0.3'))

ax3.annotate(f'\u221283.1%\nvs L/S', xy=(2, N_peso), xytext=(1.5, 5000),
            fontsize=12, fontweight='bold', color='#27AE60',
            arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2),
            ha='center', va='center',
            bbox=dict(fc='white', ec='#27AE60', boxstyle='round,pad=0.3'))

# ═══════════════════════════════════════════════════════════
# PANEL 4 (mid-right): Secciones transversales a escala
# ═══════════════════════════════════════════════════════════
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_title(u'4. Secciones de Viga a Escala (comparaci\u00f3n visual)', fontsize=15,
              fontweight='bold', pad=14, color='#2C3E50', loc='left')
ax4.axis('off')

def draw_I(ax, cx, cy, d, bf, tf, tw, color, label, scale=0.22):
    """Dibuja un perfil I a escala."""
    ds = d * scale
    bfs = bf * scale
    tfs = max(tf * scale, 1.5)
    tws = max(tw * scale, 1.2)
    # Ala superior
    ax.add_patch(patches.Rectangle((cx-bfs/2, cy+ds/2-tfs), bfs, tfs,
                 fc=color, ec='black', lw=1.2, alpha=0.9, zorder=3))
    # Ala inferior
    ax.add_patch(patches.Rectangle((cx-bfs/2, cy-ds/2), bfs, tfs,
                 fc=color, ec='black', lw=1.2, alpha=0.9, zorder=3))
    # Alma
    ax.add_patch(patches.Rectangle((cx-tws/2, cy-ds/2+tfs), tws, ds-2*tfs,
                 fc=color, ec='black', lw=1.2, alpha=0.9, zorder=3))
    # Acotacion altura
    ax.plot([cx+bfs/2+3, cx+bfs/2+3], [cy-ds/2, cy+ds/2], color='#666',
            linewidth=0.8, zorder=2)
    ax.plot([cx+bfs/2+1, cx+bfs/2+5], [cy-ds/2, cy-ds/2], color='#666',
            linewidth=0.8, zorder=2)
    ax.plot([cx+bfs/2+1, cx+bfs/2+5], [cy+ds/2, cy+ds/2], color='#666',
            linewidth=0.8, zorder=2)
    ax.text(cx+bfs/2+7, cy, f'd={d}mm', fontsize=8, va='center', color='#444', rotation=90)
    # Label inferior
    ax.text(cx, cy-ds/2-12, label, ha='center', va='top', fontsize=9,
            fontweight='bold', color=color, linespacing=1.3)

# Posiciones bien separadas
draw_I(ax4, 55, 140, 1011, 437, 73.9, 40.9, '#E74C3C',
       'MJ: W1010\n787 kg/m')
draw_I(ax4, 175, 140, 920, 420, 50, 30, '#F39C12',
       'L/S: W920x420\n449 kg/m')
draw_I(ax4, 290, 140, 306, 204, 14.6, 8.5, '#27AE60',
       'Nuestro: W310x67\n67 kg/m')
draw_I(ax4, 375, 140, 400, 190, 9, 8, '#2ECC71',
       'Custom: I-400x190\n50.8 kg/m')

# Linea base comun
ax4.plot([-5, 430], [28, 28], color='#999', linewidth=0.5, linestyle='--', zorder=1)
ax4.text(215, 18, u'(mismo eje inferior \u2014 a escala relativa)', ha='center',
         fontsize=9, color='#888', fontstyle='italic')

ax4.set_xlim(-15, 440)
ax4.set_ylim(5, 280)
ax4.set_aspect('equal')

# ═══════════════════════════════════════════════════════════
# PANEL 5 (bottom, full width): Tabla comparativa completa
# ═══════════════════════════════════════════════════════════
ax5 = fig.add_subplot(gs[2, :])
ax5.set_title(u'5. Tabla Comparativa Detallada', fontsize=15, fontweight='bold',
              pad=14, color='#2C3E50', loc='left')
ax5.axis('off')

tabla = [
    ['Criterio', 'MJ (Henao / Ortega)', u'Laura/Santiago (Pe\u00f1a et al.)', 'NUESTRO (xy = 45)'],
    ['Estructura\nanalizada',
     u'Viga en L + 1 columna\n(p\u00e1g. 17 gu\u00eda)\n\u2716 INCORRECTO',
     u'Viga en L + 1 columna\n(p\u00e1g. 17 gu\u00eda)\n\u2716 INCORRECTO',
     u'P\u00f3rtico plano biempotrado\n(2 col + 1 viga)\n\u2714 CORRECTO'],
    ['Ecuaciones\nusadas',
     u'Equilibrio est\u00e1tico\n(cuerpos libres)',
     u'Equilibrio est\u00e1tico\n(cuerpos libres)',
     u'Ecuaciones del p\u00f3rtico\n(k, p\u00e1gs. 10-11 gu\u00eda)'],
    ['Perfil de viga', 'W1010 (787 kg/m)', 'W920x420 (449 kg/m)', 'W310x67 (67 kg/m)'],
    [u'\u00c1rea de viga', u'100,200 mm\u00b2', u'57,100 mm\u00b2', u'8,530 mm\u00b2  (\u221291.5%)'],
    ['Perfil de columna', 'W258 (110 kg/m)', 'W250x250 (89 kg/m)', 'W250x58 (58 kg/m)'],
    ['Factor de\nseguridad (FS)', '1.8', '1.4', '1.55 (viga) / 1.51 (col)'],
    ['Peso total\nde acero', '10,891 kg', '6,371 kg', u'1,076 kg  (\u221290.1%)'],
    ['Perfil\npersonalizado',
     u'803 kg/m\n(A = 95,405 mm\u00b2)',
     'No incluido',
     u'50.8 kg/m\n(A = 6,476 mm\u00b2)\n\u221224% vs comercial'],
    ['Cargas\naplicadas',
     u'W\u2081, W\u2082 triangulares\n15 kN, 5 kN\u00b7m, 90 kN\u00b7m\n(de p\u00e1g. 17)',
     u'W\u2081, W\u2082 triangulares\n15 kN, 5 kN\u00b7m, 90 kN\u00b7m\n(de p\u00e1g. 17)',
     'q = 17.04 kN/m (losa)\nP = 45 kN (lateral)\n(de p\u00e1gs. 6-7)'],
]

t = ax5.table(cellText=tabla, loc='center', cellLoc='center',
              colWidths=[0.13, 0.26, 0.26, 0.26])
t.auto_set_font_size(False)
t.set_fontsize(9.5)
t.scale(1, 2.5)

# Estilo encabezado
for j in range(4):
    t[0, j].set_facecolor('#1a1a2e')
    t[0, j].set_text_props(color='white', fontweight='bold', fontsize=10.5)

# Estilo filas
for i in range(1, len(tabla)):
    t[i, 0].set_facecolor('#EAECEE')
    t[i, 0].set_text_props(fontweight='bold', fontsize=9.5)
    t[i, 1].set_facecolor('#FADBD8')   # MJ rojo claro
    t[i, 2].set_facecolor('#FEF9E7')   # LS amarillo claro
    t[i, 3].set_facecolor('#D5F5E3')   # Nuestro verde claro

# Resaltar fila de estructura (la mas critica)
for j in range(4):
    t[1, j].set_text_props(fontweight='bold', fontsize=10)
    if j == 0:
        t[1, j].set_facecolor('#D6DBDF')

# Bordes
for key, cell in t.get_celld().items():
    cell.set_edgecolor('#BDC3C7')
    cell.set_linewidth(0.8)

# ═══════════════════════════════════════════════════════════
# PANEL 6 (bottom): Resumen de ventajas
# ═══════════════════════════════════════════════════════════
ax6 = fig.add_subplot(gs[3, :])
ax6.set_title(u'6. Resumen: \u00bfPor qu\u00e9 nuestro dise\u00f1o es mejor?', fontsize=15,
              fontweight='bold', pad=14, color='#2C3E50', loc='left')
ax6.axis('off')

# Tres columnas de ventajas
ventajas = [
    {
        'icon': u'\u2714',
        'title': u'ESTRUCTURA CORRECTA',
        'desc': u'Analizamos el p\u00f3rtico plano\nbiempotrado (p\u00e1gs. 9-11)\ncon las ecuaciones del\npar\u00e1metro k de rigidez.',
        'color': '#27AE60',
        'x': 0.17,
    },
    {
        'icon': u'\u2193',
        'title': u'90% MENOS ACERO',
        'desc': u'Peso total: 1,076 kg\nvs 10,891 kg (MJ)\nvs 6,371 kg (Laura/Stgo)\nPerfiles eficientes W310/W250.',
        'color': '#2980B9',
        'x': 0.50,
    },
    {
        'icon': u'\u2605',
        'title': u'PERFIL OPTIMIZADO',
        'desc': u'Perfil custom I-400x190:\n50.8 kg/m vs 67 kg/m\n(24% m\u00e1s liviano)\nA = 6,476 mm\u00b2 vs 8,530.',
        'color': '#8E44AD',
        'x': 0.83,
    },
]

for v in ventajas:
    # Circulo con icono
    ax6.text(v['x'], 0.75, v['icon'], fontsize=40, ha='center', va='center',
             color='white', fontweight='bold', transform=ax6.transAxes, zorder=5,
             bbox=dict(boxstyle='circle,pad=0.3', fc=v['color'], ec=v['color'], lw=2))
    # Titulo
    ax6.text(v['x'], 0.48, v['title'], fontsize=13, ha='center', va='center',
             color=v['color'], fontweight='bold', transform=ax6.transAxes)
    # Descripcion
    ax6.text(v['x'], 0.20, v['desc'], fontsize=10.5, ha='center', va='center',
             color='#333', transform=ax6.transAxes, linespacing=1.4,
             bbox=dict(fc='#F8F9FA', ec='#DEE2E6', boxstyle='round,pad=0.5'))

# Nota al pie
fig.text(0.5, 0.008,
    u'NOTA: Los proyectos MJ y Laura/Santiago analizaron la estructura de la p\u00e1gina 17 (viga con cargas triangulares), '
    u'que NO es el p\u00f3rtico plano solicitado.\n'
    u'Nuestro proyecto analiza correctamente el p\u00f3rtico plano biempotrado de las p\u00e1ginas 9-11 de la gu\u00eda del proyecto.',
    ha='center', fontsize=10, fontstyle='italic', color='#555',
    bbox=dict(boxstyle='round,pad=0.5', fc='#FEF9E7', ec='#F39C12', lw=1.5))

out_path = r'C:\Users\andre\Desktop\proyecto materiales\Comparacion_Proyectos.png'
fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Diagrama guardado: {out_path}")

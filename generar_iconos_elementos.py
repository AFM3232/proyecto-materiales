# -*- coding: utf-8 -*-
"""Genera mini-diagramas del portico resaltando cada elemento que se calcula."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

BASE = r"C:\Users\andre\Desktop\proyecto materiales"
OUT = os.path.join(BASE, "iconos_elementos")
os.makedirs(OUT, exist_ok=True)

L = 10.0
h = 3.5

def base_portico(ax, highlight=None):
    """Dibuja el portico base en gris claro, luego resalta el elemento indicado."""
    # Todo en gris claro primero
    gray = '#D5D8DC'
    ax.plot([0, 0], [0, h], color=gray, linewidth=5, solid_capstyle='round')  # col izq
    ax.plot([L, L], [0, h], color=gray, linewidth=5, solid_capstyle='round')  # col der
    ax.plot([0, L], [h, h], color=gray, linewidth=5, solid_capstyle='round')  # viga

    # Apoyos
    for xb in [0, L]:
        ax.plot([xb-0.5, xb+0.5], [0, 0], color=gray, linewidth=2.5)
        for xi in np.linspace(xb-0.5, xb+0.5, 5):
            ax.plot([xi, xi-0.2], [0, -0.25], color=gray, linewidth=1)

    # Nodos
    for x, y, name in [(0,0,'A'), (0,h,'B'), (L,h,'C'), (L,0,'D')]:
        ax.plot(x, y, 'o', color=gray, markersize=8)
        offset_x = -0.6 if x == 0 else 0.6
        offset_y = -0.4 if y == 0 else 0.4
        ax.text(x + offset_x, y + offset_y, name, fontsize=11,
                ha='center', va='center', color='#AAA', fontweight='bold')

def highlight_element(ax, element, color='#E74C3C'):
    """Resalta un elemento especifico del portico."""
    lw = 10
    if element == 'viga_BC':
        ax.plot([0, L], [h, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        ax.plot(0, h, 'o', color=color, markersize=12, zorder=6)
        ax.plot(L, h, 'o', color=color, markersize=12, zorder=6)
        ax.text(0, h+0.35, 'B', fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
        ax.text(L, h+0.35, 'C', fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
    elif element == 'col_AB':
        ax.plot([0, 0], [0, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        ax.plot(0, 0, 'o', color=color, markersize=12, zorder=6)
        ax.plot(0, h, 'o', color=color, markersize=12, zorder=6)
        ax.text(-0.7, 0, 'A', fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
        ax.text(-0.7, h, 'B', fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
    elif element == 'col_DC':
        ax.plot([L, L], [0, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        ax.plot(L, 0, 'o', color=color, markersize=12, zorder=6)
        ax.plot(L, h, 'o', color=color, markersize=12, zorder=6)
        ax.text(L+0.7, 0, 'D', fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
        ax.text(L+0.7, h, 'C', fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
    elif element == 'columnas':
        ax.plot([0, 0], [0, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        ax.plot([L, L], [0, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        for x, y, n in [(0,0,'A'),(0,h,'B'),(L,0,'D'),(L,h,'C')]:
            ax.plot(x, y, 'o', color=color, markersize=12, zorder=6)
            ox = -0.7 if x == 0 else 0.7
            oy = -0.35 if y == 0 else 0.35
            ax.text(x+ox, y+oy, n, fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
    elif element == 'nudo_B':
        ax.plot(0, h, 'o', color=color, markersize=25, zorder=6)
        ax.text(0, h, 'B', fontsize=14, ha='center', va='center', color='white', fontweight='bold', zorder=7)
        # Mini flechas
        ax.annotate('', xy=(0, h), xytext=(-1.5, h),
                    arrowprops=dict(arrowstyle='->', color=color, lw=3), zorder=5)
        ax.text(-1.8, h+0.2, 'P', fontsize=12, color=color, fontweight='bold')
    elif element == 'nudos_BC':
        for x, y, n in [(0,h,'B'), (L,h,'C')]:
            ax.plot(x, y, 'o', color=color, markersize=25, zorder=6)
            ax.text(x, y, n, fontsize=14, ha='center', va='center', color='white', fontweight='bold', zorder=7)
        # Linea punteada entre nudos
        ax.plot([0, L], [h, h], color=color, linewidth=3, linestyle='--', alpha=0.5, zorder=4)
    elif element == 'bases_AD':
        for x, n in [(0,'A'), (L,'D')]:
            ax.plot(x, 0, 's', color=color, markersize=20, zorder=6)
            ax.text(x, 0, n, fontsize=13, ha='center', va='center', color='white', fontweight='bold', zorder=7)
            # Base hatching resaltado
            ax.plot([x-0.5, x+0.5], [0, 0], color=color, linewidth=3, zorder=5)
    elif element == 'todo':
        ax.plot([0, 0], [0, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        ax.plot([L, L], [0, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        ax.plot([0, L], [h, h], color=color, linewidth=lw, solid_capstyle='round', zorder=5)
        for x, y, n in [(0,0,'A'),(0,h,'B'),(L,h,'C'),(L,0,'D')]:
            ax.plot(x, y, 'o', color=color, markersize=12, zorder=6)
            ox = -0.7 if x == 0 else 0.7
            oy = -0.35 if y == 0 else 0.35
            ax.text(x+ox, y+oy, n, fontsize=13, ha='center', color=color, fontweight='bold', zorder=7)
    elif element == 'seccion_viga':
        # Seccion transversal de la viga en el nudo B
        ax.plot(0, h, 'o', color=color, markersize=20, zorder=6)
        ax.text(0, h, 'B', fontsize=12, ha='center', va='center', color='white', fontweight='bold', zorder=7)
        # Dibujar mini seccion I
        cx, cy = 5, h/2
        sc = 0.08
        d, bf, tf, tw = 306, 204, 14.6, 8.5
        ds, bfs, tfs, tws = d*sc, bf*sc, tf*sc*3, tw*sc*3
        ax.add_patch(patches.Rectangle((cx-bfs/2, cy+ds/2-tfs), bfs, tfs, fc=color, ec='black', lw=1, zorder=5))
        ax.add_patch(patches.Rectangle((cx-bfs/2, cy-ds/2), bfs, tfs, fc=color, ec='black', lw=1, zorder=5))
        ax.add_patch(patches.Rectangle((cx-tws/2, cy-ds/2+tfs), tws, ds-2*tfs, fc=color, ec='black', lw=1, zorder=5))
        ax.text(cx, cy-ds/2-0.4, 'W310x67', fontsize=10, ha='center', color=color, fontweight='bold')
        # Puntos de analisis
        for yp, label in [(cy+ds/2, '1'), (cy-ds/2, '2'), (cy, '3'), (cy+ds/2-tfs, '4')]:
            ax.plot(cx+bfs/2+0.3, yp, 'o', color='#F39C12', markersize=8, zorder=6)
            ax.text(cx+bfs/2+0.7, yp, label, fontsize=10, color='#F39C12', fontweight='bold', va='center')

# ═══════════════════════════════════════════════════════════
# Generar cada icono
# ═══════════════════════════════════════════════════════════

configs = [
    ('caso1_viga.png', 'viga_BC', '#2980B9',
     'CASO 1: Carga distribuida sobre la VIGA (B-C)'),
    ('caso2_lateral.png', 'nudo_B', '#E74C3C',
     'CASO 2: Carga lateral en el NUDO B'),
    ('superposicion.png', 'todo', '#8E44AD',
     'SUPERPOSICION: Todo el portico (A-B-C-D)'),
    ('fuerzas_viga.png', 'viga_BC', '#2980B9',
     'Fuerzas internas: VIGA (B-C)'),
    ('fuerzas_columnas.png', 'columnas', '#E74C3C',
     'Fuerzas internas: COLUMNAS (A-B y D-C)'),
    ('diseno_viga.png', 'viga_BC', '#27AE60',
     'Diseno: VIGA (B-C) - W310x67'),
    ('diseno_columna.png', 'columnas', '#27AE60',
     'Diseno: COLUMNAS (A-B y D-C) - W250x58'),
    ('perfil_custom.png', 'viga_BC', '#F39C12',
     'Perfil personalizado: VIGA (B-C)'),
    ('conexion_BC.png', 'nudos_BC', '#8E44AD',
     'Conexion: Nudos B y C (viga-columna)'),
    ('conexion_base.png', 'bases_AD', '#D35400',
     'Conexion: Bases A y D (columna-piso)'),
    ('mohr_seccion.png', 'seccion_viga', '#C0392B',
     'Esfuerzos: Seccion critica en nudo B'),
]

for fname, elem, color, title in configs:
    fig, ax = plt.subplots(figsize=(6, 3.2))
    base_portico(ax)
    highlight_element(ax, elem, color)
    ax.set_title(title, fontsize=12, fontweight='bold', color=color, pad=10)
    ax.set_xlim(-2.5, L+2.5)
    ax.set_ylim(-0.8, h+1)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=120, bbox_inches='tight',
                facecolor='white', transparent=False)
    plt.close()
    print(f"  -> {fname}")

print(f"\n{len(configs)} iconos generados en: {OUT}")

# -*- coding: utf-8 -*-
"""Diagrama 3D del sistema tridimensional y extraccion del portico plano."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

fig = plt.figure(figsize=(22, 12))

# ═══════════════════════════════════════════════════════════
# PANEL 1: Vista 3D del sistema tridimensional
# ═══════════════════════════════════════════════════════════
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.set_title('Sistema Tridimensional\n(4 columnas + 4 vigas + losa)', fontsize=14, fontweight='bold', pad=20)

Lx = 10.0  # luz larga
Ly = 4.0   # luz corta
h = 3.5    # altura columnas

# Columnas (4 esquinas)
cols = [(0,0), (Lx,0), (Lx,Ly), (0,Ly)]
for (x, y) in cols:
    ax1.plot([x, x], [y, y], [0, h], 'k-', linewidth=4, zorder=5)
    # Base (empotramiento)
    ax1.scatter([x], [y], [0], c='black', s=100, marker='s', zorder=6)

# Vigas (4 perimetrales)
vigas = [
    ((0,0,h), (Lx,0,h)),      # viga frontal (10m)
    ((Lx,0,h), (Lx,Ly,h)),    # viga derecha (4m)
    ((Lx,Ly,h), (0,Ly,h)),    # viga trasera (10m)
    ((0,Ly,h), (0,0,h)),      # viga izquierda (4m)
]
for (p1, p2) in vigas:
    ax1.plot([p1[0],p2[0]], [p1[1],p2[1]], [p1[2],p2[2]], 'b-', linewidth=4, zorder=5)

# Losa (plano semitransparente)
verts = [[(0,0,h), (Lx,0,h), (Lx,Ly,h), (0,Ly,h)]]
losa = Poly3DCollection(verts, alpha=0.15, facecolor='#3498DB', edgecolor='#2980B9', linewidth=1)
ax1.add_collection3d(losa)

# Portico a disenar resaltado (frontal, en rojo)
ax1.plot([0, 0], [0, 0], [0, h], 'r-', linewidth=6, zorder=7)
ax1.plot([Lx, Lx], [0, 0], [0, h], 'r-', linewidth=6, zorder=7)
ax1.plot([0, Lx], [0, 0], [h, h], 'r-', linewidth=6, zorder=7)

# Flechas P (lateral)
ax1.quiver(-1.5, 0, h, 1.2, 0, 0, color='red', arrow_length_ratio=0.3, linewidth=3, zorder=8)
ax1.text(-2, 0, h+0.2, 'P = 45 kN', fontsize=12, color='red', fontweight='bold')

# Flechas carga distribuida sobre losa
for xi in np.linspace(1, 9, 6):
    for yi in np.linspace(0.5, 3.5, 3):
        ax1.quiver(xi, yi, h+1, 0, 0, -0.7, color='blue', alpha=0.4, arrow_length_ratio=0.4, linewidth=1)
ax1.text(5, 2, h+1.5, 'q (losa)', fontsize=11, color='blue', ha='center', fontweight='bold')

# Etiquetas de nodos
ax1.text(0, 0, -0.4, 'A', fontsize=14, fontweight='bold', color='red', ha='center')
ax1.text(0, 0, h+0.3, 'B', fontsize=14, fontweight='bold', color='red', ha='center')
ax1.text(Lx, 0, h+0.3, 'C', fontsize=14, fontweight='bold', color='red', ha='center')
ax1.text(Lx, 0, -0.4, 'D', fontsize=14, fontweight='bold', color='red', ha='center')
ax1.text(0, Ly, -0.4, "A'", fontsize=12, color='gray', ha='center')
ax1.text(Lx, Ly, -0.4, "D'", fontsize=12, color='gray', ha='center')

# Cotas
ax1.text(5, -1.2, 0, '10 m', fontsize=12, color='#555', ha='center', fontweight='bold')
ax1.text(Lx+0.8, 2, 0, '4 m', fontsize=12, color='#555', ha='center', fontweight='bold', rotation=90)
ax1.text(-1.2, -0.5, h/2, '3.5 m', fontsize=12, color='#555', ha='center', fontweight='bold')

# Leyenda
ax1.text(5, Ly+1.5, h+1, 'ROJO = Portico plano a disenar', fontsize=11,
         color='red', ha='center', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', fc='#FADBD8', ec='red', alpha=0.8))

ax1.set_xlabel('X (m)')
ax1.set_ylabel('Y (m)')
ax1.set_zlabel('Z (m)')
ax1.set_xlim(-3, 13)
ax1.set_ylim(-2, 7)
ax1.set_zlim(-1, 6)
ax1.view_init(elev=25, azim=-55)
ax1.grid(True, alpha=0.2)

# ═══════════════════════════════════════════════════════════
# PANEL 2: Portico plano extraido (2D) con identificacion
# ═══════════════════════════════════════════════════════════
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_title('Portico Plano Extraido (2D)\nIdentificacion de Elementos', fontsize=14, fontweight='bold', pad=15)

# Columna izquierda A-B
ax2.plot([0, 0], [0, h], color='#E74C3C', linewidth=8, solid_capstyle='round', zorder=3)
ax2.text(-0.8, h/2, 'COLUMNA\nIZQUIERDA\n(A-B)\nW250x58', fontsize=10, ha='center', va='center',
         fontweight='bold', color='#C0392B', rotation=90,
         bbox=dict(boxstyle='round,pad=0.4', fc='#FADBD8', ec='#E74C3C', lw=1.5))

# Columna derecha D-C
ax2.plot([10, 10], [0, h], color='#E74C3C', linewidth=8, solid_capstyle='round', zorder=3)
ax2.text(10.8, h/2, 'COLUMNA\nDERECHA\n(D-C)\nW250x58', fontsize=10, ha='center', va='center',
         fontweight='bold', color='#C0392B', rotation=90,
         bbox=dict(boxstyle='round,pad=0.4', fc='#FADBD8', ec='#E74C3C', lw=1.5))

# Viga B-C
ax2.plot([0, 10], [h, h], color='#2980B9', linewidth=8, solid_capstyle='round', zorder=3)
ax2.text(5, h+0.55, 'VIGA (B-C) - W310x67', fontsize=12, ha='center', va='bottom',
         fontweight='bold', color='#2471A3',
         bbox=dict(boxstyle='round,pad=0.4', fc='#D6EAF8', ec='#2980B9', lw=1.5))

# Nodos
for x, y, name, desc in [(0,0,'A','Empotramiento'), (0,h,'B','Nudo rígido'),
                           (10,h,'C','Nudo rígido'), (10,0,'D','Empotramiento')]:
    ax2.plot(x, y, 'ko', markersize=14, zorder=5)
    ax2.plot(x, y, 'wo', markersize=8, zorder=6)
    ax2.text(x, y, name, fontsize=11, ha='center', va='center', fontweight='bold', zorder=7)

# Descripciones de nodos
ax2.annotate('NUDO B\n(Viga-Columna)\nConexion a momento', xy=(0, h), xytext=(-2.5, h+1.2),
            fontsize=9, ha='center', color='#8E44AD', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#8E44AD', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', fc='#F5EEF8', ec='#8E44AD'))
ax2.annotate('NUDO C\n(Viga-Columna)\nConexion a momento', xy=(10, h), xytext=(12.5, h+1.2),
            fontsize=9, ha='center', color='#8E44AD', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#8E44AD', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', fc='#F5EEF8', ec='#8E44AD'))
ax2.annotate('BASE A\n(Empotramiento)\nConexion al piso', xy=(0, 0), xytext=(-2.5, -0.8),
            fontsize=9, ha='center', color='#D35400', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#D35400', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', fc='#FDEBD0', ec='#D35400'))
ax2.annotate('BASE D\n(Empotramiento)\nConexion al piso', xy=(10, 0), xytext=(12.5, -0.8),
            fontsize=9, ha='center', color='#D35400', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#D35400', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', fc='#FDEBD0', ec='#D35400'))

# Apoyos empotrados
for xb in [0, 10]:
    ax2.plot([xb-0.4, xb+0.4], [0, 0], 'k-', linewidth=3, zorder=4)
    for xi in np.linspace(xb-0.4, xb+0.4, 6):
        ax2.plot([xi, xi-0.15], [0, -0.2], 'k-', linewidth=1.5)

# Carga distribuida
for xi in np.linspace(0.3, 9.7, 18):
    ax2.annotate('', xy=(xi, h), xytext=(xi, h+1.2),
                arrowprops=dict(arrowstyle='->', color='#3498DB', lw=1))
ax2.plot([0, 10], [h+1.2, h+1.2], color='#3498DB', linewidth=1.5)
ax2.text(5, h+1.5, 'q = 17.70 kN/m (carga de losa)', fontsize=11, ha='center',
         color='#2980B9', fontweight='bold')

# Carga lateral
ax2.annotate('', xy=(0, h), xytext=(-2, h),
            arrowprops=dict(arrowstyle='->', color='red', lw=3.5))
ax2.text(-2.2, h+0.15, 'P = 45 kN\n(lateral)', fontsize=11, color='red', fontweight='bold', ha='right')

# Cotas
ax2.annotate('', xy=(0, -1.5), xytext=(10, -1.5),
            arrowprops=dict(arrowstyle='<->', color='#555', lw=1.5))
ax2.text(5, -1.8, 'L = 10.0 m', fontsize=12, ha='center', color='#555', fontweight='bold')
ax2.annotate('', xy=(11.5, 0), xytext=(11.5, h),
            arrowprops=dict(arrowstyle='<->', color='#555', lw=1.5))
ax2.text(12, h/2, 'h = 3.5 m', fontsize=12, ha='left', va='center', color='#555', fontweight='bold')

# Leyenda de colores
legend_y = -2.8
ax2.plot([1, 1.8], [legend_y, legend_y], color='#E74C3C', linewidth=6)
ax2.text(2, legend_y, 'Columnas (W250x58)', fontsize=10, va='center')
ax2.plot([6, 6.8], [legend_y, legend_y], color='#2980B9', linewidth=6)
ax2.text(7, legend_y, 'Viga (W310x67)', fontsize=10, va='center')

ax2.set_xlim(-4, 15)
ax2.set_ylim(-3.5, h+2.5)
ax2.set_aspect('equal')
ax2.axis('off')

fig.suptitle('IDENTIFICACION DEL PORTICO PLANO DENTRO DEL SISTEMA TRIDIMENSIONAL',
             fontsize=16, fontweight='bold', y=0.98, color='#2C3E50')
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig('Portico_3D_y_2D.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Diagrama guardado: Portico_3D_y_2D.png")

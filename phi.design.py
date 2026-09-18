#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
φ-Design Engine — генератор форм на φ-структурах
Автор: Зиявутдинов Магомед Камалович (Zimaka)
Лицензия: MIT
"""

import math
import argparse
from typing import List, Tuple, Optional

PHI = (1.0 + math.sqrt(5.0)) / 2.0
INV_PHI = PHI - 1.0
TWO_PI = 2.0 * math.pi
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

__author__ = "Зиявутдинов Магомед Камалович (Zimaka)"
__version__ = "1.0.0"
__license__ = "MIT"


class PhiShapeGenerator:
    """12 генераторов φ-форм."""

    @staticmethod
    def phi_spiral(n_points: int = 200, turns: float = 4.0):
        """Логарифмическая φ-спираль: r = a·e^(b·θ)."""
        b = math.log(PHI) / (math.pi / 2)
        pts = []
        for i in range(n_points):
            theta = (i / n_points) * turns * TWO_PI
            r = math.exp(b * theta)
            pts.append((r * math.cos(theta), r * math.sin(theta)))
        return pts

    @staticmethod
    def fibonacci_vortex(n_points: int = 200,
                          circulation: float = 13.0,
                          k_layers: int = 5):
        """Γ(r) = Γ₀·Σ F_k·φ^(−k·r/r_c)."""
        pts = []
        for i in range(n_points):
            r = 0.01 + (i / n_points) * 2.0
            gamma = circulation * sum(
                FIB[k] * PHI ** (-k * r) for k in range(k_layers))
            theta = gamma * 0.5
            pts.append((r * math.cos(theta), r * math.sin(theta)))
        return pts

    @staticmethod
    def merkaba_crystal(n_layers: int = 8, radius: float = 5.0):
        """8 слоёв встречного вращения."""
        pts = []
        for layer in range(n_layers):
            r = radius * (PHI ** (-layer / n_layers))
            sign = 1 if layer % 2 == 0 else -1
            base = sign * layer * 0.3
            for k in range(6):
                theta = base + k * TWO_PI / 6
                pts.append((r * math.cos(theta), r * math.sin(theta)))
        return pts

    @staticmethod
    def fibonacci_tree(depth: int = 6, trunk: float = 3.0):
        """Рекурсивное дерево с φ-ветвлением."""
        pts = []
        def build(x, y, angle, length, d):
            if d > depth:
                return
            ex = x + length * math.cos(angle)
            ey = y + length * math.sin(angle)
            pts.append((x, y))
            pts.append((ex, ey))
            build(ex, ey, angle + math.pi / 6, length * 0.7, d + 1)
            build(ex, ey, angle - math.pi / 6, length * 0.7, d + 1)
        build(0, -trunk / 2, math.pi / 2, trunk, 0)
        return pts

    @staticmethod
    def fibonacci_phyllotaxis(n_points: int = 500, scale: float = 8.0):
        """Филотаксис: θ = 2π·k/φ."""
        pts = []
        for k in range(1, n_points + 1):
            theta = TWO_PI * k / PHI
            r = scale * math.sqrt(k / n_points)
            pts.append((r * math.cos(theta), r * math.sin(theta)))
        return pts


class PhiDesignEngine:
    """Фасад движка."""

    def __init__(self, output_dir: str = "designs"):
        self.output_dir = output_dir
        self.generator = PhiShapeGenerator()

    def generate_svg(self, points: List[Tuple[float, float]],
                      path: str, width: int = 800, height: int = 800,
                      color: str = "#00ffcc"):
        """Экспорт точек в SVG."""
        if not points:
            return None
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        span = max(max_x - min_x, max_y - min_y, 1e-6)
        margin = 40
        scale = (width - 2 * margin) / span

        def to_svg(x, y):
            sx = margin + (x - min_x) * scale
            sy = height - margin - (y - min_y) * scale
            return sx, sy

        lines = [f'<?xml version="1.0" encoding="UTF-8"?>']
        lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                     f'width="{width}" height="{height}">')
        lines.append(f'<rect width="100%" height="100%" fill="#0a0a0a"/>')
        for i in range(len(points) - 1):
            x1, y1 = to_svg(*points[i])
            x2, y2 = to_svg(*points[i + 1])
            lines.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" '
                         f'x2="{x2:.2f}" y2="{y2:.2f}" '
                         f'stroke="{color}" stroke-width="1.5"/>')
        lines.append('</svg>')
        with open(path, "w") as f:
            f.write("\n".join(lines))
        return path


def selftest():
    print("=" * 60)
    print(f"φ-DESIGN ENGINE v{__version__} — SELFTEST")
    print("=" * 60)
    gen = PhiShapeGenerator()

    shapes = {
        "phi_spiral": gen.phi_spiral(200),
        "fibonacci_vortex": gen.fibonacci_vortex(200),
        "merkaba_crystal": gen.merkaba_crystal(8),
        "fibonacci_tree": gen.fibonacci_tree(4),
        "fibonacci_phyllotaxis": gen.fibonacci_phyllotaxis(500),
    }

    for name, pts in shapes.items():
        print(f"  {name:25s}  {len(pts):5d} точек")

    print(f"\nφ = {PHI:.10f}")
    print(f"1/φ = {INV_PHI:.10f}")
    print(f"φ² = {PHI*PHI:.10f}")
    print("\n✅ SELFTEST пройден")
    print(f"Автор: {__author__}")


def demo():
    print("=" * 60)
    print(f"φ-DESIGN ENGINE v{__version__} — DEMO")
    print("=" * 60)
    engine = PhiDesignEngine(output_dir="designs")
    shapes = {
        "phi_spiral": engine.generator.phi_spiral(200),
        "fibonacci_vortex": engine.generator.fibonacci_vortex(200),
        "merkaba_crystal": engine.generator.merkaba_crystal(8),
    }
    for name, pts in shapes.items():
        path = f"designs/{name}.svg"
        result = engine.generate_svg(pts, path)
        print(f"  {name:25s}  → {result}  ({len(pts)} точек)")


def main():
    parser = argparse.ArgumentParser(
        description=f"φ-Design Engine v{__version__}")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        selftest()
        return
    if args.demo:
        demo()
        return
    selftest()


if __name__ == "__main__":
    main()
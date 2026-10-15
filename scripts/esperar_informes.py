#!/usr/bin/env python3
"""Espera a que los especialistas suban sus informes del día.

Uso: python3 scripts/esperar_informes.py AAAAMMDD slug1 [slug2 ...] [--minutos 45]
Hace git pull cada minuto hasta encontrar informes/<fecha>/<slug>.md para todos los slugs
o hasta agotar el plazo. Imprime cuáles llegaron y cuáles faltan.
"""
import argparse
import os
import subprocess
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("fecha")
ap.add_argument("slugs", nargs="+")
ap.add_argument("--minutos", type=int, default=45)
a = ap.parse_args()

limite = time.time() + a.minutos * 60
while True:
    subprocess.run(["git", "-C", RAIZ, "pull", "-q", "--rebase", "origin", "main"], capture_output=True)
    faltan = [s for s in a.slugs if not os.path.exists(os.path.join(RAIZ, "informes", a.fecha, f"{s}.md"))]
    if not faltan or time.time() > limite:
        break
    time.sleep(60)

print("llegaron:", ", ".join(s for s in a.slugs if s not in faltan) or "ninguno")
print("faltan:", ", ".join(faltan) or "ninguno")

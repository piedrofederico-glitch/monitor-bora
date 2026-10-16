"""Pone en vigencia los textos de vigencia diferida cuya fecha llegó.

Uso (desde la raíz del repo):
    python3 scripts/normas/activar_vigencias.py                  # hoy (hora Argentina)
    python3 scripts/normas/activar_vigencias.py --fecha 2026-10-23
    python3 scripts/normas/activar_vigencias.py --ver            # sólo lista lo pendiente

Lee organismos/cnv/normas-cnv/vigencias.md. Para cada línea abierta (`- [ ] AAAA-MM-DD · RG n/año · ubicación ·
archivo`) con fecha igual o anterior a la indicada:
1. agrega a historial/<archivo> las redacciones que dejan de regir (diferido/<archivo sin .md>.historial.md);
2. reemplaza vigente/<archivo> por diferido/<archivo> y borra ambos archivos de diferido/;
3. quita la marca de vigencia diferida de esas entradas en datos/modificaciones.json y regenera
   modificaciones.md y vigente/INDICE.md;
4. marca la línea con [x].
Después hay que commitear (ver docs/normas-cnv.md, "Vigencias diferidas").
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import normas as N  # noqa: E402

VIGENCIAS_MD = f'{N.NC}/vigencias.md'
LINEA = re.compile(r'^- \[( |x)\] (\d{4}-\d{2}-\d{2}) · RG (\d+)/(\d{4}) · (.*?) · `?diferido/([^`\s]+)`?\s*$')


def leer():
    L = open(VIGENCIAS_MD).read().split('\n')
    return L, [(i, LINEA.match(l)) for i, l in enumerate(L) if LINEA.match(l)]


def activar(i, m, L):
    archivo = m.group(6)
    n = int(m.group(3))
    dif = f'{N.DIF}/{archivo}'
    dif_h = dif[:-3] + '.historial.md'
    vig = f'{N.NC}/vigente/{archivo}'
    his = f'{N.HIS}/{archivo}'
    if not os.path.exists(dif):
        print(f'  ¡falta {dif}! (¿ya activado?)')
        return False
    if os.path.exists(dif_h):
        h = open(dif_h).read()
        if os.path.exists(his):
            # sin el encabezado del archivo de historial
            h = h[h.index('\n## '):] if '\n## ' in h else h
            open(his, 'a').write(h if h.startswith('\n') else '\n' + h)
        else:
            os.makedirs(os.path.dirname(his), exist_ok=True)
            open(his, 'w').write(h)
        os.remove(dif_h)
    os.makedirs(os.path.dirname(vig), exist_ok=True)
    os.replace(dif, vig)
    try:
        os.removedirs(os.path.dirname(dif))   # borra carpetas vacías de diferido/
    except OSError:
        pass
    d = json.load(open(N.MODS))
    for e in d:
        if e['n'] == n and e['archivo'] == archivo and e.get('diferido'):
            del e['diferido']
    json.dump(d, open(N.MODS, 'w'), ensure_ascii=False, indent=1)
    L[i] = L[i].replace('- [ ]', '- [x]', 1)
    print(f'  activado: RG {n}/{m.group(4)} en vigente/{archivo}')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fecha', help='AAAA-MM-DD (por defecto, hoy en Argentina)')
    ap.add_argument('--ver', action='store_true')
    a = ap.parse_args()
    hoy = a.fecha or (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).strftime('%Y-%m-%d')
    L, ls = leer()
    abiertas = [(i, m) for i, m in ls if m.group(1) == ' ']
    if a.ver or not abiertas:
        for i, m in abiertas:
            print(L[i])
        if not abiertas:
            print('Sin vigencias diferidas pendientes.')
        return
    hechas = 0
    for i, m in abiertas:
        if m.group(2) <= hoy:
            hechas += activar(i, m, L)
    open(VIGENCIAS_MD, 'w').write('\n'.join(L))
    if hechas:
        N.escribir_modificaciones()
        import indice
        indice.generar()
    print(f'{hechas} activadas al {hoy}; quedan {sum(1 for i, m in abiertas if m.group(2) > hoy)} pendientes.')


if __name__ == '__main__':
    main()

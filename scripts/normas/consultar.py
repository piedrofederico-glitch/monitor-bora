"""Consulta de redacciones de las Normas CNV: texto vigente, texto a una fecha y antes/después de una RG.

Uso (desde la raíz del repo):
    python3 scripts/normas/consultar.py --ubicacion "Tít. XIV Cap. III art. 40"              # todas las redacciones
    python3 scripts/normas/consultar.py --ubicacion "Tít. XIV Cap. III art. 40" --fecha 2026-10-01
    python3 scripts/normas/consultar.py --ubicacion "Tít. XIV Cap. III art. 40" --rg 1172    # antes y después
    python3 scripts/normas/consultar.py --ubicacion "Tít. V Cap. II Secc. VI art. 75"         # si el número se repite
    python3 scripts/normas/consultar.py --ubicacion "Tít. XIV Cap. III Anexo I" --rg 1172
    python3 scripts/normas/consultar.py --rg 1172                # qué tocó la RG y dónde está cada texto anterior
    python3 scripts/normas/consultar.py --rg 1172 --completo     # además, todos los textos anteriores

Fuentes: vigente/ (lo que rige hoy), historial/ (redacciones anteriores, con "Vigente desde/hasta" y la RG que
las reemplazó), diferido/ (lo que rige desde una fecha futura) y datos/modificaciones.json.
El texto sale literal, con las notas de vigencia. Una entrada "fragmento" del historial guarda sólo la parte que
se reemplazó (un inciso, un párrafo); el resto del artículo no cambió.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import normas as N  # noqa: E402

VIG = f'{N.NC}/vigente'


# ---------------------------------------------------------------- ubicación
def parse_ubicacion(s):
    s = s.strip()
    def g(rx):
        m = re.search(rx, s, re.I)
        return m.group(1).upper() if m else None
    tit = g(r'T[íi]t(?:ulo|\.)?\s*([IVXL]+)\b')
    cap = g(r'Cap(?:[íi]tulo|\.)?\s*([IVXL]+|preliminar)\b')
    sec = g(r'Secc?(?:i[óo]n|\.)?\s*([IVXL]+)\b')
    anexo = g(r'Anexo\s*([IVXL]+)\b')
    m = re.search(r'\bart(?:[íi]culo|\.)?\s*(\d+)\s*[°º]?\s*(bis|ter|qu[aá]ter|quinquies)?\b', s, re.I)
    art = None
    if m:
        art = m.group(1) + (' ' + m.group(2).upper().replace('QUÁTER', 'QUATER') if m.group(2) else '')
    if not tit:
        sys.exit('Indicá al menos el título: --ubicacion "Tít. XIV Cap. III art. 40"')
    return tit, cap, sec, art, anexo


def archivo_rel(tit, cap):
    if cap is None:
        return f'titulo-{tit}/titulo-{tit}.md'
    if cap == 'PRELIMINAR':
        return f'titulo-{tit}/capitulo-preliminar.md'
    return f'titulo-{tit}/capitulo-{cap}.md'


# ---------------------------------------------------------------- lectura
def leer_pars(texto):
    head, _, body = texto.partition('\n\n')
    if not head.startswith('# '):
        body = texto
    return [p for p in body.strip('\n').split('\n\n')] if body.strip() else []


def entradas_historial(path):
    """Entradas de un archivo de historial: dict(titulo, desde, hasta, por, texto, archivo)."""
    if not os.path.exists(path):
        return []
    t = open(path).read()
    out = []
    for bloque in re.split(r'\n(?=## )', t)[1:]:
        cab, _, resto = bloque.partition('\n- Texto:\n')
        titulo = cab.split('\n', 1)[0][3:].strip()
        desde = re.search(r'- Vigente desde: (.*)', cab)
        hasta = re.search(r'- Vigente hasta: (.*)', cab)
        por = re.search(r'- (?:[^:\n]*?) por: (RG (\d+)/(\d{4}).*)', cab)
        lineas = [l[2:] if l.startswith('> ') else ('' if l == '>' else None) for l in resto.strip('\n').split('\n')]
        texto = '\n'.join(l for l in lineas if l is not None)
        out.append(dict(titulo=titulo, desde=desde.group(1).strip() if desde else '', hasta=hasta.group(1).strip() if hasta else '',
                        por=por.group(1).strip() if por else '', rg=int(por.group(2)) if por else None,
                        texto=texto, archivo=os.path.relpath(path, N.NC), extra=cab))
    return out


def fecha_de(s):
    m = re.search(r'(\d{2}/\d{2}/\d{4})', s or '')
    return dt.datetime.strptime(m.group(1), '%d/%m/%Y').date() if m else None


class Texto(N.Cap):
    """Cap sobre una lista de párrafos (sin archivo)."""
    def __init__(self, pars, path):
        self.tit = self.cap = None
        self.path = path
        self.head = ['', '', '']
        self.pars = pars


def recortar(pars, path, art, sec, anexo):
    """Devuelve el texto del artículo/anexo dentro de una lista de párrafos, o None."""
    c = Texto(pars, path)
    recortar.contexto = '\n'.join(p for p in pars if re.match(r'^\[(Capítulo|Título) ', p))
    if anexo:
        for i, p in enumerate(pars):
            if re.match(rf'^### ANEXO\s+{anexo}\b', p, re.I):
                j = i + 1
                while j < len(pars) and not pars[j].startswith('### ANEXO'):
                    j += 1
                return '\n\n'.join(pars[i:j])
        return None
    if art:
        hits = [i for i, p in enumerate(pars) if N.clave_art(p) == art.upper() and (sec is None or c.seccion_de(i) == sec)]
        if not hits:
            return None
        trozos = []
        for i in hits:
            j = i + 1
            while j < len(pars) and N.clave_art(pars[j]) is None and not pars[j].startswith(('### ', '[Sección', '[Capítulo', '[Título')):
                j += 1
            trozos.append('\n\n'.join(pars[i:j]))
        recortar.contexto = c.contexto(hits[0])
        sep = '\n\n[— el texto tiene otro artículo con el mismo número —]\n\n'
        return sep.join(trozos)
    if sec:
        try:
            i, j = c.rango_seccion(sec)
        except KeyError:
            return None
        return '\n\n'.join(pars[i:j])
    return '\n\n'.join(pars)


def entrada_aplica(e, art, sec, anexo):
    """Texto de la ubicación pedida dentro de una entrada de historial (o None)."""
    t = e['titulo']
    pars = leer_pars(e['texto']) if e['texto'].startswith('# ') else [p for p in e['texto'].strip('\n').split('\n\n')]
    if art and re.match(rf'^Artículo {re.escape(art)}\b(?!\s*(BIS|TER|QUATER))', t, re.I):
        m = re.search(r'\(Sección ([IVXL]+)\)', t)
        if sec and m and m.group(1) != sec:
            return None
        return e['texto']
    if anexo and re.match(rf'^Anexo {anexo}\b', t):
        return e['texto']
    if t.startswith('Reemplazo de expresiones'):
        return None
    if re.match(r'^Artículo ', t):
        return None
    return recortar(pars, e['archivo'], art, sec, anexo)


# ---------------------------------------------------------------- línea de tiempo
def linea_de_tiempo(tit, cap, sec, art, anexo):
    rel = archivo_rel(tit, cap)
    base = rel[:-3]
    hist = [f'{N.HIS}/{rel}'] + sorted(glob.glob(f'{N.HIS}/{base}-derogado-RG-*.md'))
    versiones = []
    for h in hist:
        for e in entradas_historial(h):
            txt = entrada_aplica(e, art, sec, anexo)
            if txt:
                versiones.append(dict(tipo='historial', texto=txt, **{k: e[k] for k in ('titulo', 'desde', 'hasta', 'por', 'rg', 'archivo')}))
    versiones.sort(key=lambda v: fecha_de(v['hasta']) or dt.date.min)
    actual = None
    if os.path.exists(f'{VIG}/{rel}'):
        pars = leer_pars(open(f'{VIG}/{rel}').read())
        t = recortar(pars, f'vigente/{rel}', art, sec, anexo)
        if t:
            actual = dict(tipo='vigente', texto=t, archivo=f'vigente/{rel}', desde=N.vigente_desde(t, recortar.contexto), ctx=recortar.contexto)
    futuro = None
    if os.path.exists(f'{N.DIF}/{rel}'):
        pars = leer_pars(open(f'{N.DIF}/{rel}').read())
        t = recortar(pars, f'diferido/{rel}', art, sec, anexo)
        if t and (not actual or t != actual['texto']):
            futuro = dict(tipo='diferido', texto=t, archivo=f'diferido/{rel}', desde=N.vigente_desde(t, recortar.contexto), ctx=recortar.contexto)
    return rel, versiones, actual, futuro


def mostrar(v, rotulo):
    print(f'### {rotulo}')
    if v['tipo'] == 'historial':
        frag = ' (fragmento: sólo la parte reemplazada)' if 'fragmento' in v['titulo'] else ''
        print(f"Fuente: `{v['archivo']}`, entrada \"{v['titulo']}\"{frag}")
        print(f"Vigente desde: {v['desde']} · hasta: {v['hasta']} · reemplazada por: {v['por']}")
    else:
        print(f"Fuente: `{v['archivo']}` · vigente desde: {v['desde']}")
    print()
    print(v['texto'].strip('\n'))
    print()


def consulta_ubicacion(a):
    tit, cap, sec, art, anexo = parse_ubicacion(a.ubicacion)
    rel, versiones, actual, futuro = linea_de_tiempo(tit, cap, sec, art, anexo)
    cual = ' '.join(x for x in [f'Tít. {tit}', f'Cap. {cap}' if cap else '', f'Secc. {sec}' if sec else '',
                                f'art. {N.fmt_art(art)}' if art else '', f'Anexo {anexo}' if anexo else ''] if x)
    print(f'# {cual} (`{rel}`)\n')
    if not versiones and not actual and not futuro:
        sys.exit('No encontré esa ubicación ni en vigente/ ni en historial/ ni en diferido/.')
    todas = versiones + ([actual] if actual else []) + ([futuro] if futuro else [])
    if a.rg:
        antes = [k for k, v in enumerate(todas) if v['tipo'] == 'historial' and v['rg'] == a.rg]
        if not antes and futuro and actual and re.search(rf'RG {a.rg}/\d{{4}}', futuro['texto'] + futuro.get('ctx', '')):
            mostrar(actual, f'Antes de la RG {a.rg} (rige hasta el día anterior a {futuro["desde"]})')
            mostrar(futuro, f'Después de la RG {a.rg} (rige desde {futuro["desde"]}; vigencia diferida)')
            return
        if not antes:
            nota = [v for v in todas if v['tipo'] != 'historial' and re.search(rf'RG {a.rg}/\d{{4}}', v['texto'] + v.get('ctx', ''))]
            if nota:
                print(f'La RG {a.rg} no reemplazó un texto anterior en esta ubicación (la incorporó o modificó sin dejar historial propio).\n')
                mostrar(nota[0], 'Texto con la RG ' + str(a.rg))
            else:
                print(f'Según vigente/, historial/ y diferido/, la RG {a.rg} no modificó esta ubicación.')
            return
        for k in antes:
            mostrar(todas[k], f'Antes de la RG {a.rg}')
        sig = todas[antes[-1] + 1] if antes[-1] + 1 < len(todas) else None
        if sig:
            rot = 'Después de la RG ' + str(a.rg) + (' (texto vigente)' if sig['tipo'] == 'vigente' else
                                                   ' (rige desde ' + sig['desde'] + ')' if sig['tipo'] == 'diferido' else
                                                   ' (luego reemplazado de nuevo)')
            mostrar(sig, rot)
        else:
            print(f'Después de la RG {a.rg}: la ubicación quedó derogada o sin texto vigente.')
        return
    if a.fecha:
        f = dt.datetime.strptime(a.fecha, '%Y-%m-%d').date()
        for v in versiones:
            h = fecha_de(v['hasta'])
            if h and f <= h:
                d = fecha_de(v['desde'])
                if d and f < d and 'o antes' not in v['desde']:
                    break
                mostrar(v, f'Texto vigente al {f.strftime("%d/%m/%Y")}')
                return
        if futuro and fecha_de(futuro['desde']) and f >= fecha_de(futuro['desde']):
            mostrar(futuro, f'Texto vigente al {f.strftime("%d/%m/%Y")} (vigencia diferida)')
            return
        if actual:
            d = fecha_de(actual['desde'])
            if d and f < d and not versiones:
                print(f'Al {f.strftime("%d/%m/%Y")} esta ubicación no existía: rige desde {actual["desde"]}.')
                return
            mostrar(actual, f'Texto vigente al {f.strftime("%d/%m/%Y")}')
            return
        print('No hay texto para esa fecha (la ubicación fue derogada).')
        return
    for v in versiones:
        mostrar(v, f"Redacción anterior (hasta {v['hasta']})")
    if actual:
        mostrar(actual, 'Texto vigente')
    else:
        print('### Texto vigente\nNo tiene: la ubicación fue derogada o trasladada (ver modificaciones.md).\n')
    if futuro:
        mostrar(futuro, f"Texto que regirá desde {futuro['desde']} (vigencia diferida)")


def consulta_rg(a):
    mods = [e for e in json.load(open(N.MODS)) if e['n'] == a.rg]
    ficha = glob.glob(f'{N.RGDIR}/RG-{a.rg}-*.md')
    print(f"# RG {a.rg}: {len(mods)} afectaciones · ficha: `{os.path.relpath(ficha[0], N.REPO) if ficha else '(no hay)'}`\n")
    for e in mods:
        dif = f" (rige desde {e['diferido']}; texto en `diferido/{e['archivo']}`)" if e.get('diferido') else ''
        print(f"- {e['ubic'].replace(' | ', ', ')} — {e['op']}, art. {e['art']}{dif} — texto actual: `vigente/{e['archivo']}`")
    hs = []
    for h in sorted(glob.glob(f'{N.HIS}/**/*.md', recursive=True)) + sorted(glob.glob(f'{N.DIF}/**/*.historial.md', recursive=True)):
        hs += [e for e in entradas_historial(h) if e['rg'] == a.rg]
    print(f'\nTextos anteriores guardados ({len(hs)}):')
    for e in hs:
        print(f"- `{e['archivo']}` — \"{e['titulo']}\" (vigente hasta {e['hasta']})")
    if a.completo:
        for e in hs:
            print(f"\n### Antes de la RG {a.rg}: {e['titulo']} (`{e['archivo']}`)\nVigente desde: {e['desde']} · hasta: {e['hasta']}\n")
            print(e['texto'].strip('\n'))
    else:
        print('\nPara el texto de una ubicación antes y después: --ubicacion "..." --rg', a.rg, '; para todos los textos anteriores: --completo')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ubicacion', help='p. ej. "Tít. XIV Cap. III art. 40", "Tít. V Cap. II Secc. VI art. 75", "Tít. XIV Cap. III Anexo I"')
    ap.add_argument('--fecha', help='AAAA-MM-DD: redacción vigente a esa fecha')
    ap.add_argument('--rg', type=int, help='número de RG: redacción antes y después')
    ap.add_argument('--completo', action='store_true', help='con --rg sola: imprime todos los textos anteriores')
    a = ap.parse_args()
    if a.ubicacion:
        consulta_ubicacion(a)
    elif a.rg:
        consulta_rg(a)
    else:
        ap.print_help()


if __name__ == '__main__':
    main()

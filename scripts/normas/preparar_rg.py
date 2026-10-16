"""Prepara los insumos de una RG nueva para aplicarla con las herramientas: texto y metadatos.

Uso (desde la raíz del repo):
    python3 scripts/normas/preparar_rg.py <n> --bora organismos/cnv/normas/<AAAAMMDD>_<id>_resolucion-general-<n>-<año>.md
    python3 scripts/normas/preparar_rg.py <n> --bora <archivo> --pdf <url o ruta del PDF de la CNV>

Escribe:
- organismos/cnv/rg/fuentes/<n>.txt: texto con la disposición del PDF de la CNV (pdftotext -layout). Si el PDF no
  se consigue (la CNV a veces lo sube después que el BORA), lo arma desde el texto del BORA y lo avisa.
- la entrada <n> de organismos/cnv/rg/fuentes/meta.json: número, año, código GDE, fecha de firma, BO, aviso,
  firmantes, título y categoría de la CNV y enlaces.

El PDF de la CNV se busca en el listado de RG (www.cnv.gov.ar/sitioWeb/MarcoRegulatorio?panel=2).
Las tablas y la separación de párrafos salen mejor del PDF: si el texto vino del BORA, revisá las tablas a mano.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('NORMAS_REPO') or os.path.abspath(os.path.join(AQUI, '..', '..'))
FUENTES = f'{REPO}/organismos/cnv/rg/fuentes'
PANEL = 'https://www.cnv.gov.ar/sitioWeb/MarcoRegulatorio?panel=2'


def leer_bora(path):
    t = open(path).read()
    fm, _, cuerpo = t.partition('\n---\n')
    meta = {}
    for l in fm.split('\n'):
        m = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', l)
        if m:
            meta[m.group(1)] = m.group(2)
    return meta, cuerpo


def panel_cnv(n):
    """Fila del listado de RG de la CNV para la RG n (o None)."""
    try:
        t = subprocess.run(['curl', '-sS', '-m', '60', '-A', 'Mozilla/5.0', PANEL], capture_output=True, text=True, check=True).stdout
    except Exception as e:
        print(f'aviso: no pude leer el listado de la CNV ({e})')
        return None
    for r in re.findall(r'<tr>(.*?)</tr>', t, re.S):
        tds = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
        if len(tds) >= 4 and re.match(rf'RGCRGN{n}-\d+', tds[1]):
            links = re.findall(r'href="([^"]+)"', r)
            return dict(fecha=tds[0], categoria=tds[2], titulo=tds[3],
                        pdf=next((l for l in links if 'blob' in l), None), infoleg=next((l for l in links if 'infoleg' in l), None))
    return None


def texto_pdf(fuente):
    if re.match(r'^https?://', fuente):
        d = tempfile.mkdtemp()
        p = f'{d}/rg.pdf'
        subprocess.run(['curl', '-sS', '-L', '-m', '120', '-A', 'Mozilla/5.0', fuente, '-o', p], check=True)
    else:
        p = fuente
    r = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True, check=True)
    if len(r.stdout.strip()) < 500:
        raise RuntimeError('el PDF no tiene texto (¿escaneado?)')
    return r.stdout


def texto_bora(cuerpo, firmantes):
    """Convierte el texto del BORA (un párrafo por renglón, tablas con '|') al formato que esperan las herramientas:
    párrafos separados por renglón en blanco y tablas como renglones con columnas separadas por espacios."""
    L = [l.rstrip() for l in cuerpo.split('\n')]
    L = [l for l in L if not l.startswith('# ')]
    es_tabla = [('|' in l) for l in L]
    out = []
    for i, l in enumerate(L):
        if not l.strip():
            continue
        cerca = any(es_tabla[j] for j in range(max(0, i - 1), min(len(L), i + 2)))
        if es_tabla[i] or (cerca and out and out[-1] != '' and '|' in out[-1]):
            out.append('    '.join(c.strip() for c in l.split('|')).rstrip())
            continue
        if firmantes and l.strip() == firmantes.strip():
            out += ['', 'Digitally signed by (firmantes según el BORA)', l, '']
            continue
        if out and out[-1] != '':
            out.append('')
        out += [l, '']
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('--bora', required=True, help='archivo de organismos/cnv/normas/ con la RG')
    ap.add_argument('--pdf', help='URL o ruta del PDF de la CNV (si no, se busca en el listado)')
    a = ap.parse_args()
    fm, cuerpo = leer_bora(a.bora)
    m = re.search(r'(\d{1,4})/(\d{4})', fm.get('titulo', ''))
    if not m or int(m.group(1)) != a.n:
        sys.exit(f'el archivo del BORA no es la RG {a.n}: {fm.get("titulo")}')
    anio = int(m.group(2))
    meta = json.load(open(f'{FUENTES}/meta.json'))
    e = meta.get(str(a.n), {})
    e.update(n=a.n, anio=anio)
    gde = re.search(r'(RESGC-\d{4}-\d+-APN-[A-Z]+#CNV)', fm.get('codigo', ''))
    e['gde'] = gde.group(1) if gde else e.get('gde')
    f = re.search(r'Ciudad de Buenos Aires, (\d{1,2}/\d{1,2}/\d{4})', cuerpo)
    if f:
        e['firma_infoleg'] = f.group(1)
    a_bo = fm.get('fecha_publicacion', '')
    if re.match(r'\d{4}-\d{2}-\d{2}', a_bo):
        y, mm, d = a_bo.split('-')
        e['bo'] = f'{d}/{mm}/{y}'
    av = re.search(r'e\. (\d{2}/\d{2}/\d{4}) N° ?([\d/]+) v\. (\d{2}/\d{2}/\d{4})', cuerpo)
    if av:
        e['bo'], e['aviso_bo'], e['bo_hasta'] = av.group(1), av.group(2), av.group(3)
    e['firmantes'] = fm.get('firmantes') or e.get('firmantes')
    e['url_bora'] = fm.get('url')
    fila = panel_cnv(a.n)
    if fila:
        e.update(titulo_cnv=fila['titulo'], categoria=fila['categoria'], fecha_cnv=fila['fecha'],
                 pdf_cnv=fila['pdf'] or e.get('pdf_cnv'), infoleg=fila['infoleg'] or e.get('infoleg'))
    e.setdefault('titulo_cnv', fm.get('codigo', '').split(' - ', 1)[-1] or fm.get('titulo'))
    e.setdefault('categoria', '(sin dato: la RG todavía no figura en el listado de la CNV)')
    e.setdefault('pdf_cnv', e.get('url_bora'))
    texto = None
    pdf = a.pdf or (fila or {}).get('pdf')
    if pdf:
        try:
            texto = texto_pdf(pdf)
            e['fuente_texto'] = 'PDF CNV'
        except Exception as ex:
            print(f'aviso: no pude usar el PDF de la CNV ({ex}); uso el texto del BORA')
    if texto is None:
        texto = texto_bora(cuerpo, fm.get('firmantes'))
        e['fuente_texto'] = 'BORA'
    open(f'{FUENTES}/{a.n}.txt', 'w').write(texto)
    meta[str(a.n)] = e
    json.dump(meta, open(f'{FUENTES}/meta.json', 'w'), ensure_ascii=False, indent=1)
    print(f"RG {a.n}/{anio}: texto desde {e['fuente_texto']} → organismos/cnv/rg/fuentes/{a.n}.txt; BO {e.get('bo')}; GDE {e.get('gde')}")
    if e['fuente_texto'] == 'BORA':
        print('  revisá las tablas del texto: el BORA no conserva columnas como el PDF.')


if __name__ == '__main__':
    main()

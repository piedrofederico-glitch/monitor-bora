"""Herramientas para aplicar RG de la CNV sobre el texto consolidado de las Normas (N.T. 2013 y mod.).

Convenciones del texto consolidado (organismos/cnv/normas-cnv/vigente/<título>/<capítulo>.md):
- 3 renglones de encabezado (título, "Última modificación:", "Fuente:"), un blanco y el cuerpo.
- Cuerpo: párrafos separados por un renglón en blanco. Encabezados de sección/anexo con "### ".
- Un artículo empieza en el párrafo cuyo renglón ARTÍCULO N está precedido sólo por renglones de epígrafe
  y termina antes del próximo artículo o encabezado "### ".
- Notas de vigencia: párrafo final del artículo entre corchetes.
"""
import datetime as dt
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
from texto import a_markdown, ART, EPI  # noqa: E402

# Rutas: por defecto, el repo que contiene este script. Las variables de entorno permiten correr sobre una copia
# (prueba.py) o sobre la copia de vigencia diferida (NORMAS_VIG apuntando a diferido/, ver docs/normas-cnv.md).
AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('NORMAS_REPO') or os.path.abspath(os.path.join(AQUI, '..', '..'))
NC = f'{REPO}/organismos/cnv/normas-cnv'
VIG = os.environ.get('NORMAS_VIG') or f'{NC}/vigente'
HIS = f'{NC}/historial'
DIF = f'{NC}/diferido'
RGDIR = f'{REPO}/organismos/cnv/rg'
FUENTES = f'{RGDIR}/fuentes'            # texto de cada RG (<n>.txt) y meta.json
DATOS = f'{NC}/datos'                    # modificaciones.json y titulos.json
SIN_REGISTRO = os.environ.get('NORMAS_SIN_REGISTRO') == '1'   # no escribe historial ni modificaciones
DIFERIDO = os.path.abspath(VIG) == os.path.abspath(DIF)   # se aplica una RG de vigencia diferida (ver docs/normas-cnv.md)
META = json.load(open(f'{FUENTES}/meta.json'))
VIGENCIAS = {}   # n -> 'dd/mm/aaaa' (se completa en cada ficha)
ROMANOS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI',
           'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX']


def rom(x):
    return ROMANOS.index(x) + 1 if x in ROMANOS else 0


def fmt_art(k):
    k = str(k)
    p = k.split(' ', 1)
    return ordinal(p[0]) + (' ' + p[1] if len(p) > 1 else '')


def ordinal(n):
    """'1' -> '1°' ; '10' -> '10' (las RG escriben 1° a 9° con símbolo)."""
    n = str(n)
    return n + '°' if n.isdigit() and int(n) < 10 else n


# ---------------------------------------------------------------- RG
def fecha(s):
    return dt.datetime.strptime(s, '%d/%m/%Y').date()


def fstr(d):
    return d.strftime('%d/%m/%Y')


def rg_id(n):
    return f"RG {n}/{META[str(n)]['anio']}"


def nota(tipo, n, art_rg, extra=''):
    """[Artículo sustituido por art. 1° de la RG 1090/2025, BO 14/11/2025, vigente desde 02/02/2026]"""
    m = META[str(n)]
    v = VIGENCIAS.get(n)
    vig = ''
    if v and fecha(v) != fecha(m['bo']) + dt.timedelta(days=1):
        vig = f', vigente desde {v}'
    arts = art_rg if isinstance(art_rg, str) else ordinal(art_rg)
    return f"[{tipo} por art. {arts} de la {rg_id(n)}, BO {m['bo']}{vig}{extra}]"


def rg_lineas(n):
    """Renglones del texto layout de la RG, sin encabezado GDE ni bloque de firmas; None = salto de página."""
    t = open(f'{FUENTES}/{n}.txt').read()
    out = []
    for pi, p in enumerate(t.split('\f')):
        L = p.split('\n')
        while L and not L[-1].strip():
            L.pop()
        L = [l for l in L if not re.match(r'^\s*(IF|RESGC)-\d{4}-\d+-APN-\S+\s+Página \d+ de \d+\s*$', l)
             and not re.match(r'^\s*Página \d+ de \d+\s*$', l)]
        if pi:
            out.append(None)
        out += L
    return out


VERBOS = (r'(Sustitu|Incorpor|Derog|Reenumer|Renumer|Modific|Establec|La presente|Regístrese|Aprob|Dej|Dispon|Prorrog|Suspend|'
          r'Determin|Exim|Somet|Requer|Autoriz|Instru|Facult|Fij|Consider|Hac|Invit|Publi|Encomend|Reemplaz|Elimin|Agreg|'
          r'Excluir|Exceptu|Suprim|Reordenar|Trasladar|Comuníquese|Las presentes|Las disposiciones|Lo dispuesto|El presente|Reglament|Design|Otorg|Habilit|Mantener|Precis|Aclar|Ordenar|Tener)')


def rg_articulos(n, verbos=VERBOS):
    """Divide la parte resolutiva en artículos de la RG (numeración correlativa y verbo de acción).
    Devuelve lista de dict(num, enc, citas=[[renglones]], ini, fin)."""
    L = rg_lineas(n)
    i0 = next(i for i, l in enumerate(L) if l and re.match(r'^\s*RESUELVE:?\s*$', l))
    heads = []
    for i in range(i0 + 1, len(L)):
        l = L[i]
        if not l:
            continue
        m = re.match(r'^\s*(?:ART[ÍI]CULO|Art[íi]culo)\s+(\d+)\s*[°º]?\s*\.?\s*[-–]\s*' + verbos, l)
        if m and int(m.group(1)) == (heads[-1][1] + 1 if heads else 1):
            heads.append((i, int(m.group(1))))
    fin_total = len(L)
    for i in range(i0, len(L)):
        if L[i] and re.match(r'^\s*Digitally signed by', L[i]):
            fin_total = i; break
    arts = []
    for k, (i, num) in enumerate(heads):
        j = heads[k + 1][0] if k + 1 < len(heads) else fin_total
        span = L[i:j]
        texto = '\n'.join('\f' if x is None else x for x in span)
        a = texto.find('“')
        b = texto.rfind('”')
        enc = texto if a < 0 else texto[:a]
        citas = []
        if a >= 0 and b > a:
            # intentar segmentos balanceados de primer nivel
            segs = []; d = 0; ini = None; ok = True
            for x, ch in enumerate(texto):
                if ch == '“':
                    if d == 0: ini = x
                    d += 1
                elif ch == '”':
                    d -= 1
                    if d == 0: segs.append((ini, x))
                    if d < 0: ok = False; break
            if not ok or d != 0 or not segs:
                segs = [(a, b)]
            # descartar segmentos cortos que son sólo citas de títulos en el encabezado (p. ej. “PROYECTO ...”)
            for (x, y) in segs:
                seg = texto[x + 1:y]
                lineas = [None if z == '\f' else z for z in seg.split('\n')]
                citas.append(lineas)
            enc = texto[:segs[0][0]]
        arts.append(dict(num=num, enc=re.sub(r'\s+', ' ', enc).strip(), citas=citas, ini=i, fin=j))
    return arts


def md(lineas, epi_blanco=True):
    """Renglones (layout) de un texto citado -> lista de párrafos markdown."""
    L = list(lineas)
    # quitar renglones vacíos iniciales/finales
    while L and (L[0] is None or not L[0].strip()):
        L.pop(0)
    while L and (L[-1] is None or not L[-1].strip()):
        L.pop()
    if epi_blanco:
        # en los textos GDE el epígrafe va separado del ARTÍCULO por un blanco: lo pegamos
        L2 = []
        for i, l in enumerate(L):
            if l is not None and not l.strip():
                prev = next((x for x in reversed(L2) if x is not None), None)
                nxt = next((x for x in L[i + 1:] if x is not None and x.strip()), None)
                if prev and nxt and EPI.match(prev.strip()) and ART.match(nxt.strip()) and not re.match(r'^(SECCI|CAP[ÍI]TULO|T[ÍI]TULO|ANEXO)', prev.strip()):
                    continue
            L2.append(l)
        L = L2
    return post(a_markdown(L))


SEC = re.compile(r'(SECCI[ÓO]N\s+[IVXLC]+)\.?')


def post(ps):
    """Encabezados ### para SECCIÓN / ANEXO, igual que en la base."""
    out = []
    k = 0
    ps = list(ps)
    while k < len(ps):
        p = ps[k]
        m = SEC.fullmatch(p.strip())
        if m:
            tit = ''
            if k + 1 < len(ps):
                nx = ps[k + 1]
                first = nx.split('\n')[0]
                if '\n' in nx and ART.match(nx.split('\n')[-1]):
                    partes = nx.split('\n'); tit = partes[0]; ps[k + 1] = '\n'.join(partes[1:])
                elif EPI.match(first) and not ART.match(first) and not nx.startswith('```'):
                    tit = nx; ps[k + 1] = None
            out.append(f'### {m.group(1)}' + (f' — {tit}' if tit else ''))
            k += 1
            if k < len(ps) and ps[k] is None:
                k += 1
            continue
        if re.match(r'^ANEXO\s+[IVXLC]+\b', p) and len(p) < 200 and '\n' not in p:
            out.append('### ' + p); k += 1; continue
        if p is not None:
            out.append(p)
        k += 1
    return out


# ---------------------------------------------------------------- capítulos
def ruta(tit, cap=None):
    if cap is None:
        return f'{VIG}/titulo-{tit}/titulo-{tit}.md'
    if cap == 'PRELIMINAR':
        return f'{VIG}/titulo-{tit}/capitulo-preliminar.md'
    return f'{VIG}/titulo-{tit}/capitulo-{cap}.md'


def clave_art(par):
    """Si el párrafo inicia un artículo, devuelve su clave ('29', '4 BIS'); si no, None."""
    ls = par.split('\n')
    for j, l in enumerate(ls):
        m = re.match(r'^(?:ART[ÍI]CULO|Art[íi]culo|ARTICULO)\s*(\d+)\s*[°º]?\s*(BIS|TER|QUATER|QUÁTER|QUINQUIES)?\s*[\.\-–:]', l, re.I)
        if m:
            if all(EPI.match(x) for x in ls[:j]):
                return m.group(1) + (' ' + m.group(2).upper() if m.group(2) else '')
            return None
        if not EPI.match(l):
            return None
    return None


class Cap:
    def __init__(self, tit, cap=None):
        self.tit, self.cap = tit, cap
        self.path = ruta(tit, cap)
        if DIFERIDO and not os.path.exists(self.path):
            import shutil
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            shutil.copy(self.path.replace(DIF, f'{NC}/vigente', 1), self.path)
        t = open(self.path).read()
        head, _, body = t.partition('\n\n')
        self.head = head.split('\n')
        self.pars = [p for p in body.strip('\n').split('\n\n')] if body.strip() else []

    # -- ubicación
    def nombre(self):
        if self.cap is None:
            return f'Título {self.tit}'
        return f"Título {self.tit}, Capítulo {'Preliminar' if self.cap == 'PRELIMINAR' else self.cap}"

    def secciones(self):
        """lista de (indice_parrafo, 'XXIV', texto_encabezado)"""
        out = []
        for i, p in enumerate(self.pars):
            m = re.match(r'^### SECCI[ÓO]N\s+([IVXLC]+)\b', p)
            if m:
                out.append((i, m.group(1), p))
        return out

    def seccion_de(self, i):
        s = None
        for j, r, _ in self.secciones():
            if j <= i:
                s = r
        return s

    def rango_art(self, num, seccion=None):
        num = str(num).upper()
        hits = []
        for i, p in enumerate(self.pars):
            if clave_art(p) == num and (seccion is None or self.seccion_de(i) == seccion):
                hits.append(i)
        if len(hits) != 1:
            raise KeyError(f'{self.path}: artículo {num} sección {seccion}: {len(hits)} coincidencias')
        i = hits[0]
        j = i + 1
        while j < len(self.pars) and clave_art(self.pars[j]) is None and not self.pars[j].startswith(('### ', '[Sección', '[Capítulo', '[Título')):
            j += 1
        return i, j

    def rango_seccion(self, rom_sec):
        secs = self.secciones()
        for k, (i, r, _) in enumerate(secs):
            if r == rom_sec:
                j = secs[k + 1][0] if k + 1 < len(secs) else len(self.pars)
                # no comerse anexos del capítulo
                for x in range(i + 1, j):
                    if re.match(r'^### ANEXO', self.pars[x]):
                        j = x; break
                return i, j
        raise KeyError(f'{self.path}: sección {rom_sec} no encontrada')

    def contexto(self, i):
        """Notas de nivel capítulo/título y de la sección que contiene el párrafo i."""
        notas = [p for p in self.pars if re.match(r'^\[(Capítulo|Título) ', p)]
        sec = self.seccion_de(i)
        if sec:
            a, b = self.rango_seccion(sec)
            notas += [p for p in self.pars[a:b] if re.match(r'^\[Sección ', p)]
        return '\n'.join(notas)

    def texto(self, i, j):
        return '\n\n'.join(self.pars[i:j])

    def guardar(self, n):
        m = META[str(n)]
        self.head[1] = f"Última modificación: {rg_id(n)} (BO {m['bo']})"
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        open(self.path, 'w').write('\n'.join(self.head) + '\n\n' + '\n\n'.join(self.pars).strip('\n') + '\n')


# ---------------------------------------------------------------- historial / índice
def vigente_desde(texto_viejo, contexto=''):
    """Fecha desde la que rige un texto: la de la última nota de vigencia que contiene; si no tiene, la de la
    última nota de su sección/capítulo/título (contexto); si tampoco, 'anterior a la base'."""
    m = re.findall(r'\[[^\]]*? por art\. [^\]]*? de la RG (\d+)/(\d{4}), BO (\d{2}/\d{2}/\d{4})(?:, vigente desde (\d{2}/\d{2}/\d{4}))?\]', texto_viejo)
    if not m and contexto:
        m = re.findall(r'\[(?:Sección|Capítulo|Título)[^\]]*? por art\. [^\]]*? de la RG (\d+)/(\d{4}), BO (\d{2}/\d{2}/\d{4})(?:, vigente desde (\d{2}/\d{2}/\d{4}))?\]', contexto)
    if not m:
        return 'anterior a la base'
    n, a, bo, v = m[-1]
    if v:
        return v
    return fstr(fecha(bo) + dt.timedelta(days=1))


def vigencia_rg(n):
    m = META[str(n)]
    v = VIGENCIAS.get(n)
    return fecha(v) if v else fecha(m['bo']) + dt.timedelta(days=1)


def historial(cap, titulo_entrada, texto_viejo, n, art_rg, operacion, desde=None):
    if SIN_REGISTRO:
        return
    hp = cap.path[:-3] + '.historial.md' if DIFERIDO else cap.path.replace(VIG, HIS)
    os.makedirs(os.path.dirname(hp), exist_ok=True)
    if not os.path.exists(hp):
        open(hp, 'w').write(f'# Historial — {cap.head[0][2:]}\n\nRedacciones sustituidas o derogadas desde la base (PDF CNV actualizado a la RG 1094/2025). La más reciente va al final.\n')
    hasta = fstr(vigencia_rg(n) - dt.timedelta(days=1))
    arts = art_rg if isinstance(art_rg, str) else ordinal(art_rg)
    q = '\n'.join('> ' + x if x else '>' for x in texto_viejo.strip('\n').split('\n'))
    ent = (f'\n## {titulo_entrada}\n'
           f'- Vigente desde: {desde or vigente_desde(texto_viejo, getattr(cap, "_ctx", ""))}\n'
           f'- Vigente hasta: {hasta}\n'
           f'- {operacion} por: {rg_id(n)}, art. {arts}\n'
           f'- Texto:\n\n{q}\n')
    open(hp, 'a').write(ent)


MODS = f'{DATOS}/modificaciones.json'


def registrar(ubic_archivo, ubic, operacion, n, art_rg):
    if SIN_REGISTRO:
        return
    d = json.load(open(MODS)) if os.path.exists(MODS) else []
    arts = art_rg if isinstance(art_rg, str) else ordinal(art_rg)
    d.append(dict(archivo=ubic_archivo, ubic=ubic, op=operacion, n=n, rg=rg_id(n), art=arts, bo=META[str(n)]['bo']))
    if DIFERIDO:
        d[-1]['diferido'] = fstr(vigencia_rg(n))
    json.dump(d, open(MODS + '.tmp', 'w'), ensure_ascii=False, indent=1)
    os.replace(MODS + '.tmp', MODS)
    escribir_modificaciones()


def escribir_modificaciones():
    d = json.load(open(MODS)) if os.path.exists(MODS) else []

    def orden(a):
        m = re.match(r'titulo-([IVXL]+)/(?:capitulo-([IVXL]+|preliminar)|titulo-)', a)
        if m and '-derogado-RG-' in a:
            return (rom(m.group(1)), (rom(m.group(2)) if m.group(2) else 0) - 0.5)
        t = rom(m.group(1)) if m else 99
        c = m.group(2) if m else None
        return (t, -1 if c == 'preliminar' else (rom(c) if c else 0))
    grupos = {}
    for e in d:
        grupos.setdefault(e['archivo'], []).append(e)
    out = ['# Índice de modificaciones de las Normas CNV (N.T. 2013 y mod.)', '',
           'Índice inverso: ubicación → RG que la modificó desde la base (PDF CNV actualizado a la RG 1094/2025, BO 11/12/2025). '
           'Orden por título y capítulo; dentro de cada capítulo, en el orden en que se aplicaron las RG. '
           'Las redacciones anteriores están en `historial/` con la misma ruta.', '']
    for a in sorted(grupos, key=orden):
        if '-derogado-RG-' in a:
            out.append(f'## {grupos[a][0]["ubic"].split(" | ")[0]} (capítulo derogado)')
            out.append(f'Texto derogado: `historial/{a}`')
        else:
            out.append(f'## {grupos[a][0]["ubic"].split(" | ")[0]}')
            out.append(f'Archivo: `vigente/{a}`')
        out.append('')
        out.append('| Ubicación | Operación | RG | Artículo de la RG | BO |')
        out.append('|---|---|---|---|---|')
        for e in grupos[a]:
            op = e['op'] + (f" (rige desde {e['diferido']}; texto en `diferido/{a}`)" if e.get('diferido') else '')
            out.append(f"| {e['ubic'].split(' | ')[1] if ' | ' in e['ubic'] else e['ubic']} | {op} | {e['rg']} | {e['art']} | {e['bo']} |")
        out.append('')
    open(f'{NC}/modificaciones.md', 'w').write('\n'.join(out))


def rel(cap):
    return os.path.relpath(cap.path, VIG)


def ubic(cap, detalle):
    return f'{cap.nombre()} | {detalle}'


# ---------------------------------------------------------------- operaciones
def agregar_nota(pars, texto_nota):
    return pars + [texto_nota]


def sustituir_articulo(tit, cap, num, nuevos_pars, n, art_rg, seccion=None, epigrafe_det=None):
    c = Cap(tit, cap)
    i, j = c.rango_art(num, seccion)
    c._ctx = c.contexto(i)
    viejo = c.texto(i, j)
    sec = c.seccion_de(i)
    det = f"art. {fmt_art(num)}" + (f" (Secc. {sec})" if sec else '')
    historial(c, f"Artículo {num}" + (f" (Sección {sec})" if sec else ''), viejo, n, art_rg, 'Sustituido')
    c.pars[i:j] = list(nuevos_pars) + [nota('Artículo sustituido', n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, det), 'sustituye', n, art_rg)
    return c


def modificar_articulo(tit, cap, num, fn, n, art_rg, nota_txt, seccion=None, det_extra=''):
    """fn(lista_parrafos) -> lista_parrafos nueva (sin notas nuevas). nota_txt: 'Inciso b) sustituido' etc."""
    c = Cap(tit, cap)
    i, j = c.rango_art(num, seccion)
    c._ctx = c.contexto(i)
    viejo = c.texto(i, j)
    sec = c.seccion_de(i)
    old = list(c.pars[i:j])
    nuevos = fn(list(old))
    if nuevos == old:
        raise ValueError('modificar_articulo: sin cambios')
    # sólo el fragmento reemplazado o suprimido pasa al historial (si es una pura incorporación, no hay entrada)
    a = 0
    while a < min(len(old), len(nuevos)) and old[a] == nuevos[a]:
        a += 1
    b = 0
    while b < min(len(old), len(nuevos)) - a and old[-1 - b] == nuevos[-1 - b]:
        b += 1
    quitado = old[a:len(old) - b]
    if quitado:
        d = vigente_desde(viejo, c._ctx)
        d = d if d == 'anterior a la base' else f'{d} o antes (fecha de la última modificación registrada en el artículo)'
        historial(c, f"Artículo {num}" + (f" (Sección {sec})" if sec else '') + ' — fragmento', '\n\n'.join(quitado), n, art_rg,
                  'Sustituido/suprimido parcialmente', desde=d)
    c.pars[i:j] = nuevos + [nota(nota_txt, n, art_rg)]
    c.guardar(n)
    det = f"art. {fmt_art(num)}" + (f" (Secc. {sec})" if sec else '') + (f", {det_extra}" if det_extra else '')
    registrar(rel(c), ubic(c, det), 'modifica parcialmente', n, art_rg)
    return c


def incorporar_articulo(tit, cap, nuevos_pars, n, art_rg, despues_de=None, seccion=None, al_final_de_seccion=None, al_inicio=False, num=None):
    """Inserta después del artículo `despues_de` (clave), o al final de la sección indicada."""
    c = Cap(tit, cap)
    k0 = num or clave_art(next(p for p in nuevos_pars if clave_art(p)))
    stub = [x for x, p in enumerate(c.pars) if clave_art(p) == k0 and '[Derogado por' in p]
    if stub:
        # el número estaba ocupado por un artículo derogado: el nuevo texto ocupa su lugar
        x = stub[0]
        c.pars[x:x + 1] = list(nuevos_pars) + [nota('Artículo incorporado', n, art_rg)]
        c.guardar(n)
        sec = c.seccion_de(x)
        registrar(rel(c), ubic(c, f"art. {fmt_art(k0)}" + (f" (Secc. {sec})" if sec else '')), 'incorpora', n, art_rg)
        return c
    if despues_de is not None:
        _, j = c.rango_art(despues_de, seccion)
    elif al_final_de_seccion is not None:
        _, j = c.rango_seccion(al_final_de_seccion)
    elif al_inicio:
        j = 0
    else:
        j = len(c.pars)
        while j > 0 and c.pars[j - 1].startswith('### ANEXO'):
            j -= 1
    nuevos = list(nuevos_pars) + [nota('Artículo incorporado', n, art_rg)]
    c.pars[j:j] = nuevos
    c.guardar(n)
    k = num or clave_art(next(p for p in nuevos_pars if clave_art(p)))
    sec = c.seccion_de(j)
    registrar(rel(c), ubic(c, f"art. {fmt_art(k)}" + (f" (Secc. {sec})" if sec else '')), 'incorpora', n, art_rg)
    return c


def derogar_articulo(tit, cap, num, n, art_rg, seccion=None, verbo='Derogado'):
    c = Cap(tit, cap)
    i, j = c.rango_art(num, seccion)
    c._ctx = c.contexto(i)
    viejo = c.texto(i, j)
    sec = c.seccion_de(i)
    historial(c, f"Artículo {num}" + (f" (Sección {sec})" if sec else ''), viejo, n, art_rg, 'Derogado')
    c.pars[i:j] = [f"ARTÍCULO {ordinal(num) if ' ' not in str(num) else num}.- " + nota(verbo, n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, f"art. {fmt_art(num)}" + (f" (Secc. {sec})" if sec else '')), 'deroga', n, art_rg)
    return c


def sustituir_seccion(tit, cap, sec, nuevos_pars, n, art_rg, nota_tipo='Sección sustituida'):
    c = Cap(tit, cap)
    i, j = c.rango_seccion(sec)
    c._ctx = c.contexto(i)
    viejo = c.texto(i, j)
    historial(c, f"Sección {sec} (completa)", viejo, n, art_rg, 'Sustituida')
    c.pars[i:j] = list(nuevos_pars) + [nota(nota_tipo, n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, f"Secc. {sec} (completa)"), 'sustituye', n, art_rg)
    return c


def derogar_seccion(tit, cap, sec, n, art_rg, verbo='derogada'):
    c = Cap(tit, cap)
    i, j = c.rango_seccion(sec)
    c._ctx = c.contexto(i)
    viejo = c.texto(i, j)
    titulo_sec = c.pars[i]
    historial(c, f"Sección {sec} (completa)", viejo, n, art_rg, 'Derogada')
    nom = re.sub(r'^### SECCI[ÓO]N\s+[IVXLC]+\s*(—\s*)?', '', titulo_sec).strip()
    c.pars[i:j] = [nota(f'Sección {sec}' + (f' ({nom})' if nom else '') + f' {verbo}', n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, f"Secc. {sec} (completa)"), 'deroga', n, art_rg)
    return c


def incorporar_seccion(tit, cap, nuevos_pars, n, art_rg, despues_de_seccion=None, antes_de_anexos=True):
    c = Cap(tit, cap)
    if despues_de_seccion:
        _, j = c.rango_seccion(despues_de_seccion)
    else:
        j = len(c.pars)
        if antes_de_anexos:
            while j > 0 and any(c.pars[x].startswith('### ANEXO') for x in range(j - 1, j)):
                j -= 1
            # si hay anexos, insertar antes del primero
            for x, p in enumerate(c.pars):
                if p.startswith('### ANEXO'):
                    j = x; break
    c.pars[j:j] = list(nuevos_pars) + [nota('Sección incorporada', n, art_rg)]
    c.guardar(n)
    m = re.match(r'^### SECCI[ÓO]N\s+([IVXLC]+)', nuevos_pars[0])
    registrar(rel(c), ubic(c, f"Secc. {m.group(1) if m else '?'} (completa)"), 'incorpora', n, art_rg)
    return c


def sustituir_capitulo(tit, cap, nombre, nuevos_pars, n, art_rg, nota_tipo='Capítulo sustituido'):
    p = ruta(tit, cap)
    m = META[str(n)]
    if os.path.exists(p):
        c = Cap(tit, cap)
        viejo = c.head[0] + '\n\n' + '\n\n'.join(c.pars)
        historial(c, f"{c.nombre()} (completo)", viejo, n, art_rg, 'Sustituido')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    capn = 'Preliminar' if cap == 'PRELIMINAR' else cap
    head = f"# Título {tit} — Capítulo {capn}: {nombre}" if cap else f"# Título {tit} — {nombre}"
    open(p, 'w').write(head + f"\nÚltima modificación: {rg_id(n)} (BO {m['bo']})\nFuente: {rg_id(n)}, art. {ordinal(art_rg) if not isinstance(art_rg, str) else art_rg}.\n\n"
                       + '\n\n'.join(list(nuevos_pars) + [nota(nota_tipo, n, art_rg)]) + '\n')
    c = Cap(tit, cap)
    registrar(rel(c), ubic(c, 'capítulo completo' if cap else 'título completo'), 'sustituye' if 'sustituido' in nota_tipo else 'incorpora', n, art_rg)
    return c


def derogar_capitulo(tit, cap, n, art_rg):
    c = Cap(tit, cap)
    viejo = c.head[0] + '\n\n' + '\n\n'.join(c.pars)
    historial(c, f"{c.nombre()} (completo)", viejo, n, art_rg, 'Derogado')
    c.pars = [nota('Capítulo derogado', n, art_rg)]
    c.head[2] = 'Fuente: ' + rg_id(n) + '.'
    c.guardar(n)
    registrar(rel(c), ubic(c, 'capítulo completo'), 'deroga', n, art_rg)
    return c


def renumerar_articulo(tit, cap, num, nuevo, n, art_rg, seccion=None):
    """Cambia el número en el renglón ARTÍCULO y deja nota."""
    c = Cap(tit, cap)
    i, j = c.rango_art(num, seccion)
    c._ctx = c.contexto(i)
    ls = c.pars[i].split('\n')
    for k, l in enumerate(ls):
        if ART.match(l):
            ls[k] = re.sub(r'^((?:ART[ÍI]CULO|ARTICULO|Art[íi]culo)\s*)\d+\s*[°º]?', lambda m: m.group(1) + ordinal(nuevo), l, count=1)
            break
    c.pars[i] = '\n'.join(ls)
    c.pars[j:j] = [nota(f'Artículo renumerado (antes art. {num}' + (f' de la Secc. {seccion}' if seccion else '') + ')', n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, f"art. {num} → {nuevo}"), 'renumera', n, art_rg)
    return c


def renumerar_seccion(tit, cap, sec, nueva, n, art_rg):
    c = Cap(tit, cap)
    i, j = c.rango_seccion(sec)
    c._ctx = c.contexto(i)
    c.pars[i] = re.sub(r'^### SECCI[ÓO]N\s+' + sec + r'\b', '### SECCIÓN ' + nueva, c.pars[i])
    c.pars[i + 1:i + 1] = [nota(f'Sección renumerada (antes Secc. {sec})', n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, f"Secc. {sec} → {nueva}"), 'renumera', n, art_rg)
    return c


def cierre(n):
    """Regenera el índice de archivos y actualiza la línea de estado de base.md."""
    import indice
    indice.generar()
    p = f'{NC}/base.md'
    t = open(p).read().split('\n', 1)
    estado = 'en curso' if 'en curso' in t[0] else 'terminada'
    open(p, 'w').write(f'Estado: construcción {estado} (última RG aplicada: {n}/{META[str(n)]["anio"]})\n' + t[1])


def dividir_capitulos(lineas):
    """Divide un texto citado que contiene varios 'CAPÍTULO N' en [(rom, nombre, renglones)]."""
    idx = [i for i, l in enumerate(lineas) if l and re.fullmatch(r'CAP[ÍI]TULO\s+([IVXL]+|PRELIMINAR)\.?', l.strip())]
    out = []
    for k, i in enumerate(idx):
        j = idx[k + 1] if k + 1 < len(idx) else len(lineas)
        rom_ = re.fullmatch(r'CAP[ÍI]TULO\s+([IVXL]+|PRELIMINAR)\.?', lineas[i].strip()).group(1)
        x = i + 1
        while x < j and (lineas[x] is None or not lineas[x].strip()):
            x += 1
        nom = []
        while x < j and lineas[x] is not None and lineas[x].strip() and EPI.match(lineas[x].strip()) \
                and not re.match(r'^(SECCI[ÓO]N|ART[ÍI]CULO)', lineas[x].strip()):
            nom.append(re.sub(r'\s+', ' ', lineas[x].strip())); x += 1
        out.append((rom_, ' '.join(nom), lineas[x:j]))
    return out


def dividir_secciones(lineas):
    """[(rom, renglones_desde_el_encabezado_SECCIÓN)]"""
    idx = [i for i, l in enumerate(lineas) if l and re.fullmatch(r'SECCI[ÓO]N\s+([IVXL]+)\.?', l.strip())]
    return [(re.fullmatch(r'SECCI[ÓO]N\s+([IVXL]+)\.?', lineas[i].strip()).group(1), lineas[i:(idx[k + 1] if k + 1 < len(idx) else len(lineas))])
            for k, i in enumerate(idx)]


def tramo(desde, hasta, nuevos, ocurrencia=0):
    """Devuelve fn(pars) que reemplaza el texto desde `desde` (incl.) hasta `hasta` (excl.; None = fin del artículo)
    por los párrafos `nuevos`. Si `desde` cae dentro de un párrafo, el texto previo queda como párrafo propio."""
    def fn(pars):
        t = '\n\n'.join(pars)
        i = -1
        for _ in range(ocurrencia + 1):
            i = t.find(desde, i + 1)
        if i < 0:
            raise ValueError(f'tramo: no encuentro {desde!r}')
        if hasta is None:
            # hasta el final, sin incluir notas de vigencia finales
            j = len(t)
            m = re.search(r'(\n\n\[[^\]]*\])+$', t)
            if m:
                j = m.start()
        elif hasta == desde:
            j = i
        else:
            j = t.find(hasta, i + len(desde))
            if j < 0:
                raise ValueError(f'tramo: no encuentro {hasta!r}')
        antes = t[:i].rstrip(' ')
        if antes and not antes.endswith('\n\n'):
            antes = antes.rstrip() + '\n\n'
        despues = t[j:]
        nuevo = '\n\n'.join(nuevos)
        if despues and not despues.startswith('\n\n') and nuevo:
            nuevo += '\n\n'
        r = antes + nuevo + despues.lstrip(' ') if nuevo else antes.rstrip('\n') + ('\n\n' + despues.lstrip() if despues.strip() else '')
        return [p for p in r.split('\n\n') if p.strip()]
    return fn


def insertar_antes(ancla, nuevos):
    """fn(pars) que inserta párrafos antes del texto `ancla` (si cae en medio de un párrafo, lo parte)."""
    return tramo(ancla, ancla, list(nuevos))


def insertar_despues(ancla, nuevos):
    def fn(pars):
        t = '\n\n'.join(pars)
        i = t.find(ancla)
        if i < 0:
            raise ValueError(f'insertar_despues: no encuentro {ancla!r}')
        j = i + len(ancla)
        r = t[:j] + '\n\n' + '\n\n'.join(nuevos) + ('\n\n' + t[j:].lstrip() if t[j:].strip() else '')
        return [p for p in r.split('\n\n') if p.strip()]
    return fn


def sin_elipsis(ps):
    """Quita encabezado de artículo y '(…)' de una cita parcial: devuelve sólo los párrafos nuevos posteriores a la última elipsis inicial."""
    k = max((i for i, p in enumerate(ps) if p.strip() in ('(…)', '(...)', '…', '...')), default=-1)
    return ps[k + 1:]


def sustituir_titulo(tit, capitulos, n, art_rg, nombre_titulo=None):
    """Sustituye un Título completo. capitulos: [(rom, nombre, pars)] o [(None, nombre, pars)] si no tiene capítulos.
    La redacción anterior (todos los archivos del título) pasa a historial."""
    import glob
    d = f'{VIG}/titulo-{tit}'
    for f in sorted(glob.glob(f'{d}/*.md')):
        b = os.path.basename(f)[:-3]
        cap = None if b.startswith('titulo-') else ('PRELIMINAR' if b == 'capitulo-preliminar' else b[9:])
        c = Cap(tit, cap)
        viejo = c.head[0] + '\n\n' + '\n\n'.join(c.pars)
        historial(c, f"{c.nombre()} (completo)", viejo, n, art_rg, 'Sustituido (sustitución del Título completo)')
        os.remove(f)
    for rom_, nombre, pars in capitulos:
        p = ruta(tit, rom_)
        m = META[str(n)]
        head = f"# Título {tit} — Capítulo {rom_}: {nombre}" if rom_ else f"# Título {tit} — {nombre}"
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(head + f"\nÚltima modificación: {rg_id(n)} (BO {m['bo']})\nFuente: {rg_id(n)}, art. {ordinal(art_rg)}.\n\n"
                           + '\n\n'.join(list(pars) + [nota('Título sustituido', n, art_rg)]) + '\n')
        c = Cap(tit, rom_)
        registrar(rel(c), ubic(c, 'capítulo completo' if rom_ else 'título completo'), 'sustituye', n, art_rg)


def derogar_capitulo_y_quitar(tit, cap, n, art_rg):
    """Deroga un capítulo: su texto pasa a historial y el archivo se elimina de vigente/ (para permitir renumeraciones)."""
    c = Cap(tit, cap)
    viejo = c.head[0] + '\n\n' + '\n\n'.join(c.pars)
    original = c.path
    # el historial del capítulo derogado se guarda con nombre propio, para no mezclarlo con un capítulo que luego tome su número
    c.path = original[:-3] + f"-derogado-RG-{n}-{META[str(n)]['anio']}.md"
    ho = original.replace(VIG, HIS)
    if os.path.exists(ho):
        os.rename(ho, c.path.replace(VIG, HIS))
    historial(c, f"{c.nombre()} (completo)", viejo, n, art_rg, 'Derogado')
    registrar(rel(c), ubic(c, 'capítulo completo'), 'deroga', n, art_rg)
    os.remove(original)


def renumerar_capitulo(tit, cap, nuevo, n, art_rg):
    c = Cap(tit, cap)
    destino = ruta(tit, nuevo)
    assert not os.path.exists(destino), destino
    c.head[0] = re.sub(r'Capítulo ' + cap + r'\b', 'Capítulo ' + nuevo, c.head[0], count=1)
    c.pars = c.pars + [nota(f'Capítulo renumerado (antes Capítulo {cap})', n, art_rg)]
    old = c.path
    c.path = destino
    c.cap = nuevo
    c.guardar(n)
    os.remove(old)
    # el historial del capítulo viaja con él
    ho, hn = old.replace(VIG, HIS), destino.replace(VIG, HIS)
    if os.path.exists(ho):
        os.rename(ho, hn)
    registrar(rel(c), ubic(c, f'capítulo completo (antes Cap. {cap})'), 'renumera', n, art_rg)


def por_articulo(ps):
    """Parte una lista de párrafos citados en bloques por artículo: [(clave, [pars])]. Lo previo al primer artículo se descarta."""
    idx = [i for i, p in enumerate(ps) if clave_art(p)] + [len(ps)]
    return [(clave_art(ps[a]), ps[a:b]) for a, b in zip(idx, idx[1:])]


def parrafo(empieza, nuevos, hasta_siguiente_termino=True):
    """fn(pars): reemplaza el párrafo que empieza con `empieza` (y, si es un término del glosario, los párrafos
    siguientes hasta el próximo término “...” significa) por `nuevos`."""
    def fn(pars):
        idx = [i for i, p in enumerate(pars) if p.startswith(empieza)]
        if len(idx) != 1:
            raise ValueError(f'parrafo: {len(idx)} coincidencias para {empieza!r}')
        i = idx[0]; j = i + 1
        if hasta_siguiente_termino:
            while j < len(pars) and not re.match(r'^“[^”]+”\s+(significa|tiene)', pars[j]) and not pars[j].startswith('['):
                j += 1
        return pars[:i] + list(nuevos) + pars[j:]
    return fn


def termino_nuevo(nuevos):
    """fn(pars): inserta definiciones del glosario (art. 2°, Tít. I, Cap. II) en orden alfabético."""
    import locale

    def k(s):
        m = re.match(r'^“([^”]+)”', s)
        m2 = re.match(r'^(.+?)\s+significa', s)
        s = m.group(1) if m else (m2.group(1) if m2 else s[:40])
        s = unicodedata.normalize('NFKD', s)
        return ''.join(c for c in s if not unicodedata.combining(c)).lower()

    def fn(pars):
        out = list(pars)
        for nv in nuevos:
            if not (nv.startswith('“') or re.match(r'^.+?\s+significa', nv)):
                raise ValueError('termino_nuevo: no es una definición: ' + nv[:60])
            terms = [(i, p) for i, p in enumerate(out) if _clave_def(p)]
            pos = None
            for i, p in terms:
                if k(p) > k(nv):
                    pos = i; break
            if pos is None:
                # después del último término y de sus párrafos de continuación
                i = terms[-1][0] + 1
                while i < len(out) and not out[i].startswith('['):
                    i += 1
                pos = i
            out.insert(pos, nv)
        return out
    return fn


def bloque(n, k, verbos=VERBOS):
    """Texto citado del art. k de la RG n tomado como bloque: desde la primera “ hasta el final del artículo,
    sin la ” final. Para RG con comillas internas desbalanceadas."""
    L = rg_lineas(n)
    a = next(x for x in rg_articulos(n, verbos) if x['num'] == k)
    span = L[a['ini']:a['fin']]
    texto = '\n'.join('\f' if x is None else x for x in span)
    i = texto.find('“')
    t = texto[i + 1:].rstrip()
    if t.endswith('”'):
        t = t[:-1]
    elif t.endswith('”.'):
        t = t[:-2]
    return [None if z == '\f' else z for z in t.split('\n')]


def definiciones(ps):
    """Párrafos de definiciones de una cita del glosario: sin el encabezado del artículo ni las elipsis."""
    return [p for p in ps if p.strip() not in ('(…)', '(...)', '(…).', '(…)”.') and not clave_art(p)
            and not p.startswith(('TÉRMINOS DEFINIDOS', 'EXPRESIONES'))]


def anexos(c):
    return [(i, p) for i, p in enumerate(c.pars) if p.startswith('### ANEXO')]


def incorporar_anexo(tit, cap, nuevos_pars, n, art_rg, nombre=None):
    """Agrega un anexo al final del capítulo (los anexos van al final)."""
    c = Cap(tit, cap)
    if not nuevos_pars[0].startswith('### ANEXO'):
        raise ValueError('incorporar_anexo: la cita no empieza con el encabezado ANEXO')
    c.pars = c.pars + list(nuevos_pars) + [nota('Anexo incorporado', n, art_rg)]
    c.guardar(n)
    nom = nombre or re.match(r'^### (ANEXO\s+[IVXL]+)', nuevos_pars[0]).group(1).title().replace('Anexo', 'Anexo')
    registrar(rel(c), ubic(c, nom), 'incorpora', n, art_rg)
    return c


def rango_anexo(c, rom_):
    ax = anexos(c)
    for k, (i, p) in enumerate(ax):
        if re.match(r'^### ANEXO\s+' + rom_ + r'\b', p):
            j = ax[k + 1][0] if k + 1 < len(ax) else len(c.pars)
            return i, j
    raise KeyError(f'anexo {rom_} no encontrado en {c.path}')


def sustituir_anexo(tit, cap, rom_, nuevos_pars, n, art_rg):
    c = Cap(tit, cap)
    i, j = rango_anexo(c, rom_)
    c._ctx = '\n'.join(p for p in c.pars if re.match(r'^\[(Capítulo|Título) ', p))
    historial(c, f'Anexo {rom_}', c.texto(i, j), n, art_rg, 'Sustituido')
    c.pars[i:j] = list(nuevos_pars) + [nota('Anexo sustituido', n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, f'Anexo {rom_}'), 'sustituye', n, art_rg)
    return c


TITJ = f'{DATOS}/titulos.json'


def sustituir_denominacion_titulo(tit, nuevo, n, art_rg):
    d = json.load(open(TITJ))
    viejo = d[tit]['nombre']
    hp = f'{HIS}/titulo-{tit}/denominacion.md'
    os.makedirs(os.path.dirname(hp), exist_ok=True)
    if not os.path.exists(hp):
        open(hp, 'w').write(f'# Historial — denominación del Título {tit}\n')
    open(hp, 'a').write(f"\n## Denominación del Título {tit}\n- Vigente desde: {d[tit].get('desde') or 'anterior a la base'}\n"
                        f"- Vigente hasta: {fstr(vigencia_rg(n) - dt.timedelta(days=1))}\n- Sustituida por: {rg_id(n)}, art. {ordinal(art_rg)}\n- Texto:\n\n> TÍTULO {tit}. {viejo}\n")
    d[tit] = {'nombre': nuevo, 'nota': nota('Denominación sustituida', n, art_rg), 'desde': fstr(vigencia_rg(n))}
    json.dump(d, open(TITJ, 'w'), ensure_ascii=False, indent=1)
    registrar(f'titulo-{tit}/denominacion', f'Título {tit} | denominación', 'sustituye', n, art_rg)


def titulo_derogado(tit, n, art_rg):
    d = json.load(open(TITJ))
    d[tit]['nota'] = nota('Título derogado', n, art_rg)
    d[tit]['derogado'] = True
    json.dump(d, open(TITJ, 'w'), ensure_ascii=False, indent=1)


def rg_anexo(n, inicio=r'^\s*ANEXO\s+I\.?\s*$', fin=None):
    """Renglones de un anexo IF publicado a continuación de la resolución (desde la primera línea que coincide con
    `inicio`, posterior a RESUELVE, hasta `fin` o el final), sin pies GDE."""
    L = rg_lineas(n)
    i0 = next(i for i, l in enumerate(L) if l and re.match(r'^\s*RESUELVE:?\s*$', l))
    i = next(i for i in range(i0, len(L)) if L[i] and re.match(inicio, L[i]))
    j = len(L)
    if fin:
        j = next((x for x in range(i + 1, len(L)) if L[x] and re.match(fin, L[x])), len(L))
    out = []
    for l in L[i:j]:
        if l is not None and (re.match(r'^\s*IF-\d{4}-\d+-\s*APN-\S+#CNV\s*$', l) or re.match(r'^\s*Página \d+ de \d+\s*$', l)
                              or re.match(r'^\s*Digitally signed by', l) or re.match(r'^\s*(Date|Location):', l)):
            continue
        out.append(l)
    while out and (out[-1] is None or not out[-1].strip()):
        out.pop()
    return out


def reemplazo_global(pares, n, art_rg, descripcion):
    """Reemplaza expresiones en todo vigente/ (sin tocar notas entre corchetes). Por archivo: entrada de historial con
    los artículos afectados y el detalle de cada reemplazo, nota al inicio del cuerpo y registro en el índice."""
    import glob
    total = 0
    for f in sorted(glob.glob(f'{VIG}/titulo-*/*.md')):
        r = os.path.relpath(f, VIG)
        t_, c_ = r.split('/')
        tit = t_[7:]
        cap = None if c_.startswith('titulo-') else ('PRELIMINAR' if c_ == 'capitulo-preliminar.md' else c_[9:-3])
        c = Cap(tit, cap)
        afect = []
        cnt = 0
        art_actual = None
        for i, p in enumerate(c.pars):
            k = clave_art(p)
            if k:
                art_actual = k
            if p.startswith('['):
                continue
            q = p
            for pat, rep in pares:
                q, m = re.subn(pat, rep, q)
                cnt += m
            if q != p:
                c.pars[i] = q
                sec = c.seccion_de(i)
                lugar = (f'art. {fmt_art(art_actual)}' if art_actual else 'texto sin artículo') + (f' (Secc. {sec})' if sec else '')
                if p.startswith('### ANEXO') or any(x.startswith('### ANEXO') for x in c.pars[:i]):
                    ax = [x for x in c.pars[:i + 1] if x.startswith('### ANEXO')]
                    lugar = ax[-1][4:].split(' ')[0] + ' ' + ax[-1][4:].split(' ')[1]
                if lugar not in afect:
                    afect.append(lugar)
        if cnt:
            total += cnt
            hp = c.path.replace(VIG, HIS)
            os.makedirs(os.path.dirname(hp), exist_ok=True)
            if not os.path.exists(hp):
                open(hp, 'w').write(f'# Historial — {c.head[0][2:]}\n\nRedacciones sustituidas o derogadas desde la base (PDF CNV actualizado a la RG 1094/2025). La más reciente va al final.\n')
            open(hp, 'a').write(f"\n## Reemplazo de expresiones ({descripcion})\n- Vigente hasta: {fstr(vigencia_rg(n) - dt.timedelta(days=1))}\n"
                                f"- Reemplazado por: {rg_id(n)}, art. {ordinal(art_rg)}\n- Ocurrencias reemplazadas en este archivo: {cnt}\n"
                                f"- Ubicaciones: {', '.join(afect)}\n- Texto anterior: idéntico al vigente salvo las expresiones reemplazadas"
                                f" ({'; '.join(f'«{a}» → «{b}»' for a, b in [(x.replace('\\b', ''), y) for x, y in pares])}).\n")
            c.pars.insert(0, nota(f'Expresiones reemplazadas en este archivo ({descripcion}; {cnt} ocurrencias)', n, art_rg))
            c.guardar(n)
            registrar(rel(c), ubic(c, f'{descripcion}: {", ".join(afect)}'), 'modifica parcialmente', n, art_rg)
    return total


def _clave_def(p):
    m = re.match(r'^“([^”]+)”', p)
    if m:
        return m.group(1).strip().lower()
    m = re.match(r'^([A-ZÁÉÍÓÚ][^“”]{1,80}?)\s+significa\s', p)
    return m.group(1).strip().lower() if m else None


def glosario(defs, tit='I', cap='II', num='2', n=None, art_rg=None, extra=''):
    """Incorpora o sustituye definiciones del glosario: si ya existe una definición con el mismo término inicial,
    la reemplaza (con sus párrafos de continuación); si no, la inserta en orden alfabético. Los párrafos que no
    empiezan con un término se consideran continuación de la definición anterior. Aplica y registra."""
    c = Cap(tit, cap)
    i, j = c.rango_art(num)
    existentes = {_clave_def(p) for p in c.pars[i:j] if _clave_def(p)}
    grupos = []
    for d in defs:
        if _clave_def(d) or not grupos:
            grupos.append([d])
        else:
            grupos[-1].append(d)
    nuevas = [g for g in grupos if _clave_def(g[0]) not in existentes]
    reempl = [g for g in grupos if _clave_def(g[0]) in existentes]

    def fn(pars):
        for g in reempl:
            k = _clave_def(g[0])
            idx = [x for x, p in enumerate(pars) if _clave_def(p) == k]
            assert len(idx) == 1, (k, idx)
            a = idx[0]; b = a + 1
            while b < len(pars) and not _clave_def(pars[b]) and not pars[b].startswith('['):
                b += 1
            pars = pars[:a] + list(g) + pars[b:]
        for g in nuevas:
            pars = termino_nuevo([g[0]])(pars)
            a = pars.index(g[0])
            pars = pars[:a + 1] + list(g[1:]) + pars[a + 1:]
        return pars

    nuevas_t = [g[0] for g in nuevas]
    reempl_t = [g[0] for g in reempl]
    def _t(x):
        m = re.match(r'^“([^”]+)”', x)
        return m.group(1) if m else re.match(r'^(.+?)\s+significa', x).group(1)
    nom = lambda ds: ', '.join('“' + _t(x) + '”' for x in ds)
    partes = []
    if nuevas_t:
        partes.append(('Término incorporado' if len(nuevas_t) == 1 else 'Términos incorporados') + ': ' + nom(nuevas_t))
    if reempl_t:
        partes.append(('Definición sustituida' if len(reempl_t) == 1 else 'Definiciones sustituidas') + ': ' + nom(reempl_t))
    txt = '; '.join(partes) + extra
    modificar_articulo(tit, cap, num, fn, n, art_rg, txt, det_extra=txt)
    return nuevas_t, reempl_t


def ultimo_parrafo(nuevos, reemplazar=True):
    """fn(pars): sustituye (o agrega después de, si reemplazar=False) el último párrafo del artículo, sin contar notas."""
    def fn(pars):
        k = len(pars) - 1
        while k > 0 and pars[k].startswith('['):
            k -= 1
        return pars[:k] + ([] if not reemplazar else []) + (list(nuevos) if reemplazar else [pars[k]] + list(nuevos)) + pars[k + 1:]
    return fn


def suprimir_terminos(claves, n, art_rg, tit='I', cap='II', num='2'):
    """Suprime definiciones del glosario (con sus párrafos de continuación)."""
    def fn(pars):
        for k in claves:
            idx = [x for x, p in enumerate(pars) if _clave_def(p) == k.lower()]
            assert len(idx) == 1, (k, idx)
            a = idx[0]; b = a + 1
            while b < len(pars) and not _clave_def(pars[b]) and not pars[b].startswith('['):
                b += 1
            pars = pars[:a] + pars[b:]
        return pars
    txt = ('Término suprimido' if len(claves) == 1 else 'Términos suprimidos') + ': ' + ', '.join(f'“{k}”' for k in claves)
    modificar_articulo(tit, cap, num, fn, n, art_rg, txt, det_extra=txt)


def suprimir_anexo(tit, cap, rom_, n, art_rg, verbo='suprimido'):
    c = Cap(tit, cap)
    i, j = rango_anexo(c, rom_)
    c._ctx = '\n'.join(p for p in c.pars if re.match(r'^\[(Capítulo|Título) ', p))
    historial(c, f'Anexo {rom_}', c.texto(i, j), n, art_rg, verbo.capitalize())
    c.pars[i:j] = [nota(f'Anexo {rom_} {verbo}', n, art_rg)]
    c.guardar(n)
    registrar(rel(c), ubic(c, f'Anexo {rom_}'), 'deroga', n, art_rg)

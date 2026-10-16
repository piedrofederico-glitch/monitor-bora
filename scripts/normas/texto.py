"""Conversión de texto extraído con `pdftotext -layout` a párrafos markdown.

Se usa tanto para el PDF base de las Normas como para los textos de las RG.
"""
import re

ART = re.compile(r'^(ART[ÍI]CULO|Art[íi]culo|ARTICULO)\s*\d+')
BREAK = [
    ART,
    re.compile(r'^SECCI[ÓO]N\s+[IVXLC]+\b'),
    re.compile(r'^CAP[ÍI]TULO\s+([IVXLC]+|PRELIMINAR)\b'),
    re.compile(r'^ANEXO\s+[IVXLC]+\b'),
    re.compile(r'^\(?[a-zñ]{1,2}\)\s'),
    re.compile(r'^\(?[a-zA-Z](\.\d{1,2})+[\.\)]\s'),
    re.compile(r'^\(?[ivxl]{1,6}[\.\)]\s'),
    re.compile(r'^\(?[A-Z]{1,2}\)\s'),
    re.compile(r'^\d{1,3}(\.\d{1,3})*\s?[\.\)\-–]+\s'),
    re.compile(r'^[•\-–·▪]\s'),
]
TERM = re.compile(r'([\.:;]["”’»)\]]*\.?-?|\.”\)?)\s*$')
EPI = re.compile(r'^[^a-zäëïöüáéíóúñ]{2,}$')
SOLO = re.compile(r'^(SECCI[ÓO]N|CAP[ÍI]TULO)\s+([IVXLC]+|PRELIMINAR)\.?$')
GAP = re.compile(r'\S {3,}\S')
CORTO = 83


def es_break(s):
    return any(p.match(s) for p in BREAK)


def bloques_tabla(lineas):
    """Marca renglones que forman parte de tablas: zonas con >=3 renglones con huecos internos."""
    n = len(lineas)
    gap = [bool(GAP.search(l.strip())) for l in lineas]
    tabla = [False] * n
    i = 0
    while i < n:
        if not gap[i]:
            i += 1; continue
        j = i; ult = i; cuenta = 1
        k = i + 1
        while k < n and k - ult <= 4:
            if gap[k]:
                ult = k; cuenta += 1
            k += 1
        if cuenta >= 3:
            for x in range(i, ult + 1): tabla[x] = True
            i = ult + 1
        else:
            i += 1
    return tabla


def a_markdown(lineas):
    """lineas: renglones (con espacios de layout), '' = renglón en blanco, None = salto de página.
    Devuelve lista de párrafos; las tablas salen como bloques ``` ."""
    tabla = bloques_tabla([l or '' for l in lineas])
    items = []   # (tipo, texto) tipo: 'l' renglón de prosa, 'b' blanco, 'p' salto pág, 't' tabla
    for l, t in zip(lineas, tabla):
        if l is None:
            items.append(('p', None))
        elif t:
            items.append(('t', l.rstrip()))
        elif not l.strip():
            items.append(('b', None))
        else:
            items.append(('l', l))
    # epígrafes en cadena
    prosa = [i for i, it in enumerate(items) if it[0] == 'l']
    epi = {}
    for a in range(len(prosa) - 1, -1, -1):
        i = prosa[a]; s = items[i][1].strip()
        nxt = items[prosa[a + 1]][1].strip() if a + 1 < len(prosa) else ''
        # entre el epígrafe y el artículo no puede haber renglón en blanco
        entre = [items[x][0] for x in range(i + 1, prosa[a + 1])] if a + 1 < len(prosa) else ['b']
        pegado = all(x == 'p' for x in entre)
        epi[i] = bool(EPI.match(s) and not ART.match(s) and not es_break(s) and nxt and pegado
                      and (ART.match(nxt) or epi.get(prosa[a + 1], False)))
    pars = []
    cur = None; cur_epi = False; cur_last = ''; tab = None; corte = False
    def cerrar():
        nonlocal cur, tab
        if cur is not None: pars.append((cur, cur_epi)); cur = None
        if tab is not None:
            # quitar sangría común
            ls = [x for x in tab if x.strip()]
            ind = min((len(x) - len(x.lstrip()) for x in ls), default=0)
            pars.append(('```\n' + '\n'.join(x[ind:] for x in tab).strip('\n') + '\n```', False)); tab = None
    for i, (tp, l) in enumerate(items):
        if tp == 'p':
            corte = True; continue
        if tp == 'b':
            if not corte:
                if tab is not None: tab.append('')
                elif cur is not None: cerrar()
            continue
        if tp == 't':
            if cur is not None: cerrar()
            if tab is None: tab = []
            tab.append(l); corte = False; continue
        if tab is not None: cerrar()
        s = re.sub(r'\s+', ' ', l.strip())
        e = epi.get(i, False)
        if cur is None:
            cur, cur_epi, cur_last = s, e, s; corte = False; continue
        partir = (es_break(s) or SOLO.fullmatch(cur_last) or (e and not cur_epi)
                  or (TERM.search(cur_last) and len(cur_last) < CORTO)
                  or (corte and TERM.search(cur_last))
                  or (EPI.match(cur_last) and not EPI.match(s) and len(cur_last) < 60 and cur_epi is False and not re.search(r'(,| DE| Y| DEL| LA| LOS| LAS| EN| A| O| E| AL| PARA| POR| CON)$', cur_last)))
        if e and cur_epi and not TERM.search(cur_last):
            partir = False
        if partir:
            cerrar(); cur, cur_epi = s, e
        else:
            cur = cur + ' ' + s
        cur_last = s; corte = False
    cerrar()
    out = []
    for p, e in pars:
        if out and ART.match(p) and out[-1][1]:
            out[-1] = (out[-1][0] + '\n' + p, False)
        else:
            out.append((p, e))
    return [p for p, _ in out]

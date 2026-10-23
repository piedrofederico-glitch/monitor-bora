import json, os, re
import normas as N


def expediente(n):
    p = f'{N.FUENTES}/{n}.txt'
    if not os.path.exists(p):
        return None
    t = re.sub(r'[ \t]+', ' ', open(p).read())
    m = re.search(r'Referencia:\s*(EX-\d{4}-\d+-\s*-?APN-[A-Z]+#CNV)', t) or re.search(r'Expediente N[°º]\s*(EX-\d{4}-\s?\d+-\s*-?APN-[A-Z]+#CNV)', t)
    return re.sub(r'\s+', ' ', m.group(1)) if m else None


def ubic_corta(e):
    """'Título VI, Capítulo I | art. 29 (Secc. IX)' -> 'Tít. VI, Cap. I, art. 29 (Secc. IX)'"""
    a, _, b = e['ubic'].partition(' | ')
    a = a.replace('Título ', 'Tít. ').replace('Capítulo ', 'Cap. ')
    return f'{a}, {b}' if b else a


def ficha(n, resumen, notas=(), vigencia=None, vigencia_txt=None, filas_extra=(), base=False, sin_normas=False):
    m = N.META[str(n)]
    if vigencia:
        N.VIGENCIAS[n] = vigencia
    vig = vigencia or N.fstr(N.fecha(m['bo']) + N.dt.timedelta(days=1))
    mods = [e for e in (json.load(open(N.MODS)) if os.path.exists(N.MODS) else []) if e['n'] == n]
    filas = [f"| {ubic_corta(e)} | {e['op']} | {e['art']} |" for e in mods] + list(filas_extra)
    firm = re.sub(r'\s*NOTA:.*$', '', m.get('firmantes') or '').strip()
    titulo = m['titulo_cnv'].strip('“”"')
    L = [f"# {N.rg_id(n)} — {titulo}", '',
         f"- **Número:** Resolución General {n}/{m['anio']}",
         f"- **Código GDE:** {m['gde']}",
         ]
    ex = expediente(n)
    if ex:
        L.append(f"- **Expediente:** {ex}")
    L += [f"- **Fecha de firma:** {m.get('firma_infoleg') or m.get('firma')}",
          f"- **Publicación en el BO:** {m['bo']}" + (f" a {m['bo_hasta']}" if m.get('bo_hasta') and m['bo_hasta'] != m['bo'] else '') + (f" (aviso N° {m['aviso_bo']})" if m.get('aviso_bo') else ''),
          f"- **Vigencia:** {vig}" + (f" ({vigencia_txt})" if vigencia_txt else ''),
          f"- **Firmantes:** {firm}",
          f"- **Categoría CNV:** {m['categoria']}",
          f"- **Fuentes:** [PDF CNV]({m['pdf_cnv']}) · [InfoLEG]({m['infoleg']})" if m.get('infoleg') else f"- **Fuentes:** [PDF CNV]({m['pdf_cnv']})",
          '', '## Resumen', ''] + [f'- {r}' for r in resumen] + ['', '## Afectaciones a las Normas', '']
    if base:
        L += ['Incorporada en la base: el PDF de `organismos/cnv/fuentes/` ya contiene su texto (ver `normas-cnv/base.md`).', '']
    if sin_normas:
        L += ['No modifica el texto de las Normas (N.T. 2013 y mod.).', '']
    L += ['| Ubicación en las Normas | Operación | Artículo de la RG |', '|---|---|---|'] + filas
    if notas:
        L += ['', '## Notas de consolidación', ''] + [f'- {x}' for x in notas]
    os.makedirs(N.RGDIR, exist_ok=True)
    open(f"{N.RGDIR}/RG-{n}-{m['anio']}.md", 'w').write('\n'.join(L) + '\n')


def ficha_consulta(n, resumen_extra=(), notas=()):
    """Ficha de una RG que somete un proyecto a Elaboración Participativa de Normas (no modifica las Normas)."""
    t = re.sub(r'\s+', ' ', open(f'{N.FUENTES}/{n}.txt').read())
    proy = re.search(r'adopción de una reglamentación sobre “(.*?)”, tomando', t)
    proy = proy.group(1) if proy else re.search(r'sobre “(.*?)”', t).group(1)
    anexo = re.search(r'Anexo I \((IF-[^)]*)\)', t)
    dire = re.search(r'Designar (a (?:las|los|la|el) .*?|al .*?) para dirigir', t)
    plazo = re.search(r'Fijar un plazo de (.*?) para', t)
    m = N.META[str(n)]
    vig = N.fstr(N.fecha(m.get('bo_hasta') or m['bo']) + N.dt.timedelta(days=1))
    res = [f"Somete a consulta pública (Elaboración Participativa de Normas, Decreto N° 1172/2003) el {proy.strip()}" + (f", cuyo texto es el Anexo I ({re.sub(r'APN-?(?=[A-Z]{2,5}#CNV)', 'APN-', anexo.group(1).replace(' ', ''))})." if anexo else '.'),
           (f"Designa {dire.group(1)} para dirigir el procedimiento." if dire else 'Designa a quien dirige el procedimiento.'),
           (f"Fija un plazo de {plazo.group(1)} para presentar opiniones y propuestas a través de www.argentina.gob.ar/cnv." if plazo else 'Fija el plazo para presentar opiniones y propuestas.'),
           'Aprueba el formulario para presentar opiniones (Anexo II).'] + list(resumen_extra)
    ficha(n, res, notas=['Es un proyecto sometido a consulta: no modifica las Normas. El texto definitivo, si se aprueba, llega por otra RG.'] + list(notas),
          vigencia=vig, vigencia_txt='desde el día siguiente a su última publicación en el BO', sin_normas=True)

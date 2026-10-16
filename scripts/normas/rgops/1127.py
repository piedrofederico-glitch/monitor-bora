import normas as N, fichas, re
n = 1127
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = N.definiciones(md(1))
assert len(defs) == 1
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Término “LPA” incorporado', det_extra='término “LPA”')

# --- Cap. III del Tít. II: cuerpo (art. 2°) y Anexos I a V (art. 3°)
c = N.Cap('II', 'III')
ax = N.anexos(c)
i_ax = ax[0][0]
i_vi = next(i for i, p in ax if p.startswith('### ANEXO VI'))
viejo_cuerpo = c.pars[:i_ax]
viejos_I_V = c.pars[i_ax:i_vi]
anexo_VI = c.pars[i_vi:]
c._ctx = ''
N.historial(c, 'Anexos I a V', '\n\n'.join(viejos_I_V), n, 3, 'Sustituidos')
N.historial(c, 'Título II, Capítulo III (cuerpo, sin anexos)', c.head[0] + '\n\n' + '\n\n'.join(viejo_cuerpo), n, 2, 'Sustituido')
(rom, nom, L), = N.dividir_capitulos(A[2]['citas'][0])
nuevos_ax = N.md(N.rg_anexo(n))
# fórmula publicada como imagen y fórmula D en dos renglones
k = next(i for i, p in enumerate(nuevos_ax) if p.startswith('La fórmula del porcentaje de retribuciones R es:'))
nuevos_ax.insert(k + 1, '[Fórmula publicada como imagen en el Anexo (IF-2026-35046005-APN-GAL#CNV); transcripción:] R = (−4.75 + √(22.5625 − 0.2D)) / −0.1 =')
k = next(i for i, p in enumerate(nuevos_ax) if p.startswith('(95 - % Remuneración Proyectada'))
nuevos_ax[k] = '```\n        (95 - % Remuneración Proyectada (1) ) * % Remuneración Proyectada\nD=\n                                       20\n```'
m = N.META[str(n)]
cuerpo = N.md(L) + [N.nota('Capítulo sustituido', n, 2)]
nota_vi = ('[Nota de consolidación: la RG 1127/2026 sustituyó el Capítulo (art. 2°) y los Anexos I a V (art. 3°) sin mencionar este Anexo VI, '
           'que se conserva. Su contenido (remuneraciones individuales) coincide con el nuevo Anexo V.]')
c.head = [f"# Título II — Capítulo III: {nom}", '', f"Fuente: {N.rg_id(n)}, arts. 2° y 3°; Anexo VI: PDF base."]
c.pars = cuerpo + nuevos_ax + [N.nota('Anexos I a V sustituidos', n, 3)] + anexo_VI + [nota_vi]
c.guardar(n)
N.registrar(N.rel(c), N.ubic(c, 'capítulo completo (sin anexos)'), 'sustituye', n, 2)
N.registrar(N.rel(c), N.ubic(c, 'Anexos I a V'), 'sustituye', n, 3)

# --- Cap. IV del Tít. II (art. 4°)
(rom, nom, L), = N.dividir_capitulos(A[4]['citas'][0])
N.sustituir_capitulo('II', 'IV', nom, N.md(L), n, 4)
# --- art. 5°: art. 1° de la Secc. I del Cap. I del Tít. XVI
N.sustituir_articulo('XVI', 'I', '1', md(5), n, 5, seccion='I')
fichas.ficha(n, [
    'Simplifica y sustituye los Capítulos III ("Órganos de administración y fiscalización. Auditoría externa") y IV ("Fiscalización societaria") del Título II.',
    'Sustituye los Anexos I a V del Cap. III: fórmulas de retribuciones al directorio, ficha individual de integrantes de órganos, notas de inscripción de auditores y asociaciones de profesionales, y planilla de remuneraciones individuales.',
    'Sustituye el art. 1° de la Secc. I del Cap. I del Tít. XVI: las notificaciones se rigen por el RLPA y los plazos por la LPA.',
    'Incorpora al glosario del Tít. I la sigla LPA (Ley de Procedimientos Administrativos N° 19.549).'],
    notas=['Los Anexos I a V se publicaron como documento IF separado (IF-2026-35046005-APN-GAL#CNV) a continuación de la resolución.',
           'La fórmula R del Anexo I está publicada como imagen: se transcribió y se dejó constancia.',
           'El Anexo VI del Cap. III (base) no fue sustituido ni derogado expresamente: se conservó con una nota; su contenido coincide con el nuevo Anexo V. Pendiente de confirmar con InfoLEG.'])

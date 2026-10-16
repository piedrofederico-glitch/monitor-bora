import normas as N, fichas
n = 1160
b = lambda k: N.md(N.bloque(n, k))
E = ('(…)', '(...)', '(…)".', '(…)”.')
C = ('V', 'III')
for k, blk in N.por_articulo(b(1)):
    N.sustituir_articulo(*C, k, blk, n, 1, seccion='I')
ps = [p for p in b(2) if p not in E and not N.clave_art(p) and p != '1. Portada:']
d = [p for p in ps if p.startswith('d) ')]; i3 = [p for p in ps if not p.startswith('d) ')]
assert len(d) == 1 and i3[0].startswith('3. ')
def f2(pars):
    pars = N.tramo('d) leyenda de inserción obligatoria', '2. Advertencias.', d)(pars)
    return N.tramo('3. Consideraciones de riesgo de la inversión.', '4. Resumen de los términos', i3)(pars)
N.modificar_articulo(*C, '4', f2, n, 2, 'Subinciso d) del inciso 1 e inciso 3 sustituidos', seccion='I', det_extra='inc. 1, subinc. d), e inc. 3')
ps = [p for p in b(3) if p not in E and not N.clave_art(p)]
N.modificar_articulo(*C, '5', N.tramo('1. Estados Contables anuales', '2. Estados Contables trimestrales', ps), n, 3, 'Inciso 1. sustituido', seccion='I', det_extra='inc. 1.')
N.sustituir_articulo(*C, '6', b(4), n, 4, seccion='I')
for k, blk in N.por_articulo(b(5)):
    N.sustituir_articulo(*C, k, blk, n, 5, seccion='I')
N.sustituir_articulo(*C, '20', b(6), n, 6, seccion='I')
ps = [p for p in b(7) if p not in E and not N.clave_art(p)]
assert len(ps) == 1
N.modificar_articulo(*C, '25', N.ultimo_parrafo(ps), n, 7, 'Último párrafo sustituido', seccion='II', det_extra='último párrafo')
N.sustituir_seccion(*C, 'III', b(8), n, 8)
N.sustituir_articulo('XVIII', 'III', '26', b(9), n, 9, seccion='XII')
fichas.ficha(n, [
    'Reformula el régimen de FCI cerrados (Cap. III del Tít. V): sustituye los arts. 1°, 2°, 6°, 10, 11 y 20 de la Secc. I, partes de los arts. 4° (leyenda de portada y consideraciones de riesgo del prospecto) y 5° (EECC anuales) y el último párrafo del art. 25 (Secc. II).',
    'Sustituye la Secc. III ("Oferta pública de cuotapartes de FCIC...", arts. 26 a 39), régimen de oferta pública automática de FCIC introducido por la RG 1148.',
    'Exige advertir en el prospecto cuando los colocadores no tengan asesores legales independientes de los del emisor.',
    'Prevé sanciones ante modificaciones reiteradas por errores imputables a las partes en documentación publicada bajo los regímenes automáticos.',
    'Sustituye el art. 26 de la Secc. XII del Cap. III del Tít. XVIII (trámites en curso).'])

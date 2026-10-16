import normas as N, fichas, re
n = 1159
b = lambda k: N.md(N.bloque(n, k))
sup = [re.match(r'^“([^”]+)”', p).group(1) for p in N.definiciones(b(1))]
assert len(sup) == 2
N.suprimir_terminos(sup, n, 1)
N.glosario(N.definiciones(b(2)), n=n, art_rg=2)
CAP = ('V', 'IV')
N.sustituir_seccion(*CAP, 'VII', b(3), n, 3)
N.sustituir_seccion(*CAP, 'VIII', b(4), n, 4)
for art, sec in ((5, 'IX'), (6, 'IX'), (7, 'X'), (8, 'XII'), (9, 'XVI'), (10, 'XVI'), (11, 'XVII')):
    for k, blk in N.por_articulo(b(art)):
        N.sustituir_articulo(*CAP, k, blk, n, art, seccion=sec)
N.sustituir_seccion(*CAP, 'XX', b(12), n, 12)
N.sustituir_seccion(*CAP, 'XXI', b(13), n, 13)
N.sustituir_seccion(*CAP, 'XXII', b(14), n, 14)
for s in ('XXIII', 'XXIV', 'XXV'):
    N.derogar_seccion(*CAP, s, n, 15, verbo='suprimida')
N.suprimir_anexo(*CAP, 'II', n, 15)
N.sustituir_articulo('V', 'V', '39', b(16), n, 16, seccion='VI')
for art, sec in ((17, 'I'), (18, 'IV'), (19, 'V'), (20, 'V')):
    for k, blk in N.por_articulo(b(art)):
        N.sustituir_articulo('V', 'VIII', k, blk, n, art, seccion=sec)
N.derogar_articulo('V', 'VIII', '20', n, 21, seccion='V', verbo='Suprimido')
N.sustituir_seccion('V', 'VIII', 'VI', b(22), n, 22)
N.incorporar_articulo('XVIII', 'II', b(23), n, 23, despues_de='3')
fichas.ficha(n, [
    'Simplifica y reordena los regímenes de oferta pública de fideicomisos financieros con autorización automática (Cap. IV del Tít. V): sustituye las Secciones VII, VIII, XX, XXI y XXII y suprime las Secciones XXIII, XXIV y XXV y el Anexo II.',
    'Sustituye los arts. 11 a 15 y 17 (Secc. IX), 20, 21 y 21 BIS (Secc. X), 28 (Secc. XII), 40 y 42 (Secc. XVI) y 45 (Secc. XVII) del Cap. IV; cuando una emisión reúne los requisitos de un régimen automático, debe tramitar por él.',
    'La información de los documentos de emisión en los regímenes automáticos es responsabilidad exclusiva del Fiduciario o Fiduciante; las modificaciones reiteradas por errores imputables a las partes pueden dar lugar a sanciones.',
    'Adapta los regímenes especiales: art. 39 del Cap. V; arts. 4°, 5°, 10, 13, 14 y 17 a 19 del Cap. VIII; suprime el art. 20 de la Secc. V y sustituye la Secc. VI (cese laboral) del Cap. VIII del Tít. V.',
    'En el glosario suprime los regímenes fiduciarios automáticos "por su Bajo Impacto" y "por su Mediano Impacto", sustituye dos definiciones, e incorpora el art. 4° del Cap. II del Tít. XVIII (trámites en curso).'],
    notas=['Antecedente: régimen de la RG 1146/2026 (consulta pública de la RG 1133/2026).',
           'Las secciones, el anexo y el artículo "suprimidos" se retiraron de vigente/ con una nota; su texto está en historial/.',
           'Tras suprimir el art. 20 de la Secc. V del Cap. VIII, la nueva Secc. VI vuelve a numerar sus artículos desde el 20: quedan dos "artículo 20" en el capítulo (uno como nota de supresión).'])

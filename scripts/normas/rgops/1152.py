import normas as N, fichas
n = 1152
N.VIGENCIAS[n] = '18/06/2026'
A = {a['num']: a for a in N.rg_articulos(n)}
b = lambda k: N.md(N.bloque(n, k))
sub = [p.rstrip('”.').rstrip('”') for p in b(1) if p.startswith('40)')]
assert len(sub) == 1
N.modificar_articulo('XV', 'I', '11', N.insertar_despues('39) AGE_026- Publicidad y/o Difusión.', sub), n, 1, 'Subinciso 40) del inciso K) incorporado', det_extra='inc. K), subinc. 40)')
N.sustituir_articulo('XVIII', 'V', '2', b(2), n, 2)
N.incorporar_articulo('XVIII', 'V', b(3), n, 3, despues_de='2')
N.incorporar_articulo('XVIII', 'V', b(4), n, 4, despues_de='27')
fichas.ficha(n, [
    'Sustituye el art. 2° del Cap. V del Tít. XVIII: plazos mínimos de tenencia para ventas de valores negociables con liquidación en moneda extranjera y transferencias a depositarias del exterior; excluye al FGS.',
    'Incorpora el art. 2° BIS del Cap. V del Tít. XVIII (no aplicable a los ALyC que sean entidades financieras).',
    'Extiende a los AN el formulario MUG_038 "Tenencias de Moneda Extranjera" (subinciso 40 del inc. K del art. 11, Cap. I, Tít. XV) e incorpora el art. 28 del Cap. V del Tít. XVIII: el régimen informativo comienza con julio de 2026, a remitir hasta el 10° día hábil de agosto de 2026.'],
    vigencia='18/06/2026', vigencia_txt='art. 5°: desde el día de su publicación en el BO',
    notas=['Los arts. 2° y 3° de la RG se publicaron como "Artículo" en minúscula; el texto citado de cada uno no cierra comillas y se extrajo como bloque hasta el artículo siguiente.'])

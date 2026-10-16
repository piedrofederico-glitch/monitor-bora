import normas as N, fichas
n = 1095
A = {a['num']: a for a in N.rg_articulos(n)}
for art in (1, 2):
    for rom, nom, L in N.dividir_capitulos(A[art]['citas'][0]):
        N.sustituir_capitulo('II', rom, nom, N.md(L), n, art)
for rom, L in N.dividir_secciones(A[3]['citas'][0]):
    N.incorporar_seccion('XVIII', 'I', N.md(L), n, 3)

fichas.ficha(n, [
    'Reescribe los Capítulos I (acciones y otros valores negociables), II (asambleas y reuniones de órganos sociales, modificaciones estatutarias, asambleas a distancia) y V a X (oferta pública primaria, PyMEs, entidades de garantía, emisoras extranjeras y CEDEAR/CEVA, prospecto y reorganización societaria) del Título II.',
    'Elimina el Régimen de Valores Representativos de Deuda de Corto Plazo (VCP), el de estímulo para cooperativas con fines productivos, el de financiamiento de proyectos y otros regímenes automáticos, y unifica la PyME CNV Garantizada con la oferta pública con autorización automática de ON por su bajo impacto.',
    'Suprime la nómina de Entidades de Garantía del Cap. VII del Tít. II, el prospecto resumido y la notificación por fax; reduce informes especiales de contador o abogado.',
    'Admite la representación digital de valores negociables (art. 12, Secc. II, Cap. I, Tít. XXII) y expresa en UVA el patrimonio neto mínimo para emisores de CEDEAR y CEVA.',
    'Agrega las Secciones IV y V del Cap. I del Tít. XVIII: las emisiones PyME CNV Garantizadas y VCP anteriores siguen con el régimen vigente al emitirse hasta su cancelación.'],
    notas=['Los Capítulos III y IV del Título II no se modificaron.',
           'Cada capítulo se reemplazó completo; la redacción anterior está en historial/titulo-II/ (un bloque por capítulo).'])

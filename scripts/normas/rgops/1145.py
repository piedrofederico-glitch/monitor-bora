import normas as N, fichas
n = 1145
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.glosario(N.definiciones(md(1)), n=n, art_rg=1)
N.glosario(N.definiciones(md(2)), n=n, art_rg=2)
N.sustituir_articulo('II', 'V', '82', md(3), n, 3, seccion='XI')
N.sustituir_articulo('II', 'V', '96', md(4), n, 4, seccion='XI')
N.incorporar_seccion('II', 'V', md(5), n, 5)
fichas.ficha(n, [
    'Crea la "Oferta Pública de Valores Negociables con Autorización Automática por su Mediano Impacto Ampliado" (nueva Secc. XVIII del Cap. V del Tít. II, arts. 153 y ss.), para ON y acciones con montos mayores.',
    'Las Emisoras que usen los montos ampliados quedan sujetas desde la colocación al régimen informativo pleno del Régimen General, y pueden dirigir la oferta a inversores minoristas.',
    'Sustituye los arts. 82 (definición del régimen de ON por su mediano impacto) y 96 (opciones de las PyME CNV y PyME CNV Garantizada) de la Secc. XI.',
    'Sustituye la definición de "Inversor Calificado" del glosario (agrega que la condición puede acreditarse por DDJJ del inversor) e incorpora la del nuevo régimen ampliado.'],
    notas=['Antecedente: consulta pública de la RG 1132/2026.',
           'El PDF publicado por la CNV es una imagen escaneada sin texto: se usó el texto publicado en el Boletín Oficial (edición del 11/06/2026), cotejado con InfoLEG.'])

import normas as N, fichas
n = 1158
N.VIGENCIAS[n] = '10/08/2026'
N.incorporar_seccion('XI', None, N.md(N.bloque(n, 1)), n, 1)
fichas.ficha(n, [
    'Incorpora la Secc. VI al Tít. XI (arts. 18 y 19): los requerimientos de información o documentación de la CNV en investigaciones o supervisión en materia de PLA/FT/FP se rigen por el RLPA.',
    'Admite cursar esos requerimientos por correo electrónico a los Oficiales de Cumplimiento y a los demás sujetos registrados, a los domicilios electrónicos declarados en la AIF.'],
    vigencia='10/08/2026', vigencia_txt='art. 2°')

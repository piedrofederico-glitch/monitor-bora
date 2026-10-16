import normas as N, fichas
n = 1173
N.VIGENCIAS[n] = '15/10/2026'
b = lambda k: N.md(N.bloque(n, k))
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
ps = b(2); assert ps[0] == 'CAPÍTULO V'
N.sustituir_capitulo('XII', 'V', ps[1], ps[2:], n, 2)
N.incorporar_anexo('XII', 'V', b(3), n, 3)
ps = b(4); assert ps[0] == 'CAPÍTULO XVIII'
N.sustituir_capitulo('XVIII', 'XVIII', ps[1].rstrip('.'), ps[2:], n, 4, nota_tipo='Capítulo incorporado')
fichas.ficha(n, [
    'Sustituye el Cap. V del Tít. XII, que pasa a denominarse “Registro de Idóneos y Examen de Idoneidad”: Sección I (Registro de Idóneos) y Sección II (Examen de Idoneidad), con un nuevo esquema en el que el examen lo administran entidades reconocidas por la CNV, bajo su supervisión.',
    'Incorpora el Anexo I del Cap. V del Tít. XII: Protocolo para el reconocimiento y supervisión de entidades administradoras del Examen de Idoneidad.',
    'Incorpora al glosario (art. 2°, Cap. II, Tít. I) los términos “Idóneo” y “Registro de Idóneos”.',
    'Incorpora el Cap. XVIII del Tít. XVIII (disposiciones transitorias): la CNV sigue tomando el examen hasta el 15/12/2026 inclusive (sólo postulantes con VEP abonado a la entrada en vigencia de la RG 1173) y, en todo caso, hasta que estén operativas las primeras entidades administradoras; conserva la validez de los exámenes rendidos.'],
    vigencia='15/10/2026', vigencia_txt='art. 5°: desde el día de su publicación en el BO')

import normas as N, fichas
n = 1097
A = {a['num']: a for a in N.rg_articulos(n)}
L = A[1]['citas'][0]
caps = [(r, nom, N.md(x)) for r, nom, x in N.dividir_capitulos(L)]
assert [c[0] for c in caps] == ['I', 'II'], caps
N.sustituir_titulo('I', caps, n, 1)
N.derogar_seccion('XVI', 'I', 'I', n, 2)
N.renumerar_seccion('XVI', 'I', 'II', 'I', n, 3)
N.renumerar_seccion('XVI', 'I', 'III', 'II', n, 3)
fichas.ficha(n, [
    'Sustituye el Título I ("Disposiciones preliminares"), que pasa a tener dos capítulos: I, "Comisión Nacional de Valores. Ámbito de aplicación", y II, "Definiciones generales e interpretación".',
    'El Cap. II reúne referencias normativas (Secc. I), un glosario de términos definidos aplicable a todas las Normas (Secc. II) y reglas de interpretación de expresiones (Secc. III).',
    'Deroga la Secc. I ("Definición y alcance de términos") del Cap. I del Tít. XVI, reemplazada por el nuevo glosario del Tít. I.',
    'Renumera las Secciones II (notificaciones) y III (otras disposiciones) del Cap. I del Tít. XVI como I y II.'],
    notas=['El Título I de la base no tenía capítulos (vigente/titulo-I/titulo-I.md). Se reemplazó por vigente/titulo-I/capitulo-I.md y capitulo-II.md; el texto anterior está en historial/titulo-I/titulo-I.md.'])

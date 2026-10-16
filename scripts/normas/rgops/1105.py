import normas as N, fichas
n = 1105
A = {a['num']: a for a in N.rg_articulos(n)}
defin = N.md(A[1]['citas'][1])
assert defin[0].startswith('“PyME CNV” significa'), defin
N.modificar_articulo('I', 'II', '2', N.parrafo('“PyME CNV” significa', defin), n, 1, 'Término “PyME CNV” sustituido',
                     det_extra='término “PyME CNV”')
N.incorporar_articulo('V', 'VIII', N.md(A[2]['citas'][0]), n, 2, despues_de='8', seccion='II')
fichas.ficha(n, [
    'Sustituye la definición de "PyME CNV" del glosario (art. 2°, Secc. II, Cap. II, Tít. I): suma, para los PIC, a las entidades con Certificado MiPyME vigente no alcanzadas por las restricciones del art. 2° del Cap. VI del Tít. II.',
    'Incorpora el art. 8° BIS a la Secc. II del Cap. VIII del Tít. V: admite dispensar la identificación de fiduciantes en programas globales de FF para el desarrollo inmobiliario (art. 5°, Secc. II, Cap. V) o con activos hipotecarios.',
    'Exige que el prospecto delimite el objeto de los fideicomisos o la naturaleza del activo subyacente.'])

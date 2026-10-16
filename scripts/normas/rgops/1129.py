import normas as N, fichas
n = 1129
A = {a['num']: a for a in N.rg_articulos(n)}
defs = [d for d in N.definiciones(N.md(A[1]['citas'][0])) if d not in ('“(…)',)]
assert len(defs) == 5, defs
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1,
                     'Términos “Documento de Oferta Preliminar”, “Documento de Oferta Definitivo” y de los Regímenes de Autorización Automática incorporados',
                     det_extra='5 términos (documentos de oferta y regímenes automáticos)')
for k, blk in N.por_articulo(N.md(A[2]['citas'][0])):
    N.sustituir_articulo('II', 'IX', k, blk, n, 2, seccion='II')
fichas.ficha(n, [
    'Sustituye los arts. 8° a 10 de la Secc. II del Cap. IX del Tít. II (prospecto y suplemento de prospecto preliminar).',
    'Permite distribuir prospectos, suplementos u otros documentos de oferta preliminares antes de la autorización de la CNV (cuando se exija) o antes de la notificación, publicación en la AIF o inicio del período de difusión.',
    'En los regímenes de autorización automática o sin autorización previa exige adaptar la leyenda, indicar el régimen en los documentos de oferta preliminar y definitivo y cumplir las obligaciones de información.',
    'Admite reuniones informativas presenciales o virtuales, en el país o en el exterior, antes de la autorización, notificación o publicación de la oferta.',
    'Incorpora al glosario del Tít. I "Documento de Oferta Preliminar", "Documento de Oferta Definitivo" y tres denominaciones genéricas de regímenes de autorización automática.'],
    notas=['La cita del art. 1° abre con comillas sobre una elipsis ("“(…)"); se omitió ese marcador y se incorporaron las cinco definiciones.'])

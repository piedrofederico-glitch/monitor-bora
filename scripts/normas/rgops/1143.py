import normas as N, fichas
n = 1143
A = {a['num']: a for a in N.rg_articulos(n)}
N.incorporar_seccion('V', 'VII', N.md(A[1]['citas'][0]), n, 1)
fichas.ficha(n, [
    'Incorpora la Secc. VII al Cap. VII del Tít. V (arts. 17 a 29): régimen de FCI abiertos ETF ("FCIA ETF"), que replican mediante gestión pasiva un índice financiero o bursátil (art. 1°, tercer párrafo, de la Ley de FCI).',
    'Fija criterios para el índice de referencia, la denominación "FCIA ETF", los participantes (Participantes Autorizados y creadores de mercado), el objeto y las exclusiones.',
    'Admite préstamo de valores en cartera hasta el 30% del patrimonio neto y suscripción e integración en dinero o en especie según condiciones de la Sociedad Gerente.',
    'Exige reglamento de gestión tipo con cláusulas adicionales, prospecto de emisión, publicación diaria de la cartera y permite la representación digital de cuotapartes (Tít. XXII).'],
    notas=['Antecedente: consulta pública de la RG 1124/2026.'])

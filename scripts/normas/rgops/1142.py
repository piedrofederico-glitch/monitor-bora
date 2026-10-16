import normas as N, fichas
n = 1142
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
nuevas, reempl = N.glosario(N.definiciones(md(1)), n=n, art_rg=1)
for rom, L in N.dividir_secciones(A[2]['citas'][0]):
    assert rom in ('II', 'III', 'IV')
    N.sustituir_seccion('II', 'VIII', rom, N.md(L), n, 2)
for rom, L in N.dividir_secciones(A[3]['citas'][0]):
    N.incorporar_seccion('II', 'VIII', N.md(L), n, 3)
N.incorporar_anexo('II', 'VIII', md(4), n, 4)
fichas.ficha(n, [
    'Sustituye las Secciones II, III y IV del Cap. VIII del Tít. II: disposiciones comunes a CEDEAR y CEVA, específicas para CEDEAR (subyacentes emitidos y negociados en el exterior) y específicas para CEVA (subyacentes de residentes con oferta pública).',
    'Habilita CEVA que funcionen como productos cotizados (ETP) respaldados por canastas de activos, con Participantes Autorizados y creadores de mercado, y elimina la distinción regulatoria entre CEDEAR patrocinados y no patrocinados.',
    'Restringe la emisión de CEDEAR y CEVA a entidades supervisadas con capacidad operativa y solvencia, con requisitos específicos para fiduciarios financieros.',
    'Incorpora las Secciones V (Certificados de Depósito en Custodia, ADR), VI (aplicación supletoria) y VII (otras disposiciones) y el Anexo I (requisitos mínimos del prospecto de CEDEAR o CEVA).',
    'En el glosario del Tít. I agrega ' + ', '.join(x.split('”')[0] + '”' for x in nuevas) + ' y sustituye ' + ', '.join(x.split('”')[0] + '”' for x in reempl) + '.'],
    notas=['Antecedente: consulta pública de la RG 1123/2026.',
           'El art. 1° dice "Incorporar", pero algunas definiciones ya existían ("CEVA", "IOSCO", "Programa de CEDEAR o CEVA"): se reemplazaron por la nueva redacción y la anterior quedó en historial/.'])

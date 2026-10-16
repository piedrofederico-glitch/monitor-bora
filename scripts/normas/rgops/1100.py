import normas as N, fichas
n = 1100
A = {a['num']: a for a in N.rg_articulos(n)}
(rom, nom, L), = N.dividir_capitulos(A[1]['citas'][0])
assert rom == 'IV'
N.sustituir_capitulo('VI', 'IV', nom, N.md(L), n, 1)
fichas.ficha(n, [
    'Sustituye completo el Cap. IV ("Colocación primaria") del Tít. VI.',
    'Busca reducir cargas y costos en los procesos de colocación, en especial en emisiones con colocación simultánea en el exterior, y articularlos con estándares internacionales.',
    'Revisa la información que se suministra a la CNV sobre la colocación, preservando transparencia y trazabilidad.'])

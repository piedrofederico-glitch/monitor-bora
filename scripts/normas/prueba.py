"""Prueba de las herramientas: reaplica una RG sobre el estado anterior y compara con el commit original.

Uso (desde la raíz del repo):
    python3 scripts/normas/prueba.py            # RG 1172/2026 (sustitución de capítulo, glosario, inciso, artículo nuevo)
    python3 scripts/normas/prueba.py 1169 1150  # otras RG con script en scripts/normas/rgops/

Para cada RG busca el commit "normas-cnv: aplica RG <n>/..." en git, extrae a una carpeta temporal el estado
anterior de organismos/cnv/, corre rgops/<n>.py sobre esa copia y compara vigente/, historial/,
modificaciones.md, INDICE.md y la ficha con lo que quedó en ese commit. No toca el repo.
Sale con código 0 si todo coincide.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..'))


def git(*a):
    return subprocess.run(['git', '-C', REPO, *a], capture_output=True, text=True, check=True).stdout


def commit_de(n):
    log = git('log', '--format=%h %s', '--grep', f'aplica RG {n}/').splitlines()
    log = [l for l in log if f'aplica RG {n}/' in l and 'revierte' not in l]
    if not log:
        sys.exit(f'No encuentro el commit de la RG {n}')
    return log[0].split()[0]


def probar(n):
    c = commit_de(n)
    tmp = tempfile.mkdtemp(prefix=f'prueba-rg{n}-')
    try:
        tar = subprocess.run(['git', '-C', REPO, 'archive', f'{c}^', 'organismos/cnv'], capture_output=True, check=True).stdout
        subprocess.run(['tar', '-x', '-C', tmp], input=tar, check=True)
        # insumos actuales: textos de las RG, metadatos y títulos
        shutil.copytree(f'{REPO}/organismos/cnv/rg/fuentes', f'{tmp}/organismos/cnv/rg/fuentes', dirs_exist_ok=True)
        os.makedirs(f'{tmp}/organismos/cnv/normas-cnv/datos', exist_ok=True)
        shutil.copy(f'{REPO}/organismos/cnv/normas-cnv/datos/titulos.json', f'{tmp}/organismos/cnv/normas-cnv/datos/')
        # modificaciones.json: las entradas anteriores a la RG, sin campos agregados después
        mods = json.load(open(f'{REPO}/organismos/cnv/normas-cnv/datos/modificaciones.json'))
        k = next(i for i, e in enumerate(mods) if e['n'] == n)
        campos = ('archivo', 'ubic', 'op', 'n', 'rg', 'art', 'bo')
        prev = [{x: e[x] for x in campos} for e in mods[:k]]
        json.dump(prev, open(f'{tmp}/organismos/cnv/normas-cnv/datos/modificaciones.json', 'w'), ensure_ascii=False, indent=1)
        env = dict(os.environ, NORMAS_REPO=tmp, PYTHONPATH=AQUI)
        r = subprocess.run([sys.executable, f'{AQUI}/rgops/{n}.py'], cwd=AQUI, env=env, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout, r.stderr)
            return False
        subprocess.run([sys.executable, '-c', 'import indice; indice.generar()'], cwd=AQUI, env=env, check=True)
        # comparar los archivos que tocó el commit original
        cambiados = git('diff', '--name-only', f'{c}^', c, '--', 'organismos/cnv/normas-cnv', 'organismos/cnv/rg').split()
        cambiados = [f for f in cambiados if not f.endswith('base.md')]
        ok = True
        for f in cambiados:
            esperado = subprocess.run(['git', '-C', REPO, 'show', f'{c}:{f}'], capture_output=True, text=True).stdout
            p = f'{tmp}/{f}'
            obtenido = open(p).read() if os.path.exists(p) else None
            if obtenido != esperado:
                ok = False
                print(f'  DIFIERE: {f}')
        print(f'RG {n} (commit {c}): {len(cambiados)} archivos comparados — {"OK" if ok else "CON DIFERENCIAS"}')
        return ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    ns = [int(x) for x in sys.argv[1:]] or [1172]
    res = [probar(n) for n in ns]
    sys.exit(0 if all(res) else 1)

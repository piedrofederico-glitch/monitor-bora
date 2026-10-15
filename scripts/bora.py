#!/usr/bin/env python3
"""Descarga la primera sección del Boletín Oficial y separa lo relevante.

Uso: python3 scripts/bora.py [--fecha AAAAMMDD]

- Normas de los organismos de config/organismos.json -> organismos/<slug>/normas/
- Normas con palabras clave de config/temas.json     -> temas/textos/ + temas/candidatos/<fecha>.md
- Resumen de la corrida                              -> runs/<fecha>.json
"""
import argparse
import base64
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.parse
import urllib.request

BASE = "https://www.boletinoficial.gob.ar"
UA = "Mozilla/5.0 (monitor-bora)"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def http(url, data=None, intentos=4):
    body = urllib.parse.urlencode(data).encode() if data else None
    hdr = {"User-Agent": UA}
    if data:
        hdr["X-Requested-With"] = "XMLHttpRequest"
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, data=body, headers=hdr)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # red inestable: reintento con backoff
            if i == intentos - 1:
                raise
            print(f"  reintento {url}: {e}", file=sys.stderr)
            time.sleep(2 ** (i + 1))


def html_a_texto(fragmento):
    t = re.sub(r"<style.*?</style>", "", fragmento, flags=re.S)
    t = re.sub(r"<br\s*/?>|</p>|</tr>|</h\d>", "\n", t)
    t = re.sub(r"</td>", " | ", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    t = re.sub(r"[ \t\xa0]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n\n", t).strip()


def pdf_a_texto(pdf):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf)
        f.flush()
        try:
            return subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True,
                                  text=True, check=True).stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            from pypdf import PdfReader
            return "\n".join(p.extract_text() or "" for p in PdfReader(f.name).pages)


def listar_avisos(fecha):
    h = http(f"{BASE}/seccion/primera/{fecha}").decode("utf-8", "replace")
    avisos, rubro = [], None
    patron = re.compile(
        r'<h5 class="seccion-rubro[^>]*>([^<]*)<'
        r'|href="/detalleAviso/primera/(\d+)/(\d+)"[^>]*>\s*<div class="linea-aviso">\s*'
        r'<p class="item">([^<]*)</p>(.*?)</div>', re.S)
    for m in patron.finditer(h):
        if m.group(1) is not None:
            rubro = html.unescape(m.group(1)).strip()
            continue
        idav, f, org, resto = m.group(2), m.group(3), m.group(4), m.group(5)
        if f != fecha or "ANTERIOR" in (rubro or "").upper():
            continue  # avisos de ediciones previas que siguen publicándose
        smalls = [html.unescape(x).strip() for x in re.findall(r"<small>([^<]*)</small>", resto)]
        avisos.append({
            "id": idav, "fecha": fecha, "rubro": rubro,
            "organismo": html.unescape(org).strip(),
            "titulo": smalls[0] if smalls else "",
            "codigo": smalls[1] if len(smalls) > 1 else "",
            "url": f"{BASE}/detalleAviso/primera/{idav}/{fecha}",
        })
    return avisos


def detalle(av):
    h = http(av["url"] + "?anexos=1").decode("utf-8", "replace")
    i = h.find('id="cuerpoDetalleAviso"')
    j = h.find('id="anexosDiv"', i)
    cuerpo = h[i:j if j > 0 else i + 400000]
    cuerpo = cuerpo[cuerpo.find(">") + 1:]
    texto = html_a_texto(cuerpo)
    texto = re.split(r"\n\s*Fecha de publicaci[oó]n", texto)[0].strip()
    av["texto"] = texto
    av["firmantes"] = extraer_firmantes(texto)
    av["anexos"] = []
    for nro, idanexo, fpub in re.findall(
            r'descargarPDFAnexo\("primera",\s*"(\d+)",\s*"(\d+)",\s*"(\d+)"', h):
        try:
            d = json.loads(http(f"{BASE}/pdf/download_anexo", {
                "seccion": "primera", "nroAnexo": nro, "idAnexo": idanexo,
                "fechaPublicacion": fpub}))
            av["anexos"].append({"nro": nro, "texto": pdf_a_texto(base64.b64decode(d["pdfBase64"]))})
        except Exception as e:
            av["anexos"].append({"nro": nro, "texto": "", "error": str(e)})
    return av


def extraer_firmantes(texto):
    """Última línea con contenido antes de la marca 'e. dd/mm/aaaa N°'."""
    corte = re.search(r"\n\s*e\.\s*\d{2}/\d{2}/\d{4}\s*N", texto)
    previas = [l.strip() for l in texto[:corte.start() if corte else len(texto)].splitlines() if l.strip()]
    previas = [l for l in previas if not re.match(r"(NOTA\b|ANEXOS?\s*$|El/Los Anexo|La documentaci[oó]n no publicada)", l, re.I)]
    return previas[-1] if previas else ""


def clasificar_organismo(av, cfg):
    org = norm(av["organismo"])
    cod = av["codigo"]
    hallados = []
    for slug, c in cfg.items():
        por_org = any(re.search(norm(p), org) for p in c.get("organismo_regex", []))
        por_cod = any(re.search(p, cod) for p in c.get("codigo_regex", []))
        if not (por_org or por_cod):
            continue
        req = c.get("requiere_texto_regex")
        if req:
            # Si el título ya dice qué es (p. ej. Comunicación "C"), manda el título; si es genérico
            # ("Aviso Oficial"), se mira el comienzo del texto.
            titulo = norm(av["titulo"])
            fuente = titulo if titulo.startswith("comunicacion") else titulo + "\n" + norm(av.get("texto", "")[:1500])
            if not any(re.search(norm(p), fuente) for p in req):
                continue
        hallados.append(slug)
    return hallados


def buscar_temas(av, temas):
    """Prefijos de patrón: titulo:, codigo:, rubro:, dispositivo: (texto posterior a RESUELVE/DECRETA/
    DISPONE). Sin prefijo, busca en organismo + título + texto + anexos."""
    full = norm("\n".join([av["organismo"], av["titulo"], av["codigo"], av.get("texto", "")] +
                          [a["texto"] for a in av.get("anexos", [])]))
    texto = norm(av.get("texto", ""))
    cortes = list(re.finditer(r"\b(resuelve|resuelven|decreta|dispone|disponen|decide)\s*:", texto))
    ambitos = {
        "titulo": norm(av["titulo"]), "codigo": norm(av["codigo"]), "rubro": norm(av["rubro"] or ""),
        "dispositivo": texto[cortes[-1].end():] if cortes else texto,
    }
    hits = {}
    for tema, pats in temas.items():
        if tema.startswith("_"):
            continue
        for p in pats:
            ambito, _, regex = p.partition(":") if p.split(":")[0] in ambitos else ("", "", p)
            objetivo = ambitos.get(ambito, full)
            m = re.search(regex, objetivo, re.M)
            if m:
                ini = max(0, m.start() - 160)
                frag = re.sub(r"\s+", " ", objetivo[ini:m.end() + 160])
                hits.setdefault(tema, []).append({"patron": p, "fragmento": frag})
    return hits


def slug_archivo(av):
    t = re.sub(r"[^a-z0-9]+", "-", norm(av["titulo"]))[:60].strip("-") or "aviso"
    return f"{av['fecha']}_{av['id']}_{t}"


def md_norma(av, extra=""):
    f = av["fecha"]
    partes = [
        "---",
        f"id: {av['id']}",
        f"fecha_publicacion: {f[:4]}-{f[4:6]}-{f[6:]}",
        f"rubro: {av['rubro']}",
        f"organismo: {json.dumps(av['organismo'], ensure_ascii=False)}",
        f"titulo: {json.dumps(av['titulo'], ensure_ascii=False)}",
        f"codigo: {json.dumps(av['codigo'], ensure_ascii=False)}",
        f"firmantes: {json.dumps(av['firmantes'], ensure_ascii=False)}",
        f"url: {av['url']}",
        extra.rstrip(),
        "---", "",
        f"# {av['organismo']} — {av['titulo']}", "",
        av["texto"], "",
    ]
    for a in av.get("anexos", []):
        partes += [f"## Anexo {a['nro']}", "", a.get("error") and f"(no se pudo descargar: {a['error']})"
                   or a["texto"].strip(), ""]
    return "\n".join(p for p in partes if p is not None)


def escribir(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).strftime("%Y%m%d"))
    fecha = ap.parse_args().fecha
    orgs = json.load(open(os.path.join(RAIZ, "config/organismos.json"), encoding="utf-8"))
    temas = json.load(open(os.path.join(RAIZ, "config/temas.json"), encoding="utf-8"))

    avisos = listar_avisos(fecha)
    print(f"{fecha}: {len(avisos)} avisos en la primera sección")
    resumen = {"fecha": fecha, "total_avisos": len(avisos), "organismos": {k: [] for k in orgs},
               "temas_candidatos": []}

    for av in avisos:
        detalle(av)
        rel = {"id": av["id"], "organismo": av["organismo"], "titulo": av["titulo"],
               "codigo": av["codigo"], "firmantes": av["firmantes"], "url": av["url"]}
        for slug in clasificar_organismo(av, orgs):
            ruta = f"organismos/{slug}/normas/{slug_archivo(av)}.md"
            escribir(os.path.join(RAIZ, ruta), md_norma(av))
            resumen["organismos"][slug].append({**rel, "archivo": ruta})
        hits = buscar_temas(av, temas)
        if hits:
            ruta = f"temas/textos/{slug_archivo(av)}.md"
            extra = "temas_prima_facie: " + json.dumps(sorted(hits), ensure_ascii=False)
            escribir(os.path.join(RAIZ, ruta), md_norma(av, extra))
            resumen["temas_candidatos"].append({**rel, "archivo": ruta, "temas": hits})

    lineas = [f"# Candidatos por tema — {fecha[6:]}/{fecha[4:6]}/{fecha[:4]}", "",
              "Filtro automático por palabras clave, sin análisis. El Analista de Temas confirma o descarta.", ""]
    for c in resumen["temas_candidatos"]:
        lineas += [f"## {c['organismo']} — {c['titulo']}", f"- Texto: `{c['archivo']}`", f"- Fuente: {c['url']}"]
        for tema, hs in c["temas"].items():
            lineas.append(f"- **{tema}**: " + "; ".join(f"`{h['patron']}` → «…{h['fragmento']}…»" for h in hs[:3]))
        lineas.append("")
    if not resumen["temas_candidatos"]:
        lineas.append("Sin candidatos.")
    escribir(os.path.join(RAIZ, f"temas/candidatos/{fecha}.md"), "\n".join(lineas))
    escribir(os.path.join(RAIZ, f"runs/{fecha}.json"), json.dumps(resumen, ensure_ascii=False, indent=2))

    for slug, items in resumen["organismos"].items():
        print(f"  {slug}: {len(items)}" + "".join(f"\n    - {i['titulo']} ({i['firmantes']})" for i in items))
    print(f"  temas candidatos: {len(resumen['temas_candidatos'])}")
    for c in resumen["temas_candidatos"]:
        print(f"    - {c['organismo']} | {c['titulo']} | {', '.join(c['temas'])}")


if __name__ == "__main__":
    main()

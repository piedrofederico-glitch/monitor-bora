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


PDF_ARSAT = "https://s3.arsat.com.ar/cdn-bo-001/pdf-del-dia/primera.pdf"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
         "octubre", "noviembre", "diciembre"]
RUBROS = ["Decretos", "Decisiones Administrativas", "Resoluciones", "Resoluciones Generales",
          "Resoluciones Conjuntas", "Resoluciones Sintetizadas", "Disposiciones", "Disposiciones Conjuntas",
          "Disposiciones Sintetizadas", "Comunicaciones", "Avisos Oficiales", "Acordadas", "Leyes",
          "Decretos Sintetizados", "Concursos Oficiales", "Convenciones Colectivas de Trabajo"]


def avisos_desde_pdf(fecha, ruta_pdf=None):
    """Respaldo: el sitio del BORA corta las conexiones desde la nube, pero el PDF del día que publica
    ARSAT responde. Solo contiene la edición del día (se pisa al día siguiente). Cada aviso va entre
    marcas #I<n>I# y #F<n>F#; ese n NO es el id de /detalleAviso, así que el link apunta a la sección del día. No trae los anexos publicados solo en la web."""
    pdf = open(ruta_pdf, "rb").read() if ruta_pdf else http(PDF_ARSAT)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf)
        f.flush()
        txt = subprocess.run(["pdftotext", f.name, "-"], capture_output=True, text=True, check=True).stdout
    d = dt.date(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:]))
    if f"{d.day} de {MESES[d.month - 1]} de {d.year}" not in norm(txt[:400]):
        return []  # el PDF todavía es de la edición anterior
    # encabezado de página: "BOLETÍN OFICIAL Nº 36.018 - Primera Sección / 7 / Jueves 22 de octubre de 2026"
    txt = re.sub(r"\n*BOLET[IÍ]N OFICIAL N[ºo°] [\d.]+ - Primera Secci[oó]n\s*\n+\s*\d+\s*\n+\s*\w+ \d+ de \w+ de \d{4}\s*\n",
                 "\n", txt)
    ddmm = f"{fecha[6:]}/{fecha[4:6]}/{fecha[:4]}"
    avisos, rubro, pos = [], None, 0
    # la marca "e. dd/mm/aaaa N°" a veces queda pegada a la línea anterior (firmante o URL)
    txt = re.sub(r"[ \t]*(e\.\s*\d{2}/\d{2}/\d{4}\s*N[°º])", r"\n\1", txt)
    for m in re.finditer(r"#I(\d+)I#(.*?)#F\1F#", txt, re.S):
        org = []  # el organismo puede quedar antes de la marca #I
        for linea in txt[pos:m.start()].splitlines():
            linea = linea.strip()
            if linea in RUBROS:
                rubro, org = linea, []
            elif (re.search(r"[A-ZÁÉÍÓÚÑ]{3}", linea) and not re.search(r"[a-záéíóúñ]", linea)
                  and not linea.startswith("#") and linea not in ("NUEVOS", "ANTERIORES")):
                org.append(linea)
        pos = m.end()
        idav, cuerpo = m.group(1), m.group(2)
        marca = re.search(r"e\.\s*(\d{2}/\d{2}/\d{4})\s*N", cuerpo)
        if marca and marca.group(1) != ddmm:
            continue  # aviso de una edición anterior que se sigue publicando
        lineas = [l.strip() for l in cuerpo.strip().splitlines()]
        i = 0
        while i < len(lineas):  # organismo: líneas en mayúsculas al comienzo
            l = lineas[i]
            if l and (re.search(r"[a-záéíóúñ]", l) or re.match(r"(COMUNICACI|RESOLUCI|DISPOSICI|DECRETO)", l)):
                break
            if l:
                org.append(l)
            i += 1
        titulo = codigo = ""
        if i < len(lineas) and re.match(r"(Resoluci|Disposici|Decreto|Decisi|Comunicaci|Ley|Acordada)", lineas[i]):
            titulo, i = lineas[i], i + 1
            if i < len(lineas) and re.match(r"[A-Z]+-\d{4}-\d+-", lineas[i]):
                codigo, i = lineas[i], i + 1
        texto = re.sub(r"\n{3,}", "\n\n", "\n".join(lineas[i:])).strip()
        if not titulo:  # avisos oficiales: el título real va en el texto (p. ej. Comunicación "A")
            titulo = next((l for l in lineas[i:i + 3] if l), "")[:120]
        avisos.append({
            "id": idav, "fecha": fecha, "rubro": rubro, "organismo": " - ".join(org),
            "titulo": titulo, "codigo": codigo, "url": f"{BASE}/seccion/primera/{fecha}",
            "texto": texto, "firmantes": extraer_firmantes(texto), "anexos": [], "fuente": "pdf-arsat",
        })
    return avisos


def obtener_avisos(fecha, ruta_pdf=None):
    """Sitio web primero; si no responde, PDF de ARSAT (solo sirve para la edición de hoy)."""
    if not ruta_pdf:
        try:
            return listar_avisos(fecha), "web"
        except Exception as e:
            print(f"{fecha}: sitio del BORA inaccesible ({e}); uso el PDF de ARSAT", file=sys.stderr)
    return avisos_desde_pdf(fecha, ruta_pdf), "pdf-arsat"


def detalle(av):
    if av.get("fuente") == "pdf-arsat":
        return av  # el texto ya viene del PDF
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
    previo = texto[:corte.start() if corte else len(texto)]
    # la NOTA sobre anexos va después del firmante y puede ocupar varias líneas (PDF)
    nota = re.search(r"\n\s*(NOTA\b|El/[Ll]os [Aa]nexo|La documentaci[oó]n no publicada)", previo[-1500:])
    if nota:
        previo = previo[:len(previo) - 1500 + nota.start()] if len(previo) > 1500 else previo[:nota.start()]
    previas = [l.strip() for l in previo.splitlines() if l.strip()]
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
    ap.add_argument("--esperar-minutos", type=int, default=0,
                    help="si la edición todavía no está publicada, reintenta cada 5 min hasta este plazo")
    ap.add_argument("--pdf", help="procesar un PDF de la primera sección ya descargado (respaldo ARSAT)")
    args = ap.parse_args()
    fecha = args.fecha
    orgs = json.load(open(os.path.join(RAIZ, "config/organismos.json"), encoding="utf-8"))
    temas = json.load(open(os.path.join(RAIZ, "config/temas.json"), encoding="utf-8"))

    limite = time.time() + args.esperar_minutos * 60
    avisos, fuente = obtener_avisos(fecha, args.pdf)
    while not avisos and time.time() < limite:
        print(f"{fecha}: edición sin publicar todavía, reintento en 5 minutos", file=sys.stderr)
        time.sleep(300)
        avisos, fuente = obtener_avisos(fecha, args.pdf)
    print(f"{fecha}: {len(avisos)} avisos en la primera sección (fuente: {fuente})")
    resumen = {"fecha": fecha, "fuente": fuente, "total_avisos": len(avisos),
               "organismos": {k: [] for k in orgs}, "temas_candidatos": []}
    if fuente == "pdf-arsat":
        resumen["nota"] = "Descargado del PDF del día de ARSAT: sin anexos publicados solo en la web."

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

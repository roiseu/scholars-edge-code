import requests

HEADERS = {"User-Agent": "ScholarsEdge/1.0 (mailto:you@university.edu)"}

def doi_to_bibtex(doi):
    """Ask doi.org for a BibTeX entry using content negotiation."""
    r = requests.get(f"https://doi.org/{doi}",
                     headers={**HEADERS, "Accept": "application/x-bibtex"}, timeout=20)
    r.raise_for_status()
    return r.text

def fetch_metadata(doi):
    r = requests.get(f"https://api.crossref.org/works/{doi}", headers=HEADERS, timeout=20)
    r.raise_for_status()
    m = r.json()["message"]
    return {
        "authors": [(a.get("given", ""), a.get("family", "")) for a in m.get("author", [])],
        "year": m.get("issued", {}).get("date-parts", [[None]])[0][0],
        "title": (m.get("title") or [""])[0],
        "journal": (m.get("container-title") or [""])[0],
        "volume": m.get("volume", ""), "issue": m.get("issue", ""),
        "pages": m.get("page", ""), "doi": doi,
    }

def initials(given):
    return " ".join(p[0] + "." for p in given.replace("-", " ").split() if p)

def format_apa(meta):
    names = [f"{fam}, {initials(giv)}" for giv, fam in meta["authors"]]
    if len(names) == 1:
        au = names[0]
    elif len(names) <= 20:
        au = ", ".join(names[:-1]) + ", & " + names[-1]
    else:                                   # APA 7: first 19, ellipsis, last author
        au = ", ".join(names[:19]) + ", ... " + names[-1]
    vol = meta["volume"] + (f"({meta['issue']})" if meta["issue"] else "")
    pages = f", {meta['pages']}" if meta["pages"] else ""
    return (f"{au} ({meta['year']}). {meta['title']}. {meta['journal']}, "
            f"{vol}{pages}. https://doi.org/{meta['doi']}")

def format_ieee(meta, number):
    names = [f"{initials(giv)} {fam}" for giv, fam in meta["authors"]]
    if len(names) > 6:                      # IEEE: first author et al. beyond six
        au = names[0] + " et al."
    elif len(names) > 2:
        au = ", ".join(names[:-1]) + ", and " + names[-1]
    else:
        au = " and ".join(names)
    parts = [f'[{number}] {au}, "{meta["title"]}," {meta["journal"]}']
    if meta["volume"]: parts.append(f"vol. {meta['volume']}")
    if meta["issue"]:  parts.append(f"no. {meta['issue']}")
    if meta["pages"]:  parts.append(f"pp. {meta['pages']}")
    parts.append(str(meta["year"]))
    return ", ".join(parts) + f", doi: {meta['doi']}."

doi = "10.1038/sdata.2016.18"
print(doi_to_bibtex(doi))
meta = fetch_metadata(doi)
print(format_apa(meta))
print(format_ieee(meta, 1))

import time
import requests
import pandas as pd
import xml.etree.ElementTree as ET

API = "https://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}

def fetch_arxiv(query, max_results=200, batch=50):
    """Fetch paper metadata from arXiv with pagination and polite delays."""
    papers = []
    for start in range(0, max_results, batch):
        params = {"search_query": f"all:{query}", "start": start,
                  "max_results": min(batch, max_results - start),
                  "sortBy": "submittedDate", "sortOrder": "descending"}
        try:
            r = requests.get(API, params=params, timeout=30)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed at offset {start}: {e}")
            break
        root = ET.fromstring(r.content)
        entries = root.findall("atom:entry", NS)
        if not entries:
            break
        for e in entries:
            papers.append({
                "id": e.find("atom:id", NS).text.rsplit("/", 1)[-1],
                "title": " ".join(e.find("atom:title", NS).text.split()),
                "abstract": " ".join(e.find("atom:summary", NS).text.split()),
                "published": e.find("atom:published", NS).text[:10],
                "categories": ",".join(c.get("term", "")
                                       for c in e.findall("atom:category", NS)),
            })
        print(f"Fetched {len(papers)} records")
        time.sleep(3)   # arXiv asks for at least 3 seconds between requests
    return pd.DataFrame(papers)

df = fetch_arxiv("federated learning intrusion detection", max_results=200)
df.to_csv("data/raw/arxiv_papers.csv", index=False)

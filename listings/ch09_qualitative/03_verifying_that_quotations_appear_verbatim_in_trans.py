import re
from pathlib import Path

def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

transcripts = {p.stem: normalize(p.read_text(encoding="utf-8"))
               for p in Path("transcripts").glob("*.txt")}   # files: P01.txt, P02.txt...

quotes = [
    ("P03", "after the third false alarm in one night I stopped believing it"),
    ("P07", "the dashboard is basically a slot machine"),
]

for pid, quote in quotes:
    found = normalize(quote) in transcripts.get(pid, "")
    print(f"[{'OK' if found else 'NOT FOUND'}] {pid}: {quote}")

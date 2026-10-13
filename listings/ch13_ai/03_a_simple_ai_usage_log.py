import json
import datetime
from pathlib import Path

LOG_FILE = Path("ai_usage_log.jsonl")

def log_ai_use(tool, stage, purpose, output_used, verified_how):
    """Append one AI interaction to the log (one JSON object per line)."""
    entry = {
        "date": datetime.date.today().isoformat(),
        "tool": tool,                  # e.g. "Claude", "Elicit", "Claude Code"
        "stage": stage,                # e.g. "literature", "analysis", "writing"
        "purpose": purpose,            # what you asked it to do
        "output_used": output_used,    # how (or whether) you used the result
        "verified_how": verified_how,  # how you checked it
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def draft_disclosure():
    """Turn the log into a starting point for a disclosure statement."""
    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    uses = {}
    for e in (json.loads(line) for line in lines):
        uses.setdefault(e["tool"], set()).add(e["purpose"])
    parts = [f"{tool} ({'; '.join(sorted(p))})" for tool, p in uses.items()]
    return ("During the preparation of this work the author(s) used "
            + ", ".join(parts)
            + ". All outputs were reviewed, verified, and edited by the author(s), "
              "who take full responsibility for the content of the publication.")

log_ai_use("Elicit", "literature", "screen abstracts against inclusion criteria",
           "shortlist of 42 papers, all read in full by the author", "full-text check")
log_ai_use("Claude Code", "analysis", "refactor preprocessing into an sklearn Pipeline",
           "code merged after line-by-line review", "unit tests and full re-run")
print(draft_disclosure())

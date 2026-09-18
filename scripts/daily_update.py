import json
from pathlib import Path
from datetime import datetime, timezone

DB = Path("songs.json")
QUEUE = Path("update_queue.json")
LOG = Path("update_log.json")
LIMIT = 100

db = json.loads(DB.read_text(encoding="utf-8"))
q = json.loads(QUEUE.read_text(encoding="utf-8"))

existing = {str(x["number"]) for x in db.get("songs", [])}
add = []
remain = []

def valid(x):
    try:
        n = int(x["number"])
    except Exception:
        return False

    in_range = (1 <= n <= 558) or (1001 <= n <= 2999)

    # Human voice is intentionally NOT checked.
    # Exact video-number matching is intentionally NOT checked.
    return (
        in_range
        and bool(str(x.get("title", "")).strip())
        and bool(str(x.get("videoUrl", "")).strip())
        and x.get("lyrics") == "embedded"
        and x.get("verified") is True
    )

for x in q.get("songs", []):
    if valid(x) and str(x["number"]) not in existing and len(add) < LIMIT:
        item = dict(x)
        item["status"] = "영상 등록"
        add.append(item)
        existing.add(str(item["number"]))
    else:
        remain.append(x)

db["songs"].extend(add)
db["songs"].sort(key=lambda x: int(x["number"]))
DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")

QUEUE.write_text(
    json.dumps(
        {"description": q.get("description", ""), "songs": remain},
        ensure_ascii=False, indent=2
    ),
    encoding="utf-8"
)

log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {"updates": []}
log.setdefault("updates", []).append({
    "utc": datetime.now(timezone.utc).isoformat(),
    "added": len(add)
})
LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

print("added:", len(add))

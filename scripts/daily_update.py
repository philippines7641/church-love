import json
from pathlib import Path
from datetime import datetime, timezone

DB = Path("songs.json")
QUEUE = Path("update_queue.json")
LOG = Path("update_log.json")
LIMIT = 100

def load(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

db = load(DB, {"songs": []})
q = load(QUEUE, {"songs": []})
existing = {str(x.get("number")) for x in db.get("songs", [])}

def is_verified(x):
    try:
        n = int(x.get("number"))
    except Exception:
        return False
    return (
        x.get("verified") is True and
        x.get("vocal") == "none" and
        x.get("lyrics") == "embedded" and
        x.get("embeddable") is True and
        bool(x.get("videoUrl")) and
        ((1 <= n <= 558) or (1001 <= n <= 2999))
    )

added=[]
remain=[]
for x in q.get("songs", []):
    if is_verified(x) and str(x.get("number")) not in existing and len(added) < LIMIT:
        item=dict(x)
        item["status"]="검증 완료"
        item["updatedAt"]=datetime.now(timezone.utc).isoformat()
        added.append(item)
        existing.add(str(x.get("number")))
    else:
        remain.append(x)

db["songs"].extend(added)
db["songs"].sort(key=lambda x: int(x["number"]))
DB.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding="utf-8")
QUEUE.write_text(json.dumps({"description":q.get("description", ""),"songs":remain},ensure_ascii=False,indent=2),encoding="utf-8")

log=load(LOG,{"runs":[]})
log["runs"].append({
    "runAt":datetime.now(timezone.utc).isoformat(),
    "added":len(added),
    "numbers":[x["number"] for x in added]
})
log["runs"]=log["runs"][-90:]
LOG.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"verified songs added: {len(added)}")

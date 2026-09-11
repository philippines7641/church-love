import json
from pathlib import Path

db_path=Path("songs.json")
queue_path=Path("update_queue.json")
db=json.loads(db_path.read_text(encoding="utf-8"))
queue=json.loads(queue_path.read_text(encoding="utf-8"))

existing={str(x["number"]) for x in db["songs"]}
added=[]
remaining=[]

for x in queue.get("songs",[]):
    ok=(x.get("verified") is True
        and x.get("vocal")=="none"
        and x.get("lyrics")=="embedded"
        and x.get("embeddable") is True
        and bool(x.get("videoUrl")))
    if ok and str(x["number"]) not in existing and len(added)<100:
        added.append(x)
        existing.add(str(x["number"]))
    else:
        remaining.append(x)

db["songs"].extend(added)
db["songs"].sort(key=lambda x:int(x["number"]))
db_path.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding="utf-8")
queue_path.write_text(json.dumps({"description":queue.get("description",""),"songs":remaining},ensure_ascii=False,indent=2),encoding="utf-8")
print("Added",len(added),"verified songs.")

import json
from pathlib import Path

db = Path('songs.json')
qf = Path('update_queue.json')
limit = 100

d = json.loads(db.read_text(encoding='utf-8'))
q = json.loads(qf.read_text(encoding='utf-8'))
existing = {str(x['number']) for x in d['songs']}
add, remain = [], []
for x in q.get('songs', []):
    try:
        n = int(x['number'])
    except Exception:
        n = -1
    ok = (
        x.get('verified') is True and
        x.get('vocal') == 'none' and
        x.get('lyrics') == 'embedded' and
        x.get('embeddable') is True and
        bool(x.get('videoUrl')) and
        ((1 <= n <= 558) or (1001 <= n <= 2999))
    )
    if ok and str(n) not in existing and len(add) < limit:
        add.append(x)
        existing.add(str(n))
    else:
        remain.append(x)

d['songs'].extend(add)
d['songs'].sort(key=lambda x: int(x['number']))
db.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
qf.write_text(json.dumps({'description': q.get('description', ''), 'songs': remain}, ensure_ascii=False, indent=2), encoding='utf-8')
print('added', len(add))

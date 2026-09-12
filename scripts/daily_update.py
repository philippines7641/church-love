import json
from pathlib import Path
from datetime import datetime, timezone

DB = Path('songs.json')
QUEUE = Path('update_queue.json')
LOG = Path('update_log.json')
LIMIT = 100


def load(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


db = load(DB, {'songs': []})
q = load(QUEUE, {'songs': []})
log = load(LOG, {'updates': []})

existing = {str(x.get('number')) for x in db.get('songs', [])}
added = []
remaining = []

for x in q.get('songs', []):
    try:
        n = int(x['number'])
    except Exception:
        n = -1

    verified = (
        x.get('verified') is True and
        x.get('vocal') == 'none' and
        x.get('lyrics') == 'embedded' and
        x.get('embeddable') is True and
        bool(x.get('videoUrl')) and
        ((1 <= n <= 558) or (1001 <= n <= 2999))
    )

    if verified and str(n) not in existing and len(added) < LIMIT:
        item = dict(x)
        item['status'] = '검증완료'
        added.append(item)
        existing.add(str(n))
    else:
        remaining.append(x)

if added:
    db.setdefault('songs', []).extend(added)
    db['songs'].sort(key=lambda x: int(x['number']))
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding='utf-8')

QUEUE.write_text(json.dumps({
    'description': '실제 확인된 영상만 대기열에 넣습니다. 검증된 만큼만 하루 최대 100곡씩 누적됩니다.',
    'songs': remaining
}, ensure_ascii=False, indent=2), encoding='utf-8')

now = datetime.now(timezone.utc).isoformat()
log.setdefault('updates', []).append({
    'utc': now,
    'added': len(added),
    'numbers': [x['number'] for x in added]
})
LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding='utf-8')

print(f'검증 완료 영상 {len(added)}곡 추가')

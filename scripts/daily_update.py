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

existing_numbers = {str(x.get('number')) for x in db.get('songs', [])}
existing_titles = {str(x.get('title','')).strip().casefold() for x in db.get('songs', [])}
added = []
remaining = []

for x in q.get('songs', []):
    try:
        n = int(x.get('number'))
    except Exception:
        n = -1

    title = str(x.get('title','')).strip()
    verified = (
        x.get('verified') is True and
        x.get('vocal') == 'none' and
        x.get('lyrics') == 'embedded' and
        x.get('embeddable') is True and
        bool(x.get('videoUrl')) and
        bool(title) and
        ((1 <= n <= 558) or (1001 <= n <= 2999))
    )

    # 제목이 이미 DB에 있으면 중복 추가하지 않습니다.
    # 즉 영상에 '1번'이라고 쓰여 있지 않아도 제목으로 연결됩니다.
    if verified and str(n) not in existing_numbers and title.casefold() not in existing_titles and len(added) < LIMIT:
        item = dict(x)
        item['status'] = '검증완료'
        added.append(item)
        existing_numbers.add(str(n))
        existing_titles.add(title.casefold())
    elif verified and len(added) >= LIMIT:
        remaining.append(x)
    elif not verified:
        remaining.append(x)

if added:
    db.setdefault('songs', []).extend(added)
    db['songs'].sort(key=lambda x: int(x.get('number', 0)))
    db['version'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding='utf-8')

QUEUE.write_text(json.dumps({
    'description': '제목으로 연결된 실제 검증 영상만 하루 최대 100곡씩 누적합니다.',
    'songs': remaining
}, ensure_ascii=False, indent=2), encoding='utf-8')

log.setdefault('updates', []).append({
    'utc': datetime.now(timezone.utc).isoformat(),
    'added': len(added),
    'numbers': [x.get('number') for x in added],
    'titles': [x.get('title') for x in added]
})
LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'검증 완료 영상 {len(added)}곡 추가')

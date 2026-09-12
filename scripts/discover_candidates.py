import json, subprocess
from pathlib import Path

DB = Path('songs.json')
CAND = Path('candidate_queue.json')
LIMIT = 30

def load(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))

db = load(DB, {'songs': []})
cand = load(CAND, {'songs': []})

# 곡 번호가 영상 제목에 반드시 들어갈 필요는 없습니다.
# DB의 제목을 기준으로 YouTube 후보를 찾습니다.
waiting_titles = {str(x.get('title','')).strip().casefold() for x in cand.get('songs', [])}
waiting_titles.discard('')

songs = [
    x for x in db.get('songs', [])
    if not x.get('verified') and str(x.get('title','')).strip().casefold() not in waiting_titles
]

out = list(cand.get('songs', []))

for song in songs[:LIMIT]:
    number = song.get('number')
    title = str(song.get('title','')).strip()
    if not title:
        continue

    # 번호가 아니라 '곡 제목'을 중심으로 검색합니다.
    # 후보 검색어에는 반주/가사/무보컬 계열 표현을 사용하지만
    # 자동으로 검증 완료 처리하지 않습니다.
    query = f'"{title}" 반주 가사'
    try:
        p = subprocess.run(
            ['yt-dlp', '--flat-playlist', '--dump-single-json', f'ytsearch8:{query}'],
            capture_output=True, text=True, timeout=60
        )
        data = json.loads(p.stdout) if p.stdout else {}
        entries = data.get('entries') or []
    except Exception:
        entries = []

    for e in entries:
        vid = e.get('id')
        candidate_title = e.get('title','')
        if not vid:
            continue
        low = str(candidate_title).casefold()
        if any(k in low for k in ['반주', 'instrumental', 'inst', 'mr', '가사', 'lyrics']):
            out.append({
                'number': number,
                'title': title,
                'videoUrl': f'https://www.youtube.com/watch?v={vid}',
                'candidateTitle': candidate_title,
                'verified': False,
                'vocal': 'unknown',
                'lyrics': 'unknown',
                'embeddable': 'unknown',
                'status': '검증 필요'
            })
            break

# 같은 제목/곡은 후보 하나만 유지합니다. 번호보다 제목을 우선 식별자로 사용합니다.
seen = set()
dedup = []
for x in out:
    key = str(x.get('title','')).strip().casefold()
    if key and key not in seen:
        seen.add(key)
        dedup.append(x)

CAND.write_text(
    json.dumps({
        'description': '곡 번호가 영상 제목에 없어도 됩니다. DB의 곡 제목으로 후보를 찾고, 실제 확인 전에는 절대 검증 완료 처리하지 않습니다.',
        'songs': dedup
    }, ensure_ascii=False, indent=2),
    encoding='utf-8'
)
print('title-based candidates:', len(dedup))

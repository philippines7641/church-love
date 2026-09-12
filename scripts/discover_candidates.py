import json, re, subprocess
from pathlib import Path

DB = Path('songs.json')
CAND = Path('candidate_queue.json')
LIMIT = 30

db = json.loads(DB.read_text(encoding='utf-8'))
candidates = json.loads(CAND.read_text(encoding='utf-8')) if CAND.exists() else {'songs': []}
existing = {str(x.get('number')) for x in db.get('songs', [])}
existing |= {str(x.get('number')) for x in candidates.get('songs', [])}

songs = [x for x in db.get('songs', []) if str(x.get('number')) not in existing]
# songs.json initially contains all songs, so use entries without a verified video.
songs = [x for x in db.get('songs', []) if not x.get('verified') and str(x.get('number')) not in {str(y.get('number')) for y in candidates.get('songs', [])}]

out = candidates.get('songs', [])
for song in songs[:LIMIT]:
    n = int(song['number'])
    title = song['title']
    if not ((1 <= n <= 558) or (1001 <= n <= 2999)):
        continue
    query = f'"{title}" "통일찬송가 {n}" 반주 가사' if n <= 558 else f'"{title}" 찬송가 반주 가사'
    try:
        p = subprocess.run(['yt-dlp','--flat-playlist','--dump-single-json',f'ytsearch5:{query}'],capture_output=True,text=True,timeout=45)
        data = json.loads(p.stdout) if p.stdout else {}
        entries = data.get('entries', [])
    except Exception:
        entries = []
    for e in entries:
        vid = e.get('id')
        title2 = e.get('title','')
        if not vid: continue
        low = title2.lower()
        # Discovery only. Never mark verified automatically.
        if any(k in low for k in ['mr','반주','inst','instrumental','가사']):
            out.append({
                'number': n, 'title': title, 'videoUrl': f'https://www.youtube.com/watch?v={vid}',
                'candidateTitle': title2, 'verified': False, 'vocal': 'unknown',
                'lyrics': 'unknown', 'embeddable': 'unknown', 'status': '검증 필요'
            })
            break

# de-duplicate by number, preserve first candidate
seen=set(); dedup=[]
for x in out:
    k=str(x['number'])
    if k not in seen:
        seen.add(k); dedup.append(x)
CAND.write_text(json.dumps({'description':'자동 검색 후보. 실제 영상 확인 전에는 절대 songs.json으로 반영하지 않습니다.','songs':dedup},ensure_ascii=False,indent=2),encoding='utf-8')
print('candidates', len(dedup))

import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

API_KEY = os.environ.get("YOUTUBE_API_KEY", "").strip()
DB = Path("songs.json")
DAILY_LIMIT = 100

if not API_KEY:
    raise SystemExit("YOUTUBE_API_KEY secret is missing.")

data = json.loads(DB.read_text(encoding="utf-8"))
songs = data.get("songs", [])


def search_youtube(query):
    params = urllib.parse.urlencode({
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 10,
        "videoEmbeddable": "true",
        "key": API_KEY,
    })
    url = "https://www.googleapis.com/youtube/v3/search?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "Church-Love-Bot/2.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("items", [])


def clean(text):
    return re.sub(r"[^0-9A-Za-z가-힣 ]+", " ", text or "").lower().split()


def choose_video(song, items):
    number = str(song.get("number", ""))
    category = song.get("category", "")
    title = song.get("title", "")
    # Current DB contains placeholder titles such as '통일찬송가 1번'.
    # Prefer results that contain the hymn number and useful accompaniment/lyrics terms.
    useful = ["반주", "가사", "피아노", "mr", "inst", "accompaniment", "lyrics"]
    ranked = []
    for item in items:
        vid = item.get("id", {}).get("videoId")
        sn = item.get("snippet", {})
        vt = sn.get("title", "")
        if not vid:
            continue
        score = 0
        low = vt.lower()
        if number and re.search(rf"(?<!\d){re.escape(number)}\s*(번|장)?(?!\d)", vt):
            score += 8
        if category and category in vt:
            score += 4
        for word in useful:
            if word in low:
                score += 2
        # If a real title exists later, reward title-word overlap.
        title_words = [w for w in clean(title) if len(w) >= 2 and w not in {"통일찬송가", "복음성가"}]
        score += sum(1 for w in title_words if w in clean(vt)) * 3
        ranked.append((score, vid, vt))
    if not ranked:
        return None
    ranked.sort(key=lambda x: (-x[0], x[2]))
    return ranked[0]


checked = 0
added = 0
errors = 0

for song in songs:
    if checked >= DAILY_LIMIT:
        break
    if song.get("videoUrl"):
        continue

    checked += 1
    number = song.get("number")
    category = song.get("category", "")
    title = song.get("title", "")

    queries = [
        f'"{title}" 반주 가사',
        f'{category} {number}번 반주 가사',
        f'{category} {number}번',
    ]

    found = None
    try:
        for q in queries:
            items = search_youtube(q)
            found = choose_video(song, items)
            if found:
                break
    except Exception as exc:
        errors += 1
        print(f"YouTube API error at #{number}: {exc}")
        continue

    if found:
        score, vid, video_title = found
        song["videoUrl"] = f"https://www.youtube.com/watch?v={vid}"
        song["foundVideoTitle"] = video_title
        song["status"] = "자동 검색"
        added += 1
        print(f"ADDED #{number}: {video_title}")
    else:
        print(f"NOT FOUND #{number}")

DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"checked={checked} added={added} errors={errors}")

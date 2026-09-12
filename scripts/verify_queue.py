import json
from pathlib import Path

SRC = Path('verified_sources.json')
OUT = Path('update_queue.json')

def load(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))

src = load(SRC, {'songs': []})
verified = []
for x in src.get('songs', []):
    # 번호는 영상에서 확인할 필요가 없습니다.
    # 이 파일에 등록하는 번호는 Church Love 내부 DB 번호입니다.
    ok = (
        x.get('verified') is True and
        x.get('vocal') == 'none' and
        x.get('lyrics') == 'embedded' and
        x.get('embeddable') is True and
        bool(x.get('videoUrl')) and
        bool(x.get('title'))
    )
    if ok:
        verified.append(x)

OUT.write_text(
    json.dumps({
        'description': '실제로 확인된 영상만 넣습니다. 번호가 영상에 없어도 제목이 DB 곡과 같으면 해당 Church Love 번호로 등록됩니다.',
        'songs': verified
    }, ensure_ascii=False, indent=2),
    encoding='utf-8'
)
print('verified ready:', len(verified))

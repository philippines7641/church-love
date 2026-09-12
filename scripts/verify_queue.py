import json
from pathlib import Path

SRC=Path('candidate_queue.json')
OUT=Path('update_queue.json')
if not SRC.exists():
    raise SystemExit('candidate_queue.json not found')
d=json.loads(SRC.read_text(encoding='utf-8'))
verified=[]; pending=[]
for x in d.get('songs',[]):
    ok=(x.get('verified') is True and x.get('vocal')=='none' and x.get('lyrics')=='embedded' and x.get('embeddable') is True and bool(x.get('videoUrl')))
    (verified if ok else pending).append(x)
OUT.write_text(json.dumps({'description':'검증 완료된 영상만 자동 반영 대기열입니다.','songs':verified},ensure_ascii=False,indent=2),encoding='utf-8')
print('verified ready',len(verified),'pending',len(pending))

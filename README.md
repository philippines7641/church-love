# Church Love

## 영상 등록 원칙

통일찬송가 1~558번과 복음성가 1001~2999번을 대상으로 합니다. 새찬송가는 사용하지 않습니다.

영상은 다음 조건을 모두 실제 확인한 경우에만 `update_queue.json`에 등록합니다.

- 반주 음악
- 가사/자막 표시
- 사람의 노래 음성 없음
- YouTube 임베드 가능
- 실제 재생 확인
- 번호와 곡 제목 일치

검증되지 않은 영상을 자동으로 골라 넣지 않습니다.

## 매일 자동 누적

GitHub Actions가 매일 00:00 UTC, 한국시간 오전 9시에 실행됩니다.

그날 검증 완료된 곡이 10곡이면 10곡, 30곡이면 30곡만 추가합니다. 최대 100곡이며, 100곡을 채우기 위해 검증되지 않은 영상을 넣지 않습니다.

`update_queue.json`에 검증 완료 항목이 없으면 아무 곡도 추가하지 않습니다.

## GitHub 업로드 구조

```text
index.html
style.css
app.js
songs.json
update_queue.json
update_log.json
README.md
scripts/daily_update.py
.github/workflows/daily-update.yml
```

주의: 이 프로그램은 저작권 영상을 다운로드하거나 재배포하지 않고 YouTube 영상을 임베드하여 사용합니다.

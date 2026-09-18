# Church Love

교회 예배용 찬송가 검색 및 영상 재생 프로젝트입니다.

## 번호 체계

- 통일찬송가: 1~558
- 복음성가: 1001~2999
- 새찬송가: 제외

## 영상 등록 기준

1. 곡 제목이 일치하면 Church Love 번호로 연결합니다.
2. YouTube 영상 URL이 있어야 합니다.
3. 영상에 가사 또는 자막이 확인되어야 합니다.
4. 사람의 노래 음성 포함 여부는 제외 조건이 아닙니다.
5. 영상 제목에 Church Love 번호가 반드시 들어갈 필요가 없습니다.

## GitHub Pages

`index.html`, `style.css`, `app.js`, `songs.json`을 같은 위치에 두면 됩니다.

## 자동 업데이트

`update_queue.json`에 실제 확인된 항목을 넣으면 GitHub Actions가 하루 최대 100개씩 `songs.json`에 누적합니다.

주의: GitHub Actions가 스스로 YouTube 영상을 찾아 확인하는 기능은 아닙니다. 실제 영상 URL과 가사/자막 확인이 끝난 항목을 대기열에 넣어야 합니다.

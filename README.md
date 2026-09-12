# Church Love

교회 반주기 형태의 찬송가 검색/재생용 웹 프로젝트입니다.

## 이번 수정 사항
- 검색 문구: `찬송가 제목 또는 번호를 입력해 주세요.`
- 번호 검색과 제목 부분검색을 모두 지원합니다.
- 통일찬송가: 1~558
- 복음성가: 1001~2999
- 새찬송가는 데이터베이스에서 제외했습니다.
- 초기 데이터는 통일찬송가 100곡 + 복음성가 200곡 = 300곡입니다.
- 영상은 확인되지 않은 상태로 비워 두었습니다.
- 사람의 노래가 없는 반주 + 가사 표시 + 임베드 가능 여부가 모두 확인된 영상만 실제 재생 대상으로 넣도록 구성했습니다.
- GitHub Actions가 하루 1회 실행되어 검증 완료 대기열에서 최대 100곡을 자동 반영합니다.

## GitHub 업로드
압축을 풀어 기존 파일을 교체하고 다음 구조가 되도록 올리면 됩니다.

church-love/
- index.html
- style.css
- app.js
- songs.json
- update_queue.json
- README.md
- scripts/daily_update.py
- .github/workflows/daily-update.yml

GitHub Actions의 예약 실행은 UTC 00:00이며 한국 시간으로 오전 9시입니다.

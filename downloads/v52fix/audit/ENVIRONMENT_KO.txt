# 실행 환경 · 기준 커밋 · URL · 실행 시각
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 모든 수치는 아래 링크한 원본 로그/JSON에서 자동 추출.

- 공식 기준본 v5.1: 0003b46aeeaca319087e2bcc29ca72480e60c265
- 수정 전 v5.2 후보: 40ba21c5575ff4e8df1d33db9a5aca488290e213
- 테스트 기준(v5.2 수정 후보): c7d938d2fed2c9f485cba1700ca628a650504463 (앱 파일 528개)
- 다운로드 게시 커밋: 8ba2b77 (downloads/v52fix/ 추가, 앱 파일 변경 없음) · 이 검증 문서 커밋: 이 문서와 함께 푸시된 커밋(INDEX 참조)
- 저장소: archigon72/donnaemsae-194-test (테스트 전용). 운영 저장소 archigon72/donnaemsae-lab은 접근·변경하지 않음.
- 배포 URL: https://archigon72.github.io/donnaemsae-194-test/asset-hub.html · 구성 화면 https://archigon72.github.io/donnaemsae-194-test/management.html?mode=composition · SW 캐시명 donnaemsae-asset-hub-20261013-mobileui-v52a
- Release: https://github.com/archigon72/donnaemsae-194-test/releases/tag/v5.2fix-c7d938d
- 실행 환경: Linux 헤드리스 Google Chrome 154.0.8037.57, Playwright(Python) 1.63.0, 모바일 에뮬레이션(is_mobile, touch, ko-KR, Asia/Seoul), 각 스위트는 새 브라우저 컨텍스트(격리 프로필)·가상 원장만 사용. 가격 결측은 서비스워커 차단 컨텍스트에서 prices.json 응답만 모의.
- 로컬 실행: python http.server로 같은 파일 트리 제공(수정 전=40ba21c 트리, 수정 후=c7d938d 트리). 실배포 실행: 위 GitHub Pages URL.

| 스위트 | 환경 | PASS | FAIL | 기대 건수 | 완료 시각(KST, 로그 기록) | 대상 | 원본 로그 | 원본 JSON |
|---|---|---|---|---|---|---|---|---|
| 신규 A~G (qa_v52a.py, 수정 후) | 실배포 | 58 | 0 | 58 | 2026-10-13T21:12:54+09:00 | https://archigon72.github.io/donnaemsae-194-test/ | [raw/after_live.log.txt](raw/after_live.log.txt) | [raw/after_live/after_live_qa.json](raw/after_live/after_live_qa.json) |
| 신규 A~G (qa_v52a.py, 수정 후) | 로컬 | 58 | 0 | 58 | 2026-10-13T21:07:23+09:00 | http://127.0.0.1:8922/ | [raw/after_local.log.txt](raw/after_local.log.txt) | [raw/after_local/after_qa.json](raw/after_local/after_qa.json) |
| 신규 A~G를 수정 전 40ba21c에 실행(결함 재현) | 로컬 | 54 | 4 | 58 | 2026-10-13T21:07:23+09:00 | http://127.0.0.1:8921/ | [raw/before_local.log.txt](raw/before_local.log.txt) | [raw/before_local/before_qa.json](raw/before_local/before_qa.json) |
| v5.2 기존 검증 (qa_v52.py) | 실배포 | 65 | 0 | 65 | 2026-10-13T21:12:49+09:00 | https://archigon72.github.io/donnaemsae-194-test/ | [raw/v52_live.log.txt](raw/v52_live.log.txt) | [raw/v52_live/v52live_qa.json](raw/v52_live/v52live_qa.json) |
| v5.2 기존 검증 (qa_v52.py) | 로컬 | 65 | 0 | 65 | 2026-10-13T21:09:48+09:00 | http://127.0.0.1:8922/ | [raw/v52_local.log.txt](raw/v52_local.log.txt) | [raw/v52_local/v52_qa.json](raw/v52_local/v52_qa.json) |
| 원장 정밀검수 (audit.py) | 실배포 | 76 | 0 | 76 | 2026-10-13T21:12:51+09:00 | https://archigon72.github.io/donnaemsae-194-test/ | [raw/audit_live.log.txt](raw/audit_live.log.txt) | [raw/audit_live/audit_live_audit.json](raw/audit_live/audit_live_audit.json) |
| 원장 정밀검수 (audit.py) | 로컬 | 76 | 0 | 76 | 2026-10-13T21:09:50+09:00 | http://127.0.0.1:8922/ | [raw/audit_local.log.txt](raw/audit_local.log.txt) | [raw/audit_local/audit_audit.json](raw/audit_local/audit_audit.json) |
| 기존 원장 회귀·백업→초기화→복원 (qa_regress_v52a.py) | 실배포 | 39 | 0 | 39 | 2026-10-13T21:11:34+09:00 | https://archigon72.github.io/donnaemsae-194-test/ | [raw/reg_live.log.txt](raw/reg_live.log.txt) | [raw/reg_live/reg_live_regression.json](raw/reg_live/reg_live_regression.json) |
| 기존 원장 회귀·백업→초기화→복원 (qa_regress_v52a.py) | 로컬 | 39 | 0 | 39 | 2026-10-13T21:08:33+09:00 | http://127.0.0.1:8922/ | [raw/reg_local.log.txt](raw/reg_local.log.txt) | [raw/reg_local/reg_regression.json](raw/reg_local/reg_regression.json) |
| v5.1 도넛 색·순서 회귀 (qa_v51.py) | 실배포 | 22 | 0 | 22 | 2026-10-13T21:11:54+09:00 | https://archigon72.github.io/donnaemsae-194-test/ | [raw/v51_live.log.txt](raw/v51_live.log.txt) | [raw/v51_live/v51live_v51qa.json](raw/v51_live/v51live_v51qa.json) |
| v5.1 도넛 색·순서 회귀 (qa_v51.py) | 로컬 | 22 | 0 | 22 | 2026-10-13T21:08:53+09:00 | http://127.0.0.1:8922/ | [raw/v51_local.log.txt](raw/v51_local.log.txt) | [raw/v51_local/v51_v51qa.json](raw/v51_local/v51_v51qa.json) |

종료 코드: 각 스위트는 PASS/FAIL을 로그에 기록하고 예외 없이 종료(종료 코드 0). 종료 코드 자체는 별도 파일로 보관하지 않았음 → 다음 납품부터 기록 예정(CI 제안 참고).
실행 스크립트 원문: [raw/tools/audit.py.txt](raw/tools/audit.py.txt) · [raw/tools/layout.js.txt](raw/tools/layout.js.txt) · [raw/tools/oracle.py.txt](raw/tools/oracle.py.txt) · [raw/tools/qa_regress_v52a.py.txt](raw/tools/qa_regress_v52a.py.txt) · [raw/tools/qa_v4.py.txt](raw/tools/qa_v4.py.txt) · [raw/tools/qa_v51.py.txt](raw/tools/qa_v51.py.txt) · [raw/tools/qa_v52.py.txt](raw/tools/qa_v52.py.txt) · [raw/tools/qa_v52a.py.txt](raw/tools/qa_v52a.py.txt)

# v5.2 수정 후보(c7d938d) 검증 문서 인덱스
> **확인 주체: GrokBot 자체 검증(self-verification).** 비서실장 독립 검수 결과가 아니며, 이 페이지의 PASS는 GrokBot이 실행한 자동 검증 기록입니다.

상태: v5.2 수정 후보 납품, 비서실장 독립 검수 대기 · 테스트 커밋 c7d938d2fed2c9f485cba1700ca628a650504463 · 기준 v5.1 0003b46 · 사이트 https://archigon72.github.io/donnaemsae-194-test/asset-hub.html

모든 문서는 압축 해제 없이 브라우저에서 열립니다(.txt = 같은 내용의 일반 텍스트본, .md = 원문). 원본 로그·JSON은 raw/ 에 그대로 있습니다.

## 핵심 문서
- 변경 파일 목록·0003b46 대비 SHA·불변 증거: [CHANGES_AND_INVARIANCE_KO.txt](CHANGES_AND_INVARIANCE_KO.txt) · [.md](CHANGES_AND_INVARIANCE_KO.md)
- diff 원문 (0003b46 대비): [management-sw.js.vs_0003b46.diff.txt](diff/management-sw.js.vs_0003b46.diff.txt) · [management-view.js.vs_0003b46.diff.txt](diff/management-view.js.vs_0003b46.diff.txt) · [mobile-ui-v1.css.vs_0003b46.diff.txt](diff/mobile-ui-v1.css.vs_0003b46.diff.txt) (40ba21c 대비: [management-sw.js.vs_40ba21c.diff.txt](diff/management-sw.js.vs_40ba21c.diff.txt) · [management-view.js.vs_40ba21c.diff.txt](diff/management-view.js.vs_40ba21c.diff.txt) · [mobile-ui-v1.css.vs_40ba21c.diff.txt](diff/mobile-ui-v1.css.vs_40ba21c.diff.txt)) · [전체 528개 SHA 비교표](diff/ALL_FILES_SHA_COMPARE.txt)
- 수정 전후 값 (기대값 vs 실측값): [BEFORE_AFTER_VALUES_KO.txt](BEFORE_AFTER_VALUES_KO.txt) · [.md](BEFORE_AFTER_VALUES_KO.md)
- 실행 환경·커밋·URL·실행 시각·스위트별 결과표: [ENVIRONMENT_KO.txt](ENVIRONMENT_KO.txt) · [.md](ENVIRONMENT_KO.md)
- 백업 분할 ZIP·SHA-256·검증 명령/로그: [backup/BACKUP_VERIFY_KO.txt](backup/BACKUP_VERIFY_KO.txt) · [.md](backup/BACKUP_VERIFY_KO.md)
- 검증 제외(NOT TESTED)·알려진 문제: [NOT_TESTED_AND_KNOWN_ISSUES_KO.txt](NOT_TESTED_AND_KNOWN_ISSUES_KO.txt) · [.md](NOT_TESTED_AND_KNOWN_ISSUES_KO.md)

## 스위트별 결과 (항목별 입력·기대·실제·판정 표 + 원본 로그/JSON 링크)
| 스위트 | 실배포 PASS/FAIL | 로컬 PASS/FAIL | 상세 |
|---|---|---|---|
| 신규 A~G 58건 (수정 후) | 58/0 | 58/0 | [suites/new58_KO.txt](suites/new58_KO.txt) · [.md](suites/new58_KO.md) |
| 신규 A~G 58건을 수정 전 40ba21c에 실행 (결함 재현 54/58) | - | 54/4 | [suites/before58_KO.txt](suites/before58_KO.txt) · [.md](suites/before58_KO.md) |
| v5.2 기존 65건 | 65/0 | 65/0 | [suites/v52_65_KO.txt](suites/v52_65_KO.txt) · [.md](suites/v52_65_KO.md) |
| 원장 정밀검수 76건 | 76/0 | 76/0 | [suites/ledger76_KO.txt](suites/ledger76_KO.txt) · [.md](suites/ledger76_KO.md) |
| 원장 회귀 39건 (백업→초기화→복원 포함) | 39/0 | 39/0 | [suites/reg39_KO.txt](suites/reg39_KO.txt) · [.md](suites/reg39_KO.md) |
| v5.1 색·순서 회귀 22건 | 22/0 | 22/0 | [suites/color22_KO.txt](suites/color22_KO.txt) · [.md](suites/color22_KO.md) |

## 기타
- 요약 JSON: [SUMMARY.json](SUMMARY.json)
- 390px 캡처(PNG, 브라우저 열람): [captures_390/index.html](captures_390/index.html) · 360/412/430은 상위 폴더 ZIP
- 원본 로그·JSON·실행 스크립트 폴더: raw/ (각 스위트 문서에서 링크)
- 앱 파일 불변 확인: [APP_FILES_UNCHANGED.txt](APP_FILES_UNCHANGED.txt)
- 비밀정보 점검 기록: [PUBLISH_SCAN.txt](PUBLISH_SCAN.txt)
- 기존 다운로드 페이지: [../index.html](../index.html)

## CI 자동화 제안 (구현하지 않음)
- 범위: push 시 ① 앱 파일 528개 수·SHA를 FILES_SHA256.txt와 대조 ② 분할 ZIP 결합·zip 무결성·파일별 SHA ③ 0003b46 대비 변경 파일 허용목록 검사(원장·CORE·data 불변) ④ Playwright 스위트 실행(로컬 정적 서버), 로그·종료코드 보관 ⑤ 결과를 downloads/<버전>/ci/ 에 HTML/TXT로 출력(또는 Actions artifact).
- 추가 파일: .github/workflows/verify.yml, ci/verify_sha.py, ci/run_qa.sh (기존 QA 스크립트 재사용). 앱 파일 변경 없음.
- 권한: 워크플로 파일(.github/workflows/) 추가·수정에는 현재 토큰에 없는 Workflows 권한이 필요하고, 결과를 저장소에 다시 커밋하려면 워크플로의 contents: write 설정이 필요함. 대표 승인 전에는 진행하지 않음.
- 비용: 공개 저장소의 GitHub Actions 표준 러너 사용. 유료 서비스 없음. CI PASS도 자동 검증의 증거일 뿐, 비서실장 독립 검수가 아님.

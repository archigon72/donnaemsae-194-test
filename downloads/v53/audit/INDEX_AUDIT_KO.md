# v5.3 세전/세후 배당 토글 — 검증 문서 색인
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 상태: v5.3 개발 후보.

- 사이트: [https://archigon72.github.io/donnaemsae-194-test/management.html?mode=dividends](https://archigon72.github.io/donnaemsae-194-test/management.html?mode=dividends)
- 커밋: ed66d27 (기준 c7d938d) · SW 캐시 v53 · 상태: **v5.3 개발 후보**

## 스위트 결과
| 스위트 | 환경 | PASS | FAIL | 기준 | 로그 |
|---|---|---|---|---|---|
| v5.3 신규 세전/세후 (qa_v53.py) | 실배포 | 50 | 0 | 50 | [raw/v53_live.log.txt](raw/v53_live.log.txt) |
| v5.3 신규 세전/세후 (qa_v53.py) | 로컬(같은 파일) | 50 | 0 | 50 | [raw/local/v53_run.log.txt](raw/local/v53_run.log.txt) |
| v5.2 기존 (qa_v52.py) | 실배포 | 65 | 0 | 65 | [raw/v52_live.log.txt](raw/v52_live.log.txt) |
| v5.2 기존 (qa_v52.py) | 로컬(같은 파일) | 65 | 0 | 65 | [raw/v52_local.log.txt](raw/v52_local.log.txt) |
| v5.2fix A~G (qa_v52a.py) | 실배포 | 58 | 0 | 58 | [raw/after_live.log.txt](raw/after_live.log.txt) |
| v5.2fix A~G (qa_v52a.py) | 로컬(같은 파일) | 58 | 0 | 58 | [raw/after_local.log.txt](raw/after_local.log.txt) |
| 원장 정밀검수 (audit.py) | 실배포 | 68 | 8 | 76 | [raw/audit_live.log.txt](raw/audit_live.log.txt) |
| 원장 정밀검수 (audit.py) | 로컬(같은 파일) | 68 | 8 | 76 | [raw/audit_local.log.txt](raw/audit_local.log.txt) |
| 회귀·백업→초기화→복원 (qa_regress_v53.py = v52a 사본, 캐시명만 v53) | 실배포 | 39 | 0 | 39 | [raw/reg_live.log.txt](raw/reg_live.log.txt) |
| 회귀·백업→초기화→복원 (qa_regress_v53.py = v52a 사본, 캐시명만 v53) | 로컬(같은 파일) | 39 | 0 | 39 | [raw/reg_local.log.txt](raw/reg_local.log.txt) |
| v5.1 도넛 색·순서 (qa_v51.py) | 실배포 | 22 | 0 | 22 | [raw/v51_live.log.txt](raw/v51_live.log.txt) |
| v5.1 도넛 색·순서 (qa_v51.py) | 로컬(같은 파일) | 22 | 0 | 22 | [raw/v51_local.log.txt](raw/v51_local.log.txt) |

## 문서
- 스위트 상세 v5.3 신규: [suites/v53_50_KO.md](suites/v53_50_KO.md)
- 스위트 상세 v5.2: [suites/v52_65_KO.md](suites/v52_65_KO.md)
- 스위트 상세 v5.2fix: [suites/v52a_58_KO.md](suites/v52a_58_KO.md)
- 스위트 상세 원장 정밀검수(8 FAIL = 세후 의미 변경, NOT_TESTED 문서 참조): [suites/ledger76_KO.md](suites/ledger76_KO.md)
- 스위트 상세 회귀: [suites/reg39_KO.md](suites/reg39_KO.md)
- 스위트 상세 색·순서: [suites/color22_KO.md](suites/color22_KO.md)
- 규칙별 입력·기대·실제: [RULES_INPUT_EXPECTED_ACTUAL_KO.md](RULES_INPUT_EXPECTED_ACTUAL_KO.md)
- 변경 파일·diff·194 데이터 불변 증거: [CHANGES_AND_INVARIANCE_KO.md](CHANGES_AND_INVARIANCE_KO.md)
- NOT TESTED·분류 결정·동작 변경: [NOT_TESTED_AND_KNOWN_ISSUES_KO.md](NOT_TESTED_AND_KNOWN_ISSUES_KO.md)
- 실행 환경: [ENVIRONMENT_KO.md](ENVIRONMENT_KO.md)
- 캡처(브라우저 열람): [captures/index.html](captures/index.html)
- 백업 분할본·SHA·복원 테스트: [backup/BACKUP_VERIFY_KO.md](backup/BACKUP_VERIFY_KO.md)
- 비밀정보 점검: [PUBLISH_SCAN.txt](PUBLISH_SCAN.txt)
- 요약 JSON: [SUMMARY.json](SUMMARY.json)
- 다운로드 페이지: [../index.html](../index.html)

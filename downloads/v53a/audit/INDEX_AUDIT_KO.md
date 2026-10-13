# v5.3a 계좌유형 표시·무결성 추가 수정 — 검증 문서 색인
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 상태: v5.3 개발 후보(추가 수정).

- 테스트 주소: [관리(내 계좌 현황·계좌 종류)](https://archigon72.github.io/donnaemsae-194-test/management.html?mode=ledger) · [배당 세전/세후](https://archigon72.github.io/donnaemsae-194-test/management.html?mode=dividends) · [홈](https://archigon72.github.io/donnaemsae-194-test/asset-home.html)
- 커밋: 16ecc2d (기준 v5.3 ed66d27) · SW 캐시 v53a · 상태: **v5.3 개발 후보(추가 수정)** · 전체 v5.3 최종 승인 아님

## 스위트 결과
| 스위트 | 환경 | PASS | FAIL | 기준 | 로그 |
|---|---|---|---|---|---|
| v5.3a 계좌유형 표시·무결성 (qa_v53a.py, 신규) | 실배포 | 29 | 0 | 29 | [raw/live_v53a.log.txt](raw/live_v53a.log.txt) |
| v5.3a 계좌유형 표시·무결성 (qa_v53a.py, 신규) | 로컬(같은 파일) | 29 | 0 | 29 | [raw/local_v53a.log.txt](raw/local_v53a.log.txt) |
| v5.3 세전/세후 (qa_v53.py, 라벨 형식만 조정) | 실배포 | 50 | 0 | 50 | [raw/v53_live.log.txt](raw/v53_live.log.txt) |
| v5.3 세전/세후 (qa_v53.py, 라벨 형식만 조정) | 로컬(같은 파일) | 50 | 0 | 50 | [raw/v53_local.log.txt](raw/v53_local.log.txt) |
| v5.2 (qa_v52.py) | 실배포 | 65 | 0 | 65 | [raw/v52_live.log.txt](raw/v52_live.log.txt) |
| v5.2 (qa_v52.py) | 로컬(같은 파일) | 65 | 0 | 65 | [raw/v52_local.log.txt](raw/v52_local.log.txt) |
| v5.2fix A~G (qa_v52a.py) | 실배포 | 58 | 0 | 58 | [raw/after_live.log.txt](raw/after_live.log.txt) |
| v5.2fix A~G (qa_v52a.py) | 로컬(같은 파일) | 58 | 0 | 58 | [raw/after_local.log.txt](raw/after_local.log.txt) |
| 원장 정밀검수 (audit.py) — v5.3 미해결 8 FAIL 유지 | 실배포 | 68 | 8 | 76 | [raw/audit_live.log.txt](raw/audit_live.log.txt) |
| 원장 정밀검수 (audit.py) — v5.3 미해결 8 FAIL 유지 | 로컬(같은 파일) | 68 | 8 | 76 | [raw/audit_local.log.txt](raw/audit_local.log.txt) |
| 회귀·백업→초기화→복원 (qa_regress_v53a.py) | 실배포 | 39 | 0 | 39 | [raw/reg_live.log.txt](raw/reg_live.log.txt) |
| 회귀·백업→초기화→복원 (qa_regress_v53a.py) | 로컬(같은 파일) | 39 | 0 | 39 | [raw/reg_local.log.txt](raw/reg_local.log.txt) |
| v5.1 도넛 색·순서 (qa_v51.py) | 실배포 | 22 | 0 | 22 | [raw/v51_live.log.txt](raw/v51_live.log.txt) |
| v5.1 도넛 색·순서 (qa_v51.py) | 로컬(같은 파일) | 22 | 0 | 22 | [raw/v51_local.log.txt](raw/v51_local.log.txt) |

## 문서
- 스위트 상세 v5.3a 신규(계좌유형): [suites/v53a_29_KO.md](suites/v53a_29_KO.md)
- 스위트 상세 v5.3 세전/세후: [suites/v53_50_KO.md](suites/v53_50_KO.md)
- 스위트 상세 v5.2: [suites/v52_65_KO.md](suites/v52_65_KO.md)
- 스위트 상세 v5.2fix: [suites/v52a_58_KO.md](suites/v52a_58_KO.md)
- 스위트 상세 원장 정밀검수(v5.3 미해결 8 FAIL 유지, 별도 쟁점): [suites/ledger76_KO.md](suites/ledger76_KO.md)
- 스위트 상세 회귀: [suites/reg39_KO.md](suites/reg39_KO.md)
- 스위트 상세 색·순서: [suites/color22_KO.md](suites/color22_KO.md)
- 테스트 시나리오(유형 4종 생성·새로고침·이동·수정·백업·초기화·복원·구 원장): [suites/v53a_29_KO.md](suites/v53a_29_KO.md)
- 변경 파일·diff·194 데이터 불변 증거: [CHANGES_AND_INVARIANCE_KO.md](CHANGES_AND_INVARIANCE_KO.md)
- 마이그레이션 정책 확인·수정 경로·미해결 쟁점·NOT TESTED: [NOT_TESTED_AND_KNOWN_ISSUES_KO.md](NOT_TESTED_AND_KNOWN_ISSUES_KO.md)
- 실행 환경: [ENVIRONMENT_KO.md](ENVIRONMENT_KO.md)
- 캡처(브라우저 열람): [captures/index.html](captures/index.html)
- 기존 스위트 조정 diff: [raw/SUITE_ADAPTATION.diff.txt](raw/SUITE_ADAPTATION.diff.txt)
- 백업 분할본·SHA·복원 테스트: [backup/BACKUP_VERIFY_KO.md](backup/BACKUP_VERIFY_KO.md)
- 비밀정보 점검: [PUBLISH_SCAN.txt](PUBLISH_SCAN.txt)
- 요약 JSON: [SUMMARY.json](SUMMARY.json)
- 다운로드 페이지: [../index.html](../index.html)

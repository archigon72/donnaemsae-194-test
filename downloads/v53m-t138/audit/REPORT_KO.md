# GrokBot 자체 검증 — t138 / v53m

- 커밋: `9d8261e` · 태그: `v53m-t138-9d8261e` · 기준: `v53l-calendar-8f6b4f1`
- UAT: https://archigon72.github.io/donnaemsae-194-test/account-uat/
- SW 캐시: `dnmuat194-acct-uat-v53m-1`

## 구현
1. 계좌 라벨(표시 전용): `계좌명(계좌종류)`. 이름에 종류 토큰이 있으면 한 번만 제거 → `키움 IRP`→`키움(IRP)`, `카카오 ISA(ISA)` 중복 없음. 종류 없음→`(종류 미확인)`. 저장 이름·원장·세금 정책 불변.
2. 거래 등록: 제목/닫기 sticky + visualViewport 높이 맞춤, 검색 전체선택·X·즉시후보·빈결과 안내, 보유범위 안내 강조, 기존 계좌 종류 읽기전용, 배당재투자도 보유종목만(UI+저장 가드), 유형 변경 시 부적합 종목 해제.
3. '계좌 추가' 버튼(거래 등록과 분리, 하단바 겹침 0).
4. 캘린더: 배당락 기준 권리수량 q>0일 때만 표시(전량 매도 후 비보유 혼입 원인 → 수정).
5. 팔레트: 지시서 HEX 토큰(uat-t138.css), 도넛 8색, 범례 이름·% 줄바꿈.
6. 금액(표시만): 원=버림+쉼표, 만=버림 소수1자리, 1,000원 미만은 원 표기.

## QA (개발자 자체 QA)
| 스위트 | 결과 |
|---|---|
| unit_t138 | 21/21 PASS |
| unit1 / unit2 | 15/15 · 21/21 PASS |
| func | 35/35 PASS |
| uat_new / uat_vp / uat_regress | 38 · 37 · 40 PASS |
| qa_t138 로컬 (360/390/430) | 37/37 PASS |
| qa_t138 HTTPS 실사이트 | 37/37 PASS |
| 삼성/갤럭시 실기기 | **NOT TESTED** (대표 실기기 검수 대기) |

이슈별 표: [ISSUE_TABLE.md](ISSUE_TABLE.md)

## 범위 불변
[CHANGES_AND_INVARIANCE_KO.md](CHANGES_AND_INVARIANCE_KO.md)

## 백업
- 수정 전 baseline_8f6b4f1_pre_t138.zip — d5fd8bfcfed40cb8ab4243dd049ca003ce4fbd40bbb2cd78a38252a5d3d4c4b5 (197파일, unzip -t OK, 독립 해제 대조 197/197)
- 수정 후 completed_9d8261e_t138.zip — c33bec4799bcf472192231ffe8042cb14e77dd2a468923f13b66c3e5dd67d0ea (266파일, unzip -t OK, 대조 266/266)
- part 파일은 공개 GitHub 미게시, 채팅 첨부로 전달. 결합 방법: [JOIN_KO.txt](JOIN_KO.txt)

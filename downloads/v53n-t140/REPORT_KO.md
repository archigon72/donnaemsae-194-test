# v53n-t140 보고서 — GrokBot 자체 검증

이 보고서는 대표의 실화면 확인 전 상태입니다. '수정 완료'나 '최종 PASS'가 아닙니다. t138의 자체 37/37 PASS가 실화면에서 FAIL로 판정되었으므로, 이번 결과도 대표의 실화면 판정을 기준으로 삼아 주십시오.

- URL: https://archigon72.github.io/donnaemsae-194-test/account-uat/asset-hub.html (내 자산보기), https://archigon72.github.io/donnaemsae-194-test/account-uat/management.html
- 커밋: 83becb1 → 88e8514 (코드), 태그 v53n-t140-88e8514
- SW 캐시: dnmuat194-acct-uat-v53n-2

## 수정 1 — 계좌 주요 종목 top5 (asset-hub)
- 각 행에 종목명, 비중 %, 현재 평가액을 표시함 (B안).
- 순위와 비중은 구성 도넛(평가액 모드)과 같은 함수(compData)에서 계산함.
- 조회 범위를 따름. 6위 이하는 기타 #6B7280으로 묶음.
- 시세가 없는 보유 종목은 하단에 '제외'로 표시함. 보유하지 않은 종목은 표시하지 않음.
- 직접투자 원가 표시(내가 넣은 돈 800,000원 · 직접투자 취득원가)는 그대로 유지함.

| 항목 | 결과 |
|---|---|
| 종목명·순서·% = 평가액 구성 범례 (360/390/430) | PASS |
| 순위 색 = 승인 8색 순서, 도넛 조각 색과 일치 | PASS |
| 금액 합 494,610원 = 평가액 합계 | PASS |
| 조회 범위 카카오(ISA) → 그 계좌 보유 2종목만 | PASS |
| 원가 표시 유지 | PASS |
| 기타(#6B7280) 행 실화면 표시 | NOT TESTED (시험 데이터가 4종목이라 해당 없음) |

자세한 비교는 TOP5_TABLE_KO.md에 있음.

## 수정 2 — 승인 팔레트
- asset-hub와 management.html 전체에 적용함. 거래 등록 버튼의 초록 그라데이션은 primary #A7DEC9 바탕 + #09251E 글자로 바꿈.
- t140b에서 추가로 고친 3-B 역할 불일치(내부 점검에서 발견):
  - 카드 테두리: raised → border #385465
  - 선택 탭 글자: text → primary #A7DEC9
  - 관리 화면 보조 글자: complete #9DCFF3 → muted #AEC0CB
- CSS 변수 18개 = 지시서 HEX (HTTPS, 강제 새로고침 후에도 동일): PASS
- computed style 표 318행, 불일치 0: PASS (COLOR_TABLE_KO.md)
- SW: 강제 새로고침(캐시 끔) 후 캐시 키가 v53n-2 하나뿐이고 controller 활성: PASS
- 사람 눈으로 보는 전체 화면 색 인상, 명암 대비 실기기 확인: NOT TESTED (대표 실화면 확인 필요)
- 검사한 부위는 표본 선택자 기준임. 팔레트 매핑은 자동 변환이라, 표본 밖 세부 요소(배지·차트 보조선 등)에서 역할이 어긋날 수 있음. 실화면에서 이상한 부위가 보이면 지적해 주십시오.

## 수정 3 — '+ 거래 등록' FAB (asset-hub)

| 항목 | 결과 |
|---|---|
| 우측 하단 표시, 하단 내비와 겹침 0, 중심점 가림 없음 (360/390/430) | PASS |
| 탭 → 기존 거래 등록 모달 → 닫기 → 같은 화면으로 복귀 | PASS |
| 모달이 열린 동안 FAB 숨김 | PASS |
| 탭 전환 후 복귀 시에도 유지 | PASS |
| 계좌 추가와 분리 | PASS |
| 소프트 키보드, 실기기 safe-area | NOT TESTED |

자세한 내용은 FAB_EVIDENCE_KO.md에 있음.

## 회귀 + 신규 시험 (HTTPS 빌드)

| 묶음 | 결과 |
|---|---|
| qa_t140 (신규) | 61/61 PASS |
| qa_t138 (기존 37, SW 캐시 이름만 v53n-2로 갱신) | 37/37 PASS |
| uat_regress | 40/40 PASS |
| uat_new | 38/38 PASS |
| uat_vp | 37/37 PASS |
| func | 35/35 PASS |
| unit_t138 | 21/21 PASS (로컬 node, 코드 동일) |
| unit1 | 15/15 PASS (로컬 node, 코드 동일) |
| unit2 | 21/21 PASS (로컬 node, 코드 동일) |

BEFORE(9d8261e, HTTPS): FAB 없음, top5 없음 (360/390/430 모두). 캡처는 captures/before/에 있음.

## NOT TESTED
- 삼성 실기기와 삼성 인터넷 브라우저 (항상 NOT TESTED)
- iOS Safari 실기기
- 소프트 키보드 겹침, 실기기 safe-area
- top5 기타 행 실화면 표시
- 사람 눈으로 보는 색 인상과 명암 대비 (대표 실화면 판정 대기)

## 백업
공개 GitHub에 백업 ZIP을 올리지 않았음 (대표 규칙). 백업이 필요하면 채팅 첨부로 전달함.

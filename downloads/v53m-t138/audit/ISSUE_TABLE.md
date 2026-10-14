| 이슈 | 재현 | 해소 | 결과 |
|---|---|---|---|
| 거래 모달 상단 잘림 | BEFORE 360 trade_dialog | sticky h2/닫기 + visualViewport --uat-vvh | PASS (로컬·HTTPS) |
| 종목 검색/교체 UX | 검색칸 전체선택·X·빈결과 | uat-search-wrap + doSearch | PASS |
| 보유제한(추가매수/매도/재투자) | 지시서상 정상 | holdingOnly에 reinvest 포함·안내 강조 | PASS |
| 계좌명/종류 순서 | 기존 [종류] 이름 | AL=이름(종류), 기존 종류 읽기전용 | PASS |
| 어디서든 계좌 추가 | FAB만 존재 | uat-acct-add 분리 버튼 | PASS |
| 캘린더 비보유 혼입 | 매도 후 q=0 ex 점 | ex push만 q>0 | PASS (unit+엔진) |
| 계좌 필터 | 칩/탭 | AL+필터 유지 | PASS |
| 세전/세후 합산 | unit2 | 불변 | PASS 21/21 |
| 도넛 이름/% | ellipsis | uat-donut-legend wrap | PASS |
| 금액 소수점 | 옛 round | floor 원 / floor 만 1자리 / <1000원 | PASS |
| 계좌 라벨 계좌명(종류) | 요청 추가 | AL+dedupe 규칙 | PASS 360/390/430 |
| 삼성 실기기 | — | — | NOT TESTED |

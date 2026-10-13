# 기존 원장 회귀·백업→초기화→복원 (qa_regress_v52a.py)
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 모든 수치는 아래 링크한 원본 로그/JSON에서 자동 추출.

## 실배포 https://archigon72.github.io/donnaemsae-194-test/
- 실행 완료 시각(로그 파일 기록 시각, KST): 2026-10-13T21:11:34+09:00 · 대상 base: https://archigon72.github.io/donnaemsae-194-test/ · 결과: PASS 39 / FAIL 0 / 총 39
- 원본 로그: [raw/reg_live.log.txt](raw/reg_live.log.txt) · 원본 JSON: [raw/reg_live/reg_live_regression.json](raw/reg_live/reg_live_regression.json)

| # | 항목 (입력 조건·기대 기준이 항목명에 포함) | 판정 | 실측 상세(기대·실제 값) |
|---|---|---|---|
| 1 | fresh throwaway profile: no stored facts | PASS | null |
| 2 | 497880 검색 노출 | PASS | null |
| 3 | register=497880 → 거래 등록 시트에 497880 선택 | PASS | "497880" |
| 4 | FAB opens trade sheet & FAB hidden while open | PASS | null |
| 5 | 8px slider kept (all dialog track rules 8px, input bg transparent/no border) | PASS | {"rules": [".garden #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px", "body.mu #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px"], "bg": "rgba(0, 0, 0, 0)", "border": "0px"} |
| 6 | 최초매수 497880 10주 | PASS | [] |
| 7 | 최초매수 472150 10주 (새 계좌 ISA) | PASS | [] |
| 8 | 매도 시 해당 계좌 보유종목만 표시 | PASS | ["472150"] |
| 9 | 추가매수 시 보유종목만 표시 | PASS | ["472150"] |
| 10 | 최초매수 시 194종 전체 표시 | PASS | 194 |
| 11 | 자동금액 = 수량×가격 (7×12,345=86,415) | PASS | ["86,415 원", "7주 × 12,345원"] |
| 12 | 추가매수 497880 5주 | PASS | [] |
| 13 | 같은 날짜 복수 거래 (2026-03-03 두번째) | PASS | [] |
| 14 | 같은 날 order_key 0,1 순서 | PASS | [0, 1] |
| 15 | 부분 매도 497880 3주 | PASS | [] |
| 16 | 매도 비율 50% → floor(27×0.5)=13주, 잔여 14주 | PASS | ["27주", "13", "13주", "14주", "50"] |
| 17 | 비율 매도 저장 | PASS | [] |
| 18 | 슬라이더 100% → 보유 전량 14주 | PASS | "14" |
| 19 | 전량 매도 저장 | PASS | [] |
| 20 | 보유 초과 매도 차단 | PASS | ["매도 수량이 보유수량 12주를 초과했습니다."] |
| 21 | 전량매도 종목은 매도 목록에서 제외 | PASS | ["497880"] |
| 22 | 전량매도 후 최초매수로 새 사이클 | PASS | [] |
| 23 | 0018C0 사이클 2개 | PASS | 2 |
| 24 | 신규 ETF 배당재투자 (보유 없던 0005A0, 50%) | PASS | {"calc": "사용 가능한 배당금: 39,550원\n이번에 재투자할 금액: 19,775원\n매수 가능 수량: 2주\n실제 매수금액: 18,180원\n재투자 후 남는 배당금: 21,370원", "qty": "2", "price": "9090", "amount": "18,180 원", "err": []} |
| 25 | 잔여 배당현금 재투자 (0005A0, 100%) | PASS | {"calc": "사용 가능한 배당금: 21,370원\n이번에 재투자할 금액: 21,370원\n매수 가능 수량: 2주\n실제 매수금액: 18,180원\n재투자 후 남는 배당금: 3,190원", "qty": "2", "price": "9090", "amount": "18,180 원", "err": []} |
| 26 | 잔여 현금 대조: 2차 사용가능 = 1차 사용가능 − 1차 매수금액 | PASS | {"a1": 39550.0, "used1": 18180.0, "a2": 21370.0} |
| 27 | 거래 수정 (추가매수 5→6주) | PASS | [] |
| 28 | 거래 날짜 변경 (03-03→03-04) | PASS | [] |
| 29 | 거래 삭제 | PASS | 9 |
| 30 | 새로고침 후 원장·화면 동일 | PASS | null |
| 31 | 거래 레코드 스키마 키 불변 | PASS | ["account_id", "code", "cycle_id", "order_key", "quantity", "trade_date", "trade_price", "transaction_id", "type"] |
| 32 | 백업 파일 = 저장 원장 | PASS | null |
| 33 | 기록 초기화 | PASS | null |
| 34 | 백업 복원 → 원장 동일 | PASS | null |
| 35 | 복원 후 성과 화면 숫자 동일 | PASS | null |
| 36 | SW scope=사이트 경로, 새 캐시명, mobile-ui-v1.css 캐시 | PASS | {"scope": "https://archigon72.github.io/donnaemsae-194-test/", "keys": ["donnaemsae-asset-hub-20261013-mobileui-v52a"], "count": 363, "css": true} |
| 37 | 오프라인 새로고침 (SW 캐시) | PASS | "연구소 대문\n돈냄새연구소\n정밀하게 분석하고, 천천히 키운다.\n계좌·거래 관리\n\n계좌와 거래 기록을 관리하고 백업해요.\n\n배당 성과 분석으로 →\n" |
| 38 | 가상 데이터 정리 (localStorage 비움) | PASS | null |
| 39 | 콘솔/페이지 오류 0건 | PASS | [] |

실패 상세: 없음

- console/pageerror 기록: []

## 로컬 http://127.0.0.1 (같은 커밋 파일)
- 실행 완료 시각(로그 파일 기록 시각, KST): 2026-10-13T21:08:33+09:00 · 대상 base: http://127.0.0.1:8922/ · 결과: PASS 39 / FAIL 0 / 총 39
- 원본 로그: [raw/reg_local.log.txt](raw/reg_local.log.txt) · 원본 JSON: [raw/reg_local/reg_regression.json](raw/reg_local/reg_regression.json)

| # | 항목 (입력 조건·기대 기준이 항목명에 포함) | 판정 | 실측 상세(기대·실제 값) |
|---|---|---|---|
| 1 | fresh throwaway profile: no stored facts | PASS | null |
| 2 | 497880 검색 노출 | PASS | null |
| 3 | register=497880 → 거래 등록 시트에 497880 선택 | PASS | "497880" |
| 4 | FAB opens trade sheet & FAB hidden while open | PASS | null |
| 5 | 8px slider kept (all dialog track rules 8px, input bg transparent/no border) | PASS | {"rules": [".garden #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px", "body.mu #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px"], "bg": "rgba(0, 0, 0, 0)", "border": "0px"} |
| 6 | 최초매수 497880 10주 | PASS | [] |
| 7 | 최초매수 472150 10주 (새 계좌 ISA) | PASS | [] |
| 8 | 매도 시 해당 계좌 보유종목만 표시 | PASS | ["472150"] |
| 9 | 추가매수 시 보유종목만 표시 | PASS | ["472150"] |
| 10 | 최초매수 시 194종 전체 표시 | PASS | 194 |
| 11 | 자동금액 = 수량×가격 (7×12,345=86,415) | PASS | ["86,415 원", "7주 × 12,345원"] |
| 12 | 추가매수 497880 5주 | PASS | [] |
| 13 | 같은 날짜 복수 거래 (2026-03-03 두번째) | PASS | [] |
| 14 | 같은 날 order_key 0,1 순서 | PASS | [0, 1] |
| 15 | 부분 매도 497880 3주 | PASS | [] |
| 16 | 매도 비율 50% → floor(27×0.5)=13주, 잔여 14주 | PASS | ["27주", "13", "13주", "14주", "50"] |
| 17 | 비율 매도 저장 | PASS | [] |
| 18 | 슬라이더 100% → 보유 전량 14주 | PASS | "14" |
| 19 | 전량 매도 저장 | PASS | [] |
| 20 | 보유 초과 매도 차단 | PASS | ["매도 수량이 보유수량 12주를 초과했습니다."] |
| 21 | 전량매도 종목은 매도 목록에서 제외 | PASS | ["497880"] |
| 22 | 전량매도 후 최초매수로 새 사이클 | PASS | [] |
| 23 | 0018C0 사이클 2개 | PASS | 2 |
| 24 | 신규 ETF 배당재투자 (보유 없던 0005A0, 50%) | PASS | {"calc": "사용 가능한 배당금: 39,550원\n이번에 재투자할 금액: 19,775원\n매수 가능 수량: 2주\n실제 매수금액: 18,180원\n재투자 후 남는 배당금: 21,370원", "qty": "2", "price": "9090", "amount": "18,180 원", "err": []} |
| 25 | 잔여 배당현금 재투자 (0005A0, 100%) | PASS | {"calc": "사용 가능한 배당금: 21,370원\n이번에 재투자할 금액: 21,370원\n매수 가능 수량: 2주\n실제 매수금액: 18,180원\n재투자 후 남는 배당금: 3,190원", "qty": "2", "price": "9090", "amount": "18,180 원", "err": []} |
| 26 | 잔여 현금 대조: 2차 사용가능 = 1차 사용가능 − 1차 매수금액 | PASS | {"a1": 39550.0, "used1": 18180.0, "a2": 21370.0} |
| 27 | 거래 수정 (추가매수 5→6주) | PASS | [] |
| 28 | 거래 날짜 변경 (03-03→03-04) | PASS | [] |
| 29 | 거래 삭제 | PASS | 9 |
| 30 | 새로고침 후 원장·화면 동일 | PASS | null |
| 31 | 거래 레코드 스키마 키 불변 | PASS | ["account_id", "code", "cycle_id", "order_key", "quantity", "trade_date", "trade_price", "transaction_id", "type"] |
| 32 | 백업 파일 = 저장 원장 | PASS | null |
| 33 | 기록 초기화 | PASS | null |
| 34 | 백업 복원 → 원장 동일 | PASS | null |
| 35 | 복원 후 성과 화면 숫자 동일 | PASS | null |
| 36 | SW scope=사이트 경로, 새 캐시명, mobile-ui-v1.css 캐시 | PASS | {"scope": "http://127.0.0.1:8922/", "keys": ["donnaemsae-asset-hub-20261013-mobileui-v52a"], "count": 363, "css": true} |
| 37 | 오프라인 새로고침 (SW 캐시) | PASS | "연구소 대문\n돈냄새연구소\n정밀하게 분석하고, 천천히 키운다.\n계좌·거래 관리\n\n계좌와 거래 기록을 관리하고 백업해요.\n\n배당 성과 분석으로 →\n" |
| 38 | 가상 데이터 정리 (localStorage 비움) | PASS | null |
| 39 | 콘솔/페이지 오류 0건 | PASS | [] |

실패 상세: 없음

- console/pageerror 기록: []


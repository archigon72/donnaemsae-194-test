# 회귀·백업→초기화→복원 (qa_regress_v53b.py)
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 상태: v5.3 개발 후보(마무리 수정).

## 실배포: PASS 39 / FAIL 0 / 기준 39
- 원본 로그: [raw/reg_live.log.txt](../raw/reg_live.log.txt) · 원본 JSON: [raw/reg_live/reg_regression.json](../raw/reg_live/reg_regression.json)

| # | 항목 | 판정 | 상세 |
|---|---|---|---|
| 1 | fresh throwaway profile: no stored facts  | PASS | fresh throwaway profile: no stored facts  |
| 2 | 497880 검색 노출  | PASS | 497880 검색 노출  |
| 3 | register=497880 → 거래 등록 시트에 497880 선택 "497880" | PASS | register=497880 → 거래 등록 시트에 497880 선택 "497880" |
| 4 | FAB opens trade sheet & FAB hidden while open  | PASS | FAB opens trade sheet & FAB hidden while open  |
| 5 | 8px slider kept (all dialog track rules 8px, input bg transparent/no border) | PASS | 8px slider kept (all dialog track rules 8px, input bg transparent/no border) {"rules": [".garden #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px", "body.mu #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px"], "bg": "rgba(0, 0, 0, 0)", "border": "0px"} |
| 6 | 최초매수 497880 10주 | PASS | 최초매수 497880 10주 [] |
| 7 | 최초매수 472150 10주 (새 계좌 ISA) | PASS | 최초매수 472150 10주 (새 계좌 ISA) [] |
| 8 | 매도 시 해당 계좌 보유종목만 표시 | PASS | 매도 시 해당 계좌 보유종목만 표시 ["472150"] |
| 9 | 추가매수 시 보유종목만 표시 | PASS | 추가매수 시 보유종목만 표시 ["472150"] |
| 10 | 최초매수 시 194종 전체 표시 194 | PASS | 최초매수 시 194종 전체 표시 194 |
| 11 | 자동금액 = 수량×가격 (7×12,345=86,415) | PASS | 자동금액 = 수량×가격 (7×12,345=86,415) ["86,415 원", "7주 × 12,345원"] |
| 12 | 추가매수 497880 5주 | PASS | 추가매수 497880 5주 [] |
| 13 | 같은 날짜 복수 거래 (2026-03-03 두번째) | PASS | 같은 날짜 복수 거래 (2026-03-03 두번째) [] |
| 14 | 같은 날 order_key 0,1 순서 | PASS | 같은 날 order_key 0,1 순서 [0, 1] |
| 15 | 부분 매도 497880 3주 | PASS | 부분 매도 497880 3주 [] |
| 16 | 매도 비율 50% → floor(27×0.5)=13주, 잔여 14주 | PASS | 매도 비율 50% → floor(27×0.5)=13주, 잔여 14주 ["27주", "13", "13주", "14주", "50"] |
| 17 | 비율 매도 저장 | PASS | 비율 매도 저장 [] |
| 18 | 슬라이더 100% → 보유 전량 14주 "14" | PASS | 슬라이더 100% → 보유 전량 14주 "14" |
| 19 | 전량 매도 저장 | PASS | 전량 매도 저장 [] |
| 20 | 보유 초과 매도 차단 | PASS | 보유 초과 매도 차단 ["매도 수량이 보유수량 12주를 초과했습니다."] |
| 21 | 전량매도 종목은 매도 목록에서 제외 | PASS | 전량매도 종목은 매도 목록에서 제외 ["497880"] |
| 22 | 전량매도 후 최초매수로 새 사이클 | PASS | 전량매도 후 최초매수로 새 사이클 [] |
| 23 | 0018C0 사이클 2개 2 | PASS | 0018C0 사이클 2개 2 |
| 24 | 신규 ETF 배당재투자 (보유 없던 0005A0, 50%) | PASS | 신규 ETF 배당재투자 (보유 없던 0005A0, 50%) {"calc": "사용 가능한 배당금: 35,444원\n이번에 재투자할 금액: 17,722원\n매수 가능 수량: 1주\n실제 매수금액: 9,090원\n재투자 후 남는 배당금: 26,354원", "qty": "1", "price": "9090", "amount": "9,090 원", "err": []} |
| 25 | 잔여 배당현금 재투자 (0005A0, 100%) | PASS | 잔여 배당현금 재투자 (0005A0, 100%) {"calc": "사용 가능한 배당금: 26,354원\n이번에 재투자할 금액: 26,354원\n매수 가능 수량: 2주\n실제 매수금액: 18,180원\n재투자 후 남는 배당금: 8,174원", "qty": "2", "price": "9090", "amount": "18,180 원", "err": []} |
| 26 | 잔여 현금 대조: 2차 사용가능 = 1차 사용가능 − 1차 매수금액 | PASS | 잔여 현금 대조: 2차 사용가능 = 1차 사용가능 − 1차 매수금액 {"a1": 35444.0, "used1": 9090.0, "a2": 26354.0} |
| 27 | 거래 수정 (추가매수 5→6주) | PASS | 거래 수정 (추가매수 5→6주) [] |
| 28 | 거래 날짜 변경 (03-03→03-04) | PASS | 거래 날짜 변경 (03-03→03-04) [] |
| 29 | 거래 삭제 9 | PASS | 거래 삭제 9 |
| 30 | 새로고침 후 원장·화면 동일  | PASS | 새로고침 후 원장·화면 동일  |
| 31 | 거래 레코드 스키마 키 불변 | PASS | 거래 레코드 스키마 키 불변 ["account_id", "code", "cycle_id", "order_key", "quantity", "trade_date", "trade_price", "transaction_id", "type"] |
| 32 | 백업 파일 = 저장 원장  | PASS | 백업 파일 = 저장 원장  |
| 33 | 기록 초기화  | PASS | 기록 초기화  |
| 34 | 백업 복원 → 원장 동일  | PASS | 백업 복원 → 원장 동일  |
| 35 | 복원 후 성과 화면 숫자 동일  | PASS | 복원 후 성과 화면 숫자 동일  |
| 36 | SW scope=사이트 경로, 새 캐시명, mobile-ui-v1.css 캐시 | PASS | SW scope=사이트 경로, 새 캐시명, mobile-ui-v1.css 캐시 {"scope": "https://archigon72.github.io/donnaemsae-194-test/", "keys": ["donnaemsae-asset-hub-20261013-mobileui-v53b"], "count": 365, "css": true} |
| 37 | 오프라인 새로고침 (SW 캐시) "연구소 대문\n돈냄새연구소\n정밀하게 분석하고, 천천히 키운다.\n계좌·거래 관리\n\n계좌와 거래 기록을 관리하고 백업해요.\n\n배당 성과 분석으로 →\n" | PASS | 오프라인 새로고침 (SW 캐시) "연구소 대문\n돈냄새연구소\n정밀하게 분석하고, 천천히 키운다.\n계좌·거래 관리\n\n계좌와 거래 기록을 관리하고 백업해요.\n\n배당 성과 분석으로 →\n" |
| 38 | 가상 데이터 정리 (localStorage 비움)  | PASS | 가상 데이터 정리 (localStorage 비움)  |
| 39 | 콘솔/페이지 오류 0건 | PASS | 콘솔/페이지 오류 0건 [] |

## 로컬(같은 파일): PASS 39 / FAIL 0 / 기준 39
- 원본 로그: [raw/reg_local.log.txt](../raw/reg_local.log.txt) · 원본 JSON: [raw/reg_local/reg_regression.json](../raw/reg_local/reg_regression.json)

| # | 항목 | 판정 | 상세 |
|---|---|---|---|
| 1 | fresh throwaway profile: no stored facts  | PASS | fresh throwaway profile: no stored facts  |
| 2 | 497880 검색 노출  | PASS | 497880 검색 노출  |
| 3 | register=497880 → 거래 등록 시트에 497880 선택 "497880" | PASS | register=497880 → 거래 등록 시트에 497880 선택 "497880" |
| 4 | FAB opens trade sheet & FAB hidden while open  | PASS | FAB opens trade sheet & FAB hidden while open  |
| 5 | 8px slider kept (all dialog track rules 8px, input bg transparent/no border) | PASS | 8px slider kept (all dialog track rules 8px, input bg transparent/no border) {"rules": [".garden #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px", "body.mu #ledger-dialog input[type=\"range\"]::-webkit-slider-runnable-track => 8px"], "bg": "rgba(0, 0, 0, 0)", "border": "0px"} |
| 6 | 최초매수 497880 10주 | PASS | 최초매수 497880 10주 [] |
| 7 | 최초매수 472150 10주 (새 계좌 ISA) | PASS | 최초매수 472150 10주 (새 계좌 ISA) [] |
| 8 | 매도 시 해당 계좌 보유종목만 표시 | PASS | 매도 시 해당 계좌 보유종목만 표시 ["472150"] |
| 9 | 추가매수 시 보유종목만 표시 | PASS | 추가매수 시 보유종목만 표시 ["472150"] |
| 10 | 최초매수 시 194종 전체 표시 194 | PASS | 최초매수 시 194종 전체 표시 194 |
| 11 | 자동금액 = 수량×가격 (7×12,345=86,415) | PASS | 자동금액 = 수량×가격 (7×12,345=86,415) ["86,415 원", "7주 × 12,345원"] |
| 12 | 추가매수 497880 5주 | PASS | 추가매수 497880 5주 [] |
| 13 | 같은 날짜 복수 거래 (2026-03-03 두번째) | PASS | 같은 날짜 복수 거래 (2026-03-03 두번째) [] |
| 14 | 같은 날 order_key 0,1 순서 | PASS | 같은 날 order_key 0,1 순서 [0, 1] |
| 15 | 부분 매도 497880 3주 | PASS | 부분 매도 497880 3주 [] |
| 16 | 매도 비율 50% → floor(27×0.5)=13주, 잔여 14주 | PASS | 매도 비율 50% → floor(27×0.5)=13주, 잔여 14주 ["27주", "13", "13주", "14주", "50"] |
| 17 | 비율 매도 저장 | PASS | 비율 매도 저장 [] |
| 18 | 슬라이더 100% → 보유 전량 14주 "14" | PASS | 슬라이더 100% → 보유 전량 14주 "14" |
| 19 | 전량 매도 저장 | PASS | 전량 매도 저장 [] |
| 20 | 보유 초과 매도 차단 | PASS | 보유 초과 매도 차단 ["매도 수량이 보유수량 12주를 초과했습니다."] |
| 21 | 전량매도 종목은 매도 목록에서 제외 | PASS | 전량매도 종목은 매도 목록에서 제외 ["497880"] |
| 22 | 전량매도 후 최초매수로 새 사이클 | PASS | 전량매도 후 최초매수로 새 사이클 [] |
| 23 | 0018C0 사이클 2개 2 | PASS | 0018C0 사이클 2개 2 |
| 24 | 신규 ETF 배당재투자 (보유 없던 0005A0, 50%) | PASS | 신규 ETF 배당재투자 (보유 없던 0005A0, 50%) {"calc": "사용 가능한 배당금: 35,444원\n이번에 재투자할 금액: 17,722원\n매수 가능 수량: 1주\n실제 매수금액: 9,090원\n재투자 후 남는 배당금: 26,354원", "qty": "1", "price": "9090", "amount": "9,090 원", "err": []} |
| 25 | 잔여 배당현금 재투자 (0005A0, 100%) | PASS | 잔여 배당현금 재투자 (0005A0, 100%) {"calc": "사용 가능한 배당금: 26,354원\n이번에 재투자할 금액: 26,354원\n매수 가능 수량: 2주\n실제 매수금액: 18,180원\n재투자 후 남는 배당금: 8,174원", "qty": "2", "price": "9090", "amount": "18,180 원", "err": []} |
| 26 | 잔여 현금 대조: 2차 사용가능 = 1차 사용가능 − 1차 매수금액 | PASS | 잔여 현금 대조: 2차 사용가능 = 1차 사용가능 − 1차 매수금액 {"a1": 35444.0, "used1": 9090.0, "a2": 26354.0} |
| 27 | 거래 수정 (추가매수 5→6주) | PASS | 거래 수정 (추가매수 5→6주) [] |
| 28 | 거래 날짜 변경 (03-03→03-04) | PASS | 거래 날짜 변경 (03-03→03-04) [] |
| 29 | 거래 삭제 9 | PASS | 거래 삭제 9 |
| 30 | 새로고침 후 원장·화면 동일  | PASS | 새로고침 후 원장·화면 동일  |
| 31 | 거래 레코드 스키마 키 불변 | PASS | 거래 레코드 스키마 키 불변 ["account_id", "code", "cycle_id", "order_key", "quantity", "trade_date", "trade_price", "transaction_id", "type"] |
| 32 | 백업 파일 = 저장 원장  | PASS | 백업 파일 = 저장 원장  |
| 33 | 기록 초기화  | PASS | 기록 초기화  |
| 34 | 백업 복원 → 원장 동일  | PASS | 백업 복원 → 원장 동일  |
| 35 | 복원 후 성과 화면 숫자 동일  | PASS | 복원 후 성과 화면 숫자 동일  |
| 36 | SW scope=사이트 경로, 새 캐시명, mobile-ui-v1.css 캐시 | PASS | SW scope=사이트 경로, 새 캐시명, mobile-ui-v1.css 캐시 {"scope": "http://127.0.0.1:8134/", "keys": ["donnaemsae-asset-hub-20261013-mobileui-v53b"], "count": 365, "css": true} |
| 37 | 오프라인 새로고침 (SW 캐시) "연구소 대문\n돈냄새연구소\n정밀하게 분석하고, 천천히 키운다.\n계좌·거래 관리\n\n계좌와 거래 기록을 관리하고 백업해요.\n\n배당 성과 분석으로 →\n" | PASS | 오프라인 새로고침 (SW 캐시) "연구소 대문\n돈냄새연구소\n정밀하게 분석하고, 천천히 키운다.\n계좌·거래 관리\n\n계좌와 거래 기록을 관리하고 백업해요.\n\n배당 성과 분석으로 →\n" |
| 38 | 가상 데이터 정리 (localStorage 비움)  | PASS | 가상 데이터 정리 (localStorage 비움)  |
| 39 | 콘솔/페이지 오류 0건 | PASS | 콘솔/페이지 오류 0건 [] |


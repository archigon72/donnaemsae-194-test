# 미래배당 예상 규칙 구현 (대표 결정 2026-10-14) — GrokBot 자체 검증
- 사전계산: account-uat/fd-forecast.json (gen.py, 입력 = data/management-distributions.json v5.3f + .github/oneclick/krx_calendar.json). 원장에 쓰지 않음.
- 주기 분류(백테스트와 동일): 데이터 기준일 2026-10-08 직전 12개월 배당락 횟수 n — ≥40 weekly, ≥10 monthly, ≥3 quarterly, ≥1 semi/annual, 0 none. 결과: monthly 161 · quarterly 24 · semi/annual 8 · none 1(0238P0, 이력 없음) · weekly 0
- 금액(옵션 C, N=3): monthly만 주당 = 최근 3회 주당 분배금 평균(유리수 정확 계산, 3으로 나눔) × 해당 회차 권리수량. 백테스트 방식(전체 행)과 실제 적용(중복 제외 행)의 최근 3회 값 차이 0/161
- quarterly·semi/annual: 예상 배당락·지급일만 표시, 금액 '금액 미정' — 연간·월·계좌 합계에서 제외(0으로 합산하지 않고 건수로 표시)
- 예상 배당락일: 마지막 실제 배당락월 + 주기(monthly 1개월, 그 외 round(12/n)개월). 일자 = 최근 3회의 '월말까지 남은 KRX 영업일 수' 최빈값(동률 시 최근)을 그 달 마지막 영업일에서 역산
- 예상 지급일: 예상 배당락 다음날부터 3번째 KRX 영업일(기존 규칙). 자가검증: 기존 estimated 3,416건 100% 재현
- 실제 우선: 각 종목 기존 자료 마지막 배당락일 이후만 예측 → 실제/예상 중복 0
- 달력 범위: krx_calendar 2006-01-01~2027-12-31. 2027 휴일은 라이브러리 추정(KRX 미공표) → 화면 안내. 지급일이 2028년으로 넘어가는 2027년 12월 예상 회차 125건은 추측하지 않고 제외. 2028년 이후 예상 없음(안내 표시)
- 권리·경계: 권리수량 = 기존 entitlement(배당락일 전 매수분). 예상 배당락일 ≤ 등록일 → 보류. 등록 전 지급 → 소급 없음
- 세금: 기존 ManagementTax.compute(계좌 유형·종목 분류) 그대로. 예상 회차는 회차 과세표준 자료가 없으므로 기존 규칙의 '자료 없음' 경로 적용(일반 해외형 15.4%, 국내 커버드콜 세전×18% 과세표준, 기타 100%×15.4%, ISA/연금저축/IRP 0)
- 표시: KRW 전용(승인 편차). 요약·차트·캘린더 만 단위 1자리, 상세 원 단위

## 달력 상태 (대표 결정 2026-10-14 후속)
- 연도별 status: account-uat/fd-calendar.json — 2026 이하 official(기존 krx_calendar) · 2027 estimated(기존 note_2027 라이브러리 추정) · 2028+ estimated(python-holidays 0.106 financial_holidays("XKRX"): 주말 제외 + 고정 공휴일 + 음력 설/추석 + 대체휴일 + 선거일 등)
- 지급일 라벨: 배당락일~지급일 구간의 모든 연도가 official이면 '예상(…공식 달력)', 하나라도 estimated면 '추정(…추정 휴일)' — 실제 지급일·기존 3,416건(공식 연도 산정)은 불변
- 2027-12 배당락 → 2028 지급 125건: 포함·전부 estimated
- 예상 배당락 범위: ~2028-12 (UI 연도 상한 2028). 달력 데이터는 2029까지 보유(연말 경계용)
- 재계산: account-uat/tools/fd_gen.py + tools/krx_official/<연도>.json 등록 → fd-calendar/fd-forecast 자동 갱신 (README 참고). 가상 공식 등록 시험: 2027 status official·지급일 121건 이동·라벨 2,085건 공식 전환

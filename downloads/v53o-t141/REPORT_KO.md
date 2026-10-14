# v53o-t141 보고서 — GrokBot 자체 검증

대표의 실화면 승인 전 상태입니다. '완료'나 최종 PASS가 아닙니다. 삼성 실기기는 NOT TESTED입니다.

- URL: https://archigon72.github.io/donnaemsae-194-test/account-uat/asset-hub.html · management.html · dividend.html
- 커밋: 52c18d1 (코드), 기준 a87175e. 태그 v53o-t141-52c18d1
- SW 캐시: dnmuat194-acct-uat-v53o-1

## 바꾼 것 (색만)
- 신규 8색 순서 적용:
  - 노랑 #FFC83D, 파랑 #56B9FF, 민트 #46E5AC, 핑크 #FF83AC, 라벤더 #B59AFF, 오렌지 #FFAA66, 아쿠아 #45DCE5, 연파랑 #83A5FF
  - 적용 위치: 자산 구성 도넛, 계좌 주요 종목 top5, 계좌별 비중(관리 구성 계좌 탭, 배당 계좌별 탭)
- 상태색 통일:
  - 완료 #56B9FF, 미래 예상 #FFC83D, 지급예정 #FF83AC, 배당락 #46E5AC
  - 적용 위치: 월별 막대, 캘린더 상태점, 배지, 범례
- GrokBot 선택 사항 (대표 확인 필요):
  - 입금 확인 필요: 회색조 #BBC9D5 → 라벤더 #B59AFF
  - 추정·주의: 살구 #E9B6A8 → 오렌지 #FFAA66
- 선택 버튼, 칩, 탭, 하단 내비 활성: 파랑 #56B9FF
- 기존 갈색, 탁한 녹색(#317C69 등), 회색조 강조색 제거. 잔존 0건 (스캔 결과)
- 캘린더의 다른 달 날짜칸에 있던 opacity 0.35를 제거함 (상태점이 어둡게 보이던 원인). 대신 날짜 글자만 흐린 글자색으로 구분함.
- 차트 요소(도넛, 막대, 상태점, top5 점)와 그 모든 조상: opacity 1, filter none, mix-blend normal

## 바꾸지 않은 것
- 네이비 배경, 레이아웃, 계산, 원장, 세금 정책
- FAB: #A7DEC9 바탕, #09251E 글자 그대로 (QA로 확인)
- 저장 버튼(주 버튼)의 #A7DEC9: 선택 버튼이 아니어서 유지. 바꿔야 하면 지시 바랍니다.
- 기타 #6B7280: 대표가 앞서 결정한 값이라 유지. 회색 계열이므로 바꿀지 확인 바랍니다.

## 시험 (HTTPS 빌드)

| 묶음 | 결과 |
|---|---|
| qa_t141 (신규: 색, 투명도·필터, 잔존 스캔, FAB 불변, 강제 새로고침 SW) | 117/117 PASS |
| qa_t140 | 61/61 PASS |
| qa_t138 | 37/37 PASS |
| uat_regress | 40/40 PASS |
| uat_new | 38/38 PASS |
| uat_vp | 37/37 PASS |
| func | 35/35 PASS |
| unit_t138 / unit1 / unit2 (로컬 node, 코드 동일) | 21 / 15 / 21 PASS |

기존 시험 사본(qa_t138, qa_t140, uat_regress)에서 바꾼 것은 기대값뿐임: 구 팔레트 → 신규 8색·상태색, SW 이름 → v53o-1. 원본 시험 스크립트는 수정하지 않음.

## 제출물
- computed-color 표: COLOR_TABLE_KO.md (BEFORE/AFTER, 98행, 불일치 0)
- 실화면 BEFORE/AFTER 360/390/430: captures/
  - 대상 화면: hub, donut, acctshare, management, bar, fdacct, calendar
  - 각각 화면 상단(_top)과 전체(_full) 캡처
- 차트 BEFORE/AFTER: charts/
  - 도넛, 막대, top5, 계좌 구성
  - 배당 계좌별 차트(fdacct)는 AFTER만 있음 (BEFORE 촬영 시점에는 캡처 대상에 없었음)

## NOT TESTED
- 삼성 실기기와 삼성 인터넷 브라우저
- iOS Safari
- 사람 눈으로 보는 색 인상과 명암 (대표 실화면 판정 대기)

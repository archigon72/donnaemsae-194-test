# 신규 8색 computed-color 표 (HTTPS, GrokBot 자체 검증)

신규 8색 순서: #FFC83D · #56B9FF · #46E5AC · #FF83AC · #B59AFF · #FFAA66 · #45DCE5 · #83A5FF

상태색: 완료=#56B9FF, 미래 예상=#FFC83D, 지급예정=#FF83AC, 배당락=#46E5AC. 입금 확인 필요(#B59AFF)와 추정(#FFAA66)은 회색조·갈색조를 빼기 위해 GrokBot이 신규 8색 안에서 고른 것이며 대표 확인이 필요함.

"투명도·필터"는 요소 자신과 모든 조상의 opacity 곱, filter, mix-blend-mode를 확인한 값.

| 화면 | 폭 | 요소 | BEFORE computed | AFTER computed | 기대 | 투명도·필터(AFTER) | 판정 |
|---|---|---|---|---|---|---|---|
| hub | 360 | top5 색점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| hub | 360 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| hub | 360 | FAB 바탕 | `#A7DEC9` | `#A7DEC9` | `#A7DEC9 (FAB 불변)` | - | PASS |
| hub | 390 | top5 색점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| hub | 390 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| hub | 390 | FAB 바탕 | `#A7DEC9` | `#A7DEC9` | `#A7DEC9 (FAB 불변)` | - | PASS |
| hub | 430 | top5 색점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| hub | 430 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| hub | 430 | FAB 바탕 | `#A7DEC9` | `#A7DEC9` | `#A7DEC9 (FAB 불변)` | - | PASS |
| donut | 360 | 도넛 조각 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| donut | 360 | 범례 점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| donut | 360 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| donut | 390 | 도넛 조각 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| donut | 390 | 범례 점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| donut | 390 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| donut | 430 | 도넛 조각 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| donut | 430 | 범례 점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| donut | 430 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| acctshare | 360 | 도넛 조각 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| acctshare | 360 | 범례 점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| acctshare | 360 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| acctshare | 390 | 도넛 조각 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| acctshare | 390 | 범례 점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| acctshare | 390 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| acctshare | 430 | 도넛 조각 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| acctshare | 430 | 범례 점 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| acctshare | 430 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| fdacct | 360 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| fdacct | 360 | 계좌별 비중 막대 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| fdacct | 390 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| fdacct | 390 | 계좌별 비중 막대 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| fdacct | 430 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| fdacct | 430 | 계좌별 비중 막대 | `#9DCFF3 #A7DEC9 #F5D39A #D1B9EE` | `#FFC83D #56B9FF #46E5AC #FF83AC` | `#FFC83D #56B9FF #46E5AC #FF83AC` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 막대 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 막대 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 막대 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 막대 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 상태점 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 상태점 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 상태점 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 상태점 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| bar | 360 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| bar | 390 | 막대 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 막대 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 막대 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 막대 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 상태점 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 상태점 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 상태점 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 상태점 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| bar | 390 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| bar | 430 | 막대 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 막대 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 막대 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 막대 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 상태점 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 상태점 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 상태점 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 상태점 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| bar | 430 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| calendar | 360 | 상태점 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| calendar | 360 | 상태점 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| calendar | 360 | 상태점 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| calendar | 360 | 상태점 배당락 | `#97DFCA` | `#46E5AC` | `#46E5AC` | opacity 1 · filter none · blend normal | PASS |
| calendar | 360 | 상태점 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| calendar | 360 | 선택 버튼 글자 | `#A7DEC9 #EFF6F8` | `#56B9FF` | `#56B9FF` | - | PASS |
| calendar | 390 | 상태점 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| calendar | 390 | 상태점 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| calendar | 390 | 상태점 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| calendar | 390 | 상태점 배당락 | `#97DFCA` | `#46E5AC` | `#46E5AC` | opacity 1 · filter none · blend normal | PASS |
| calendar | 390 | 상태점 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| calendar | 390 | 선택 버튼 글자 | `#A7DEC9 #EFF6F8` | `#56B9FF` | `#56B9FF` | - | PASS |
| calendar | 430 | 상태점 완료 | `#9DCFF3` | `#56B9FF` | `#56B9FF` | opacity 1 · filter none · blend normal | PASS |
| calendar | 430 | 상태점 예상 | `#F5D39A` | `#FFC83D` | `#FFC83D` | opacity 1 · filter none · blend normal | PASS |
| calendar | 430 | 상태점 지급예정 | `#F0B9D0` | `#FF83AC` | `#FF83AC` | opacity 1 · filter none · blend normal | PASS |
| calendar | 430 | 상태점 배당락 | `#97DFCA` | `#46E5AC` | `#46E5AC` | opacity 1 · filter none · blend normal | PASS |
| calendar | 430 | 상태점 확인 필요 | `#BBC9D5` | `#B59AFF` | `#B59AFF` | opacity 1 · filter none · blend normal | PASS |
| calendar | 430 | 선택 버튼 글자 | `#A7DEC9 #EFF6F8` | `#56B9FF` | `#56B9FF` | - | PASS |
| management | 360 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| management | 360 | FAB 바탕 | `#A7DEC9` | `#A7DEC9` | `#A7DEC9 (FAB 불변)` | - | PASS |
| management | 390 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| management | 390 | FAB 바탕 | `#A7DEC9` | `#A7DEC9` | `#A7DEC9 (FAB 불변)` | - | PASS |
| management | 430 | 선택 버튼 글자 | `#A7DEC9` | `#56B9FF` | `#56B9FF` | - | PASS |
| management | 430 | FAB 바탕 | `#A7DEC9` | `#A7DEC9` | `#A7DEC9 (FAB 불변)` | - | PASS |

불일치 0건.

구 강조색 잔존 스캔: 각 화면에서 보이는 모든 요소의 color, background, border, fill, stroke, outline, background-image를 확인함. 구 파스텔(9DCFF3·F5D39A·F0B9D0·97DFCA·D1B9EE·B6D6AB·BBC9D5·A8C8EB·E9B6A8), 탁한 녹색 317C69·294B43, 갈색 6C5343·E4BF9D, fd.css 구 원색(F5B93A·3D8BFF·FF6F91) 잔존 0건 (qa_t141.json의 잔존 0 항목, 360/390/430 × 7화면).

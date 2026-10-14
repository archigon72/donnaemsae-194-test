# '+ 거래 등록' FAB 단계별 터치 증거 (HTTPS, GrokBot 자체 검증)

측정: Playwright + Chrome, 모바일 뷰포트 360/390/430, 터치 에뮬레이션, 대상 asset-hub.html (내 자산보기).

| 폭 | FAB 위치(x,y,w,h) | 하단 내비 y | 겹침 | 중심점 최상단 | 1 탭 | 2 모달(FAB 숨김) | 3 닫기→복귀 | 탭 전환 후 유지 | 판정 |
|---|---|---|---|---|---|---|---|---|---|
| 360 | 234,616,110×48 | 679 | 0 | PASS | PASS | PASS | PASS | PASS | PASS |
| 390 | 264,720,110×48 | 778 | 0 | PASS | PASS | PASS | PASS | PASS | PASS |
| 430 | 304,808,110×48 | 859 | 0 | PASS | PASS | PASS | PASS | PASS | PASS |

캡처 파일: `fab/<폭>_fab_1_before_tap.png`, `fab/<폭>_fab_2_modal.png`, `fab/<폭>_fab_3_closed_return.png`

- 탭하면 기존 거래 등록 모달(`data-action="trade"`, 관리 화면과 같은 흐름)이 열림. 새 흐름은 만들지 않았음.
- 계좌 추가와 분리됨: 허브의 FAB는 거래 등록 하나뿐이고, 계좌 추가는 기존 위치 그대로임.
- 콘텐츠가 가려지지 않도록 페이지 하단 여백 150px을 추가함.

NOT TESTED
- 실제 화면 키보드 표시 시 겹침: 에뮬레이터로는 소프트 키보드를 재현할 수 없음. 모달이 열려 있는 동안 FAB가 숨는 것까지만 확인함.
- 실기기 safe-area(노치/제스처 바) 하단 여백
- 삼성 실기기와 삼성 인터넷 브라우저

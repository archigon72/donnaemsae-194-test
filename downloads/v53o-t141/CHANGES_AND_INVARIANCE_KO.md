# 변경과 불변 (GrokBot 자체 검증)

기준: a87175e
코드 커밋: 52c18d1

## 변경 파일 (모두 account-uat/)
- uat-t141.css (신규, 마지막에 로드)
  - 상태 토큰과 .fd 차트 변수 재정의
  - t140 팔레트에서 구 강조색이 들어 있는 규칙만 신규색으로 복제 (209규칙, 277곳)
  - 선택 버튼 색
  - 차트 opacity/filter/blend 고정
  - 다른 달 날짜칸 투명도 제거
- management-view.js: PAL을 신규 8색으로 교체, 강조 리터럴 10곳 교체
- fd-view.js: PAL을 신규 8색으로 교체
- asset-hub.html, management.html, dividend.html: uat-t141.css 연결
- uat-sw.js: 캐시 v53o-1, uat-t141.css 사전 캐시
- UAT_BUILD_INFO.json: t141 항목

## 불변
- 레이아웃, 계산, 원장 키 dnmuat194.management.facts.v1, 세금 정책, FAB
- auto-test/latest.json 82d63c89…: HTTPS에서 재확인
- account-uat/와 downloads/ 밖 변경 0
- 백업 공개 업로드 0

# 변경 파일과 불변 확인 (GrokBot 자체 검증)

기준: 9d8261e (v53m-t138)
변경 커밋: 83becb1 (t140), 88e8514 (t140b: 3-B 부위별 역할 고정, SW v53n-2)

## 변경 파일 (모두 account-uat/ 안)
- account-uat/asset-hub.html: t140 팔레트·t138 CSS/JS·t140 CSS 연결. 이전에는 asset-hub에 t138 자산이 빠져 있어 라벨이 "키움 IRP(IRP)"로 보였고 팔레트도 적용되지 않았음.
- account-uat/management.html, account-uat/dividend.html: CSS 연결.
- account-uat/management-view.js:
  - 계좌 주요 종목 top5 카드 추가
  - compData에 범위 필터와 평가액 강제 옵션 추가
  - 기타 색 #6B7280
  - 허브 FAB 추가
  - JS 안 리터럴 색 21개를 승인 토큰으로 변경
- account-uat/uat-t140-palette.css (신규): 기존 CSS의 리터럴 색을 가장 가까운 역할의 승인 토큰으로 바꾼 오버라이드 405규칙. 보조 글자 15곳은 3-B에 맞춰 text-muted로 보정함. 신규 색은 없음.
- account-uat/uat-t140.css (신규): FAB, 계좌 추가, 주 버튼, top5 카드 스타일과 3-B 역할 고정(카드 테두리=border, 선택 탭=raised+primary, 보조 글자=muted).
- account-uat/uat-sw.js: 캐시 이름 dnmuat194-acct-uat-v53n-2, 신규 파일 사전 캐시.
- account-uat/UAT_BUILD_INFO.json: t140 항목.

## 불변
- 원장 키 dnmuat194.management.facts.v1: 변경 없음 (스토리지 구조 변경 없음, 이행 불필요)
- auto-test/latest.json sha256 82d63c8923200cb8e3fecdab828b27f6abfa17afd26a53a4834d5dbd7d5fc39d: 변경 없음 (HTTPS에서 재확인)
- 메인 사이트, /auto-test/, CORE, 194 목록·메타, 세금·계좌 정책, 실제 원장: 변경 0 (9d8261e..HEAD에서 account-uat/와 downloads/ 밖 변경 0)
- archigon72/donnaemsae-lab: 접근 없음
- 직접투자 원가 표시(내가 넣은 돈 · 직접투자 취득원가): 유지됨 (QA에서 확인)
- 백업 ZIP 공개 저장소 업로드: 0건

# t144 보고서 — 삼성 인터넷 강제 다크 대응 (GrokBot 자체 검증)

- 배포 커밋: 32086a5 (기준 t143 9336df3), SW 캐시 dnmuat194-acct-uat-v53r-1
- 변경 파일(account-uat): asset-hub.html, management.html, dividend.html, color-check.html, uat-sw.js, UAT_BUILD_INFO.json, 신규 uat-t144.css, uat-t144.js
- 원장·CORE·계산·세금·레이아웃 변경 없음. t143 검색창 개선·저장 버튼 #56B9FF 유지.

## 원인과 대응
1. 삼성 인터넷의 '웹 콘텐츠에 어두운 화면 모드 강제 적용'이 켜져 있으면 color-scheme / prefers-color-scheme 를 무시하고 색 필터를 씌움 (MDN browser-compat-data #29347 현장 보고; Samsung Developer 블로그 2020-12-15 "Dark Mode in Samsung Internet").
   → CSS 선언만으로는 막는다고 단정할 수 없음. `color-scheme: only dark`는 보조 선언으로만 유지(강제 적용 OFF·크롬 계열에서 재변환 방지).
2. 삼성 인터넷 야간/다크 모드는 CSS 배경·텍스트·SVG·비트맵에 필터를 적용하지만 canvas·video는 필터 대상이 아님 (ctrl.blog "Everything you need to know about Night mode in Samsung Internet").
   → uat-t144.js 가 도넛(SVG 조각)·월별/계좌별 막대·범례 점·상태 점·저장 버튼 바탕을 같은 HEX로 canvas에 덧그림. 색 값은 기존 코드가 계산한 값을 그대로 읽음.
3. 한계: 글자·입력창·일반 버튼·배경(네이비)은 여전히 삼성 필터 대상. 네이비 배경은 이미 어두워 변화가 작을 것으로 예상하나 실기기 미확인. 저장 버튼 글자(#081521)는 필터로 밝게 바뀔 수 있음(대비 저하 위험).

## 검증 (프록시 = Chromium Auto Dark, 삼성 실제 필터 아님)
- 도넛·월별 막대 픽셀: 360/390/430/1024/1280/1440 × 일반/프록시 다크 모두 승인 HEX와 차이 0.
- 주의: 프록시는 t143에서도 색을 바꾸지 않았음 → 프록시 PASS는 삼성 문제 해결의 증거가 아님.
- 회귀(HTTPS): qa_t144 121/121, qa_t142 15/15, qa_t141 117/117, qa_t140 61/61, qa_t138 37/37, uat_regress 40/40, uat_vp 37/37, uat_new 38/38, qa_t143 70/82 (실패 12건은 모두 'meta=dark' 정확일치 단언 → t144에서 'only dark'로 의도 변경).
- t143 HTTPS(수정 전): uat_regress 40/40, uat_vp 37/37, qa_t138 37/37.

## NOT TESTED
- 삼성 인터넷 실기기 강제 다크(재현 불가), 삼성 실기기 전반, iOS Safari.
- 실기기 확인: color-check.html 에서 C줄(canvas)이 표기 색처럼 밝은지 확인.

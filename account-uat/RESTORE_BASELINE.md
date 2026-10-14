# 기준선 복구 매뉴얼 (GrokBot 자체 검증)
- 최종 기준선 태그: `v53h-final-96bd93f` → 커밋 96bd93f (test_control=none), v5.3h 안정화 e071f33 포함
- 자동화 latest: auto-20261014-181446-live (latest.json sha256 82d63c89…)
- 복구(되돌리기 커밋, 강제 푸시 금지): `git checkout -b restore v53h-final-96bd93f` 후 필요 파일만 `git checkout v53h-final-96bd93f -- <경로>` → 일반 커밋/푸시
- UAT 제거: `git rm -r account-uat` → 일반 커밋 (메인/auto-test 영향 없음)
- 백업 ZIP(공개 범위만): baseline_617a6b3 a3927132…(2103), workcopy e261fe02…(2105), completed_e071f33 8a27e209…(2105) — 작업 박스 /workspace/v53h/backups 보관, 공개 업로드 안 함

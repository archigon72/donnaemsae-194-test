# 백업 분할본·SHA·복원 테스트
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 상태: v5.3 개발 후보(추가 수정).

| 분할본 | bytes | SHA-256 |
|---|---|---|
| donnaemsae-194-test_v5.3a_16ecc2d.zip.part00 (채팅 첨부 전달) | 15000000 | 24f088630a3e5b841758a8d198fe20c6a9cb11057dca12ea8c5b2f085bd68da7 |
| donnaemsae-194-test_v5.3a_16ecc2d.zip.part01 (채팅 첨부 전달) | 15000000 | 516104eb3be47ae738dc431be47c18277c9a2f8fd75c1a1aa5197a8754c32ddb |
| donnaemsae-194-test_v5.3a_16ecc2d.zip.part02 (채팅 첨부 전달) | 253512 | 5275279e72c8532eb01a194137cde40fc1151b3104c9eda7a467ccb14e41877a |

- 전체 ZIP SHA: [FULL_ZIP_SHA256.txt](FULL_ZIP_SHA256.txt) · 파일별 SHA(530): [FILES_SHA256.txt](FILES_SHA256.txt)
- 복원 스크립트: [restore.sh.txt](restore.sh.txt) · 복원 안내: [RESTORE_KO.txt](RESTORE_KO.txt)
- 복원 테스트 로그(분할본 결합→ZIP SHA 확인→무결성→해제→530개 SHA 일치): [RESTORE_TEST_LOG.txt](RESTORE_TEST_LOG.txt)
- 결과: ALL 530 FILES OK

※ 2026-10-14 대표 승인: 백업 ZIP part 파일은 공개 GitHub에서 삭제했습니다. part는 채팅 첨부로만 전달하며, 이 문서의 SHA-256로 검증합니다. (git 이력에는 남아 있음)

# 백업 분할본·SHA·복원 테스트
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 상태: v5.3 개발 후보(마무리 수정).

| 분할본 | bytes | SHA-256 |
|---|---|---|
| [donnaemsae-194-test_v5.3b_8da64ac.zip.part00](../../donnaemsae-194-test_v5.3b_8da64ac.zip.part00) | 15000000 | 45e4cdc7d0ef28848430ffbe83dfc146b4fcdec0f01d9ca907dc05260feae2a2 |
| [donnaemsae-194-test_v5.3b_8da64ac.zip.part01](../../donnaemsae-194-test_v5.3b_8da64ac.zip.part01) | 15000000 | 9602aa2c723779f6f013743fae37ab451aa6048df6c9aebdf7ee6fddff0a5a03 |
| [donnaemsae-194-test_v5.3b_8da64ac.zip.part02](../../donnaemsae-194-test_v5.3b_8da64ac.zip.part02) | 253699 | b3abffc8227780cd9d24416c91e7a5c8c438e642528f4166fc5ee12223e83995 |

- 전체 ZIP SHA: [FULL_ZIP_SHA256.txt](FULL_ZIP_SHA256.txt) · 파일별 SHA(530): [FILES_SHA256.txt](FILES_SHA256.txt)
- 복원 스크립트: [restore.sh.txt](restore.sh.txt) · 복원 안내: [RESTORE_KO.txt](RESTORE_KO.txt)
- 복원 테스트 로그(분할본 결합→ZIP SHA 확인→무결성→해제→530개 SHA 일치): [RESTORE_TEST_LOG.txt](RESTORE_TEST_LOG.txt)
- 결과: ALL 530 FILES OK

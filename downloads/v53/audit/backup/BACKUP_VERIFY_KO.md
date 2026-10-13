# 백업 분할본·SHA·복원 테스트
> 확인 주체: GrokBot 자체 검증(self-verification). 비서실장 독립 검수 결과가 아님. 상태: v5.3 개발 후보.

| 분할본 | bytes | SHA-256 |
|---|---|---|
| [donnaemsae-194-test_v5.3_ed66d27.zip.part00](../../donnaemsae-194-test_v5.3_ed66d27.zip.part00) | 15000000 | b3f03c9ec54ca7d8bf9894abb1965ee5552b685cf1de21551e785e66852deb13 |
| [donnaemsae-194-test_v5.3_ed66d27.zip.part01](../../donnaemsae-194-test_v5.3_ed66d27.zip.part01) | 15000000 | 0658958127d85ed48a287fcdbd86dc3064f5f66148682605040988bca93eafbb |
| [donnaemsae-194-test_v5.3_ed66d27.zip.part02](../../donnaemsae-194-test_v5.3_ed66d27.zip.part02) | 251048 | 65b6b80f2bfc426e41d5c876c328458af7851da28ad9c402c831581b50a814ce |

- 전체 ZIP SHA: [FULL_ZIP_SHA256.txt](FULL_ZIP_SHA256.txt) · 파일별 SHA(530): [FILES_SHA256.txt](FILES_SHA256.txt)
- 복원 스크립트: [restore.sh.txt](restore.sh.txt) · 복원 안내: [RESTORE_KO.txt](RESTORE_KO.txt)
- 복원 테스트 로그(분할본 결합→ZIP SHA 확인→무결성→해제→530개 SHA 일치): [RESTORE_TEST_LOG.txt](RESTORE_TEST_LOG.txt)
- 결과: ALL 530 FILES OK

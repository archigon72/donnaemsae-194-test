# HEX vs computed style (HTTPS, GrokBot 자체 검증)

승인 HEX는 DIRECTIVE_COLOR_LOCKED.txt 3-A/3-B 기준. 지정 HEX가 있으면 정확 일치로 판정하고, 없으면(투명 배경 등) 승인 집합에 드는지로 판정함. 측정 경로: HTTPS, 360/390/430, 허브·허브 강제 새로고침·관리 화면.

| 화면 | 폭 | 항목 | computed | 3-B 지정 HEX | 승인 토큰 | 판정 |
|---|---|---|---|---|---|---|
| hub | 360 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub | 360 | hero/card bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub | 360 | card border | `#385465` | `#385465` | --fd-border | PASS |
| hub | 360 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 360 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 360 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 360 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 360 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| hub | 360 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 360 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 360 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 360 | top5 row bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 360 | top5 rank1 swatch | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub | 360 | top5 rank2 swatch | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 360 | top5 rank3 swatch | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub | 360 | top5 rank4 swatch | `#D1B9EE` | `#D1B9EE` | 원형4 | PASS |
| hub | 360 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub | 360 | scope select bg | `#102638` | `#102638` | --fd-surface | PASS |
| hub | 360 | scope select text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 360 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub | 360 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| hub | 360 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 360 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| hub | 360 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| hub | 360 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 360 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 360 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| hub | 360 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 360 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| hub | 360 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub | 360 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub | 360 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| hub | 360 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| hub | 360 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| hub | 360 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| hub | 360 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| hub | 360 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| hub | 390 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub | 390 | hero/card bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub | 390 | card border | `#385465` | `#385465` | --fd-border | PASS |
| hub | 390 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 390 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 390 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 390 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 390 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| hub | 390 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 390 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 390 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 390 | top5 row bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 390 | top5 rank1 swatch | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub | 390 | top5 rank2 swatch | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 390 | top5 rank3 swatch | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub | 390 | top5 rank4 swatch | `#D1B9EE` | `#D1B9EE` | 원형4 | PASS |
| hub | 390 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub | 390 | scope select bg | `#102638` | `#102638` | --fd-surface | PASS |
| hub | 390 | scope select text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 390 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub | 390 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| hub | 390 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 390 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| hub | 390 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| hub | 390 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 390 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 390 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| hub | 390 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 390 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| hub | 390 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub | 390 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub | 390 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| hub | 390 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| hub | 390 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| hub | 390 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| hub | 390 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| hub | 390 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| hub | 430 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub | 430 | hero/card bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub | 430 | card border | `#385465` | `#385465` | --fd-border | PASS |
| hub | 430 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 430 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 430 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 430 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 430 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| hub | 430 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 430 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 430 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 430 | top5 row bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 430 | top5 rank1 swatch | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub | 430 | top5 rank2 swatch | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 430 | top5 rank3 swatch | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub | 430 | top5 rank4 swatch | `#D1B9EE` | `#D1B9EE` | 원형4 | PASS |
| hub | 430 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub | 430 | scope select bg | `#102638` | `#102638` | --fd-surface | PASS |
| hub | 430 | scope select text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 430 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub | 430 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| hub | 430 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub | 430 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| hub | 430 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| hub | 430 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub | 430 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub | 430 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| hub | 430 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub | 430 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| hub | 430 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub | 430 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub | 430 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| hub | 430 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| hub | 430 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| hub | 430 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| hub | 430 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| hub | 430 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| hub_hardreload | 360 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub_hardreload | 360 | hero/card bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub_hardreload | 360 | card border | `#385465` | `#385465` | --fd-border | PASS |
| hub_hardreload | 360 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 360 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 360 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 360 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 360 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| hub_hardreload | 360 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 360 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 360 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 360 | top5 row bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 360 | top5 rank1 swatch | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub_hardreload | 360 | top5 rank2 swatch | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 360 | top5 rank3 swatch | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub_hardreload | 360 | top5 rank4 swatch | `#D1B9EE` | `#D1B9EE` | 원형4 | PASS |
| hub_hardreload | 360 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub_hardreload | 360 | scope select bg | `#102638` | `#102638` | --fd-surface | PASS |
| hub_hardreload | 360 | scope select text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 360 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub_hardreload | 360 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| hub_hardreload | 360 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 360 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| hub_hardreload | 360 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| hub_hardreload | 360 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 360 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 360 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| hub_hardreload | 360 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 360 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| hub_hardreload | 360 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub_hardreload | 360 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub_hardreload | 360 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| hub_hardreload | 360 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| hub_hardreload | 360 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| hub_hardreload | 360 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| hub_hardreload | 360 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| hub_hardreload | 360 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| hub_hardreload | 390 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub_hardreload | 390 | hero/card bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub_hardreload | 390 | card border | `#385465` | `#385465` | --fd-border | PASS |
| hub_hardreload | 390 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 390 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 390 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 390 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 390 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| hub_hardreload | 390 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 390 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 390 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 390 | top5 row bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 390 | top5 rank1 swatch | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub_hardreload | 390 | top5 rank2 swatch | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 390 | top5 rank3 swatch | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub_hardreload | 390 | top5 rank4 swatch | `#D1B9EE` | `#D1B9EE` | 원형4 | PASS |
| hub_hardreload | 390 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub_hardreload | 390 | scope select bg | `#102638` | `#102638` | --fd-surface | PASS |
| hub_hardreload | 390 | scope select text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 390 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub_hardreload | 390 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| hub_hardreload | 390 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 390 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| hub_hardreload | 390 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| hub_hardreload | 390 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 390 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 390 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| hub_hardreload | 390 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 390 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| hub_hardreload | 390 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub_hardreload | 390 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub_hardreload | 390 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| hub_hardreload | 390 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| hub_hardreload | 390 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| hub_hardreload | 390 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| hub_hardreload | 390 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| hub_hardreload | 390 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| hub_hardreload | 430 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub_hardreload | 430 | hero/card bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub_hardreload | 430 | card border | `#385465` | `#385465` | --fd-border | PASS |
| hub_hardreload | 430 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 430 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 430 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 430 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 430 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| hub_hardreload | 430 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 430 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 430 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 430 | top5 row bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 430 | top5 rank1 swatch | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub_hardreload | 430 | top5 rank2 swatch | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 430 | top5 rank3 swatch | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub_hardreload | 430 | top5 rank4 swatch | `#D1B9EE` | `#D1B9EE` | 원형4 | PASS |
| hub_hardreload | 430 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| hub_hardreload | 430 | scope select bg | `#102638` | `#102638` | --fd-surface | PASS |
| hub_hardreload | 430 | scope select text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 430 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| hub_hardreload | 430 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| hub_hardreload | 430 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| hub_hardreload | 430 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| hub_hardreload | 430 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| hub_hardreload | 430 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| hub_hardreload | 430 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| hub_hardreload | 430 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| hub_hardreload | 430 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| hub_hardreload | 430 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| hub_hardreload | 430 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| hub_hardreload | 430 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| hub_hardreload | 430 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| hub_hardreload | 430 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| hub_hardreload | 430 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| hub_hardreload | 430 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| hub_hardreload | 430 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| hub_hardreload | 430 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| management | 360 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| management | 360 | hero/card bg | `#102638@0.9` | (지정 없음, 집합만) | --fd-surface | PASS |
| management | 360 | card border | `#385465` | `#385465` | --fd-border | PASS |
| management | 360 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 360 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 360 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 360 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 360 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| management | 360 | 계좌추가 bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 360 | 계좌추가 border | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 360 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 360 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 360 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 360 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| management | 360 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| management | 360 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| management | 360 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 360 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| management | 360 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| management | 360 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 360 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 360 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| management | 360 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 360 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| management | 360 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| management | 360 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| management | 360 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| management | 360 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| management | 360 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| management | 360 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| management | 360 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| management | 360 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| management | 390 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| management | 390 | hero/card bg | `#102638@0.9` | (지정 없음, 집합만) | --fd-surface | PASS |
| management | 390 | card border | `#385465` | `#385465` | --fd-border | PASS |
| management | 390 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 390 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 390 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 390 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 390 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| management | 390 | 계좌추가 bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 390 | 계좌추가 border | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 390 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 390 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 390 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 390 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| management | 390 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| management | 390 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| management | 390 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 390 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| management | 390 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| management | 390 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 390 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 390 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| management | 390 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 390 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| management | 390 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| management | 390 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| management | 390 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| management | 390 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| management | 390 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| management | 390 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| management | 390 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| management | 390 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |
| management | 430 | body bg | `#081521` | `#081521` | --fd-bg | PASS |
| management | 430 | hero/card bg | `#102638@0.9` | (지정 없음, 집합만) | --fd-surface | PASS |
| management | 430 | card border | `#385465` | `#385465` | --fd-border | PASS |
| management | 430 | card text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 430 | h2 text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 430 | muted label | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 430 | FAB bg | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 430 | FAB text | `#09251E` | `#09251E` | 버튼글자 | PASS |
| management | 430 | 계좌추가 bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 430 | 계좌추가 border | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 430 | selected tab bg | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 430 | selected tab text | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 430 | unselected tab text | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 430 | bottom nav bg | `#000000@0` | (지정 없음, 집합만) | 투명 | PASS |
| management | 430 | --fd-bg | `#081521` | `#081521` | --fd-bg | PASS |
| management | 430 | --fd-surface | `#102638` | `#102638` | --fd-surface | PASS |
| management | 430 | --fd-surface-raised | `#193448` | `#193448` | --fd-surface-raised | PASS |
| management | 430 | --fd-surface-soft | `#213B4B` | `#213B4B` | --fd-surface-soft | PASS |
| management | 430 | --fd-border | `#385465` | `#385465` | --fd-border | PASS |
| management | 430 | --fd-text | `#EFF6F8` | `#EFF6F8` | --fd-text | PASS |
| management | 430 | --fd-text-muted | `#AEC0CB` | `#AEC0CB` | --fd-text-muted | PASS |
| management | 430 | --fd-text-subtle | `#8CA4B3` | `#8CA4B3` | --fd-text-subtle | PASS |
| management | 430 | --fd-primary | `#A7DEC9` | `#A7DEC9` | --fd-primary, 원형2 | PASS |
| management | 430 | --fd-primary-strong | `#317C69` | `#317C69` | --fd-primary-strong | PASS |
| management | 430 | --fd-complete | `#9DCFF3` | `#9DCFF3` | --fd-complete, 원형1 | PASS |
| management | 430 | --fd-expected | `#F5D39A` | `#F5D39A` | --fd-expected, 원형3 | PASS |
| management | 430 | --fd-scheduled | `#F0B9D0` | `#F0B9D0` | --fd-scheduled, 원형5 | PASS |
| management | 430 | --fd-exdate | `#97DFCA` | `#97DFCA` | --fd-exdate | PASS |
| management | 430 | --fd-unconfirmed | `#BBC9D5` | `#BBC9D5` | --fd-unconfirmed, 원형7 | PASS |
| management | 430 | --fd-warning | `#E9B6A8` | `#E9B6A8` | --fd-warning | PASS |
| management | 430 | --fd-error | `#E9A8B1` | `#E9A8B1` | --fd-error | PASS |
| management | 430 | --fd-focus | `#B4E3FC` | `#B4E3FC` | --fd-focus | PASS |

불일치 0건.

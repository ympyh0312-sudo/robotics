# tb3_sandbox 지도 (Nav2)

이 폴더의 `tb3_sandbox.pgm`, `tb3_sandbox.yaml` 은 수정하지 않은 원본이다.

| 항목 | 내용 |
|---|---|
| 출처 | https://github.com/ros-navigation/navigation2 (`jazzy` 브랜치) |
| 경로 | `nav2_bringup/maps/tb3_sandbox.{pgm,yaml}` |
| 커밋 | `94d1c2a345dda6ff637e6a72c9101d927ee99f19` |
| 저작권자 | Nav2 project contributors |
| 라이선스 | Apache-2.0 (`nav2_bringup/package.xml` 의 `<license>` 선언, Nav2 `LICENSE` 의 "표시 없는 파일은 Apache-2.0" 안내) |
| 라이선스 전문 | 이 패키지의 `../../LICENSE` (Apache License 2.0) |
| Nav2 LICENSE 원문 | `LICENSE.nav2` |
| sha256 (pgm) | `0103b9dfaa3b79592af71cc35d64f69cfbd3565d173160820ad8ef56cd27b3fc` |
| sha256 (yaml) | `2a284eba0a3aa4a904bce71734c56a543e979899f1cf34daad6e8215e608b438` |

## 수정 사항

원본은 그대로 두고, `scripts/prepare_map.py` 로 정리한 사본을 `maps/tb3_sandbox.*` 에 만들었다.
정리 내용은 벽의 틈 메우기(`--seal-unknown`)와 기둥 속 채우기(`--fill-holes 400`)이다.
`worlds/tb3_sandbox.sdf` 는 그 지도에서 `scripts/pgm_to_world.py` 로 생성한 파일이다.

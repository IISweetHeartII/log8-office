# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.1.0] — log8-office 첫 공개 배포 (First Public Release)

### Added

- **CC0 자체 제작 아트 전면 도입** (Full CC0 self-generated art replacement): `assets-gen/` 픽셀킷 툴킷으로 고양이 스프라이트·배경 타일·UI 버튼 전체를 직접 생성. 외부 아트팩 의존 없음 (All sprites, tiles, and UI buttons generated in-house via `assets-gen/` pixelkit — no external art pack dependency).
- **고양이 에이전트 8마리** (8 cat-avatar agents): 각 에이전트마다 개성 있는 고양이 아바타와 역할 배지 적용. 7가지 작업 상태(idle / talking / writing / researching / executing / syncing / error)에 따라 오피스 구역(라운지·책상·리서치 코너·서버랙·버그존 등)을 자동 이동 (Each agent has a distinct cat avatar and role badge; cats walk to the matching office zone based on live activity state).
- **한국어 우선 다국어 지원** (Korean-first i18n): 기본 언어 한국어, 영어·일본어·중국어(간체) 지원. 전체 UI 문자열을 `I18N` 객체로 중앙 관리 (Default locale Korean; English, Japanese, Simplified Chinese supported; all strings centralized in an `I18N` object in `index.html`).
- **Ark Pixel Font 다국어 픽셀 폰트 스택** (Ark Pixel Font multilingual pixel-font stack): SIL OFL 1.1 라이선스, CJK 포함 픽셀 렌더링 지원 (SIL OFL 1.1 license, covers CJK pixel rendering).
- **원클릭 에이전트 연동** (One-click agent integration): `office-agent-push.py` 스크립트 + `SKILL.md` Claude Code 스킬로 에이전트 오피스 입장·상태 푸시 자동화 (`office-agent-push.py` script and `SKILL.md` Claude Code skill for automated agent join/state-push).
- **스모크 테스트** (Smoke test): `scripts/smoke_test.py` — 주요 엔드포인트(/health · /status · /agents · /set_state)를 비파괴적으로 검증 (Non-destructive verification of key endpoints).
- **배경 세밀화** (Finer background): 오피스 배경 타일셋을 업스트림 대비 더 세밀한 해상도로 교체 (Office background tileset replaced with finer-resolution version compared to upstream).

### Changed

- **비상업 업스트림 에셋 교체** (Replaced non-commercial upstream art): ringhyacinth/Star-Office-UI의 비상업 라이선스 에셋 및 LimeZu 게스트 스프라이트를 CC0 자체 생성 에셋으로 전면 교체. 프로젝트 전체 상업적 이용 가능 (All non-commercial-licensed assets from the upstream and LimeZu guest sprites replaced with CC0 self-generated art — the full project is now commercially usable).
- **Flask 백엔드 구조 개선** (Flask backend restructured): 에이전트 관리·인증·상태 처리를 `*_utils.py` 모듈로 분리 (Agent management, auth, and state handling split into `*_utils.py` modules).

### Removed

- **중앙 "Star" 로봇 캐릭터 제거** (Removed central "Star" robot): 업스트림의 중심 마스코트 로봇 제거 (Upstream mascot robot removed).
- **하단 패널 및 데스크탑 래퍼 제거** (Removed bottom panels and desktop wrappers): 업스트림의 하단 정보 패널과 Electron 기반 데스크탑 래퍼 레이어 제거 (Upstream bottom info panels and Electron wrapper layer removed from default UI).
- **LimeZu 스프라이트 제거** (Removed LimeZu sprites): 비상업 외부 스프라이트 에셋 완전 제거 (All non-commercial external sprite assets removed).

---

[Unreleased]: https://github.com/IISweetHeartII/log8-office/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/IISweetHeartII/log8-office/releases/tag/v0.1.0

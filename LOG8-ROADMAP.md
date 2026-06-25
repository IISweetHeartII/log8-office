# log8-office — 로드맵 & 목표

> [`ringhyacinth/Star-Office-UI`](https://github.com/ringhyacinth/Star-Office-UI) 포크.
> **한국어 특화 + 다국어 + 완전무료 + 에이전트 원클릭 연동**으로 재배포하는 OSS 프로젝트.

## 🎯 비전 (원본 대비 차별점)

원본은 좋지만 (1) 中/英/日만 지원 (2) 이미지생성이 **Gemini 유료 API** 의존 (3) 에이전트 연동이 수동.
→ log8-office는:

1. **완전 무료** — 키 없이 셀프 이미지생성 (OAuth 기반 무료 스킬 번들)
2. **다국어 + 한국어 특화** — 깔끔한 i18n 구조, 한국어 1급 지원
3. **에이전트 원클릭 연동** — 상태 푸시를 재사용 가능한 스킬로

한 줄: **"키 없이 무료 + 내 언어로 + 내 에이전트 바로 입장하는 픽셀 사무실"**

## 🗺️ 단계별 목표 (Phase)

| Phase | 목표 | 상태 |
|---|---|---|
| ~~**P1. i18n 정비**~~ ✅ | ~~하드코딩 추출 → 언어팩. ko/en/ja~~ **완료**: ko 추가+기본, KO버튼, I18N 166키 parity, STATES/thoughts/transient 전부 i18n화, **Ark Pixel 4-팩 멀티스택**(ko/ja/zh/latin 전부 도트) | ✅ 완료 |
| ~~**P2. 완전 무료화**~~ ✅ | ~~Gemini 유료 의존 제거~~ → **CC0 자체 생성 아트** 전면 도입으로 외부 의존 근본 해결. Gemini 생성 기능은 키 없어도 기본 동작 | ✅ 완료 (assets-gen 신설) |
| ~~**P3. 에이전트 연동 스킬**~~ ✅ | ~~상태 푸시를 **재사용 SKILL.md**로 정리~~ **완료**: `office-agent-push.py` 환경변수화, `docs/AGENT-INTEGRATION.md` 다국어 가이드, `frontend/join-office-skill.md`, `agent-invite-template.txt` | ✅ 완료 |
| **P4. UI 개선** | 캐릭터 커스텀(아바타 연동), 모바일, 디자인 다듬기 | 진행 예정 |
| ~~**P5. OSS 재배포**~~ 진행 중 | README 3국어(ko/en/ja) 재작성, SKILL.md de-brand, .github/CONTRIBUTING/CODE_OF_CONDUCT/SECURITY, CI, 테마/커스터마이징 시스템, clean-history 공개 배포 | 🔄 진행 중 |

## ✅ 완료 — 라이선스 클린 & 자체 에셋 (2026-06-24)

원본의 발목을 잡던 **"미술 자산 비상업(non-commercial)"** 문제를 근본 해결:

- **전 미술 에셋(37개) 자체 생성 교체** → 100% 오리지널 **CC0**(상업 사용 자유). 원본 비상업 아트·LimeZu 게스트·고양이+랍스터 앱아이콘·구 스크린샷 전부 대체.
- **`assets-gen/` 생성 툴킷 신설** = 팔레트 테마 시스템. `pixelkit.py`(팔레트·픽셀 프리미티브·스프라이트 패커) + `gen_star/furniture/scene/brand.py`. 팔레트만 바꿔 사무실 전체 리스킨 가능.
- **테마 프리셋 4종** (`default`, `midnight`, `sakura`, `forest`) + `build.py --theme <이름> --install` 원스텝 적용.
- **치수/프레임 100% 호환**: 원본과 동일 치수라 Phaser 애니 프레임 수 자동 일치(검증: 치수 37/37, http 200 35/35, 참조 28/28, 누락 0).
- **폰트 정리**: desktop-pet의 비-OFL `ipix.ttf` 제거 → 번들 **Ark Pixel(OFL)** 로 교체. 이제 전 폰트 OFL.

→ 결과: **누구나 클론해서 상업적으로 써도 되는** 완전 자유 OSS 베이스 확보.

## ✅ 완료 — 8남매 고양이 에이전트 + 상태별 이동 (2026-06-24)

- **고양이 8마리 픽셀화**: rosie·navi·kkami·cheese·hermes·buffett·luna·gamjaring 아바타를 각자 색/특징대로 CC0 픽셀 스프라이트로 생성(`assets-gen/gen_cats.py` → `frontend/cat_<name>.webp` 8프레임 + `cat_<name>_role.png` 초상). gamjaring은 감자🥔.
- **이름→고양이 레지스트리**(`CAT_AGENTS`, 확장 가능): 에이전트 이름이 매칭되면 전용 고양이 스프라이트 사용.
- **상태별 이동 구현**: idle→휴게실(소파), writing/executing→책상, talking→미팅, researching→리서치 코너, syncing→서버랙, error→버그구역. 에이전트가 텔레포트 대신 **걸어서(walk tween)** 이동.

## ✅ 완료 — P3 에이전트 연동 + 전체 de-brand

- 푸시 스크립트 환경변수화(`OFFICE_URL/OFFICE_JOIN_KEY/OFFICE_AGENT_NAME`), 다국어 가이드 `docs/AGENT-INTEGRATION.md` + 입장 스킬 `frontend/join-office-skill.md` + 초대 템플릿. 원작자 브랜딩 게스트 표면 전부 제거, 간판 `log8 픽셀 오피스`.

## 🔄 진행 중 — P5 OSS 재배포 (2026-06-25 ~)

- README.md(ko) / README.en.md / README.ja.md 전면 재작성 — 정확한 프로젝트 사실 기반, 업스트림 내용 제거
- SKILL.md de-brand — 龙虾/ringhyacinth 참조 제거, 영/한 병기
- LOG8-ROADMAP.md P5 상태 반영
- .github/ 스캐폴딩 (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CI)
- clean-history 공개 배포 준비

## 📦 현재 상태

- **저장소**: `IISweetHeartII/log8-office` (main 브랜치)
- **프론트엔드**: `frontend/index.html` **단일 파일 5261줄** (HTML/CSS/JS/i18n/Phaser 게임 전부 인라인)
- **백엔드**: Flask (`backend/app.py` + `*_utils.py` 모듈). 의존성 = flask, pillow.

## 🛠️ 코드 지도

- **i18n**: `frontend/index.html`의 `const I18N` / `const BUBBLE_TEXTS` / `bubbleTextMapByLang`
- **상태 → 구역 매핑**: `backend/app.py`의 `STATE_TO_AREA_MAP`
- **멀티에이전트**: `/join-agent` · `/agent-push` · `/leave-agent` · `/agents`, `join-keys.json`, `office-agent-push.py`
- **아트 생성**: `assets-gen/` — `pixelkit.py`, `gen_*.py`, `build.py`, `themes/`

## ⚖️ 라이선스

- 코드: MIT
- 미술 에셋: CC0 1.0 (퍼블릭 도메인) — 상업 이용 가능
- 폰트 (Ark Pixel Font): SIL OFL 1.1

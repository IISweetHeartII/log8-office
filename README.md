# log8-office

**AI 에이전트의 실시간 작업 상태를 픽셀 고양이로 시각화하는 오피스 대시보드**

[English](README.en.md) | [日本語](README.ja.md)

---

![log8-office](docs/screenshots/cover.png)

픽셀 오피스에 고양이들이 모여 일합니다. 에이전트가 코딩 중이면 고양이가 책상으로 걸어가고, 리서치 중이면 리서치 코너로, 에러가 나면 버그존으로 이동합니다. 상태가 바뀔 때마다 고양이가 직접 걸어서 이동합니다.

OpenClaw · Claude Code · 그 어떤 AI 에이전트도 join key 하나로 입장 가능합니다. 상태 보드로만 써도 됩니다.

---

## ✨ 주요 특징

- **100% 오리지널 CC0 아트** — `assets-gen/`의 스크립트로 모든 픽셀 아트를 직접 생성합니다. 외부 아트팩 의존 없음. 상업적 이용 자유.
- **한국어 우선 다국어 지원** — 기본 언어 한국어, 영어·일본어·중국어(간체) 지원. 전체 UI를 다국어 Ark Pixel 픽셀 폰트로 렌더링.
- **고양이 8마리 + 상태별 구역 이동** — 에이전트의 활동 상태에 따라 고양이가 오피스 내 해당 구역으로 걸어서 이동.
- **원클릭 에이전트 연동** — `office-agent-push.py`와 join SKILL로 어떤 에이전트든 빠르게 입장.

---

## 🚀 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/IISweetHeartII/log8-office.git
cd log8-office

# 2. 가상환경 만들기 + 의존성 설치
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt

# 3. 백엔드 실행
.venv/bin/python backend/app.py
```

브라우저에서 http://127.0.0.1:19000 열기.

**상태 바꾸기 (별도 터미널)**

```bash
python3 set_state.py writing "문서 정리 중"
python3 set_state.py idle
```

유효한 상태값: `idle` / `talking` / `writing` / `researching` / `executing` / `syncing` / `error`

**프로덕션 배포 시**

`.env.example`을 `.env`로 복사하고 `FLASK_SECRET_KEY`와 `ASSET_DRAWER_PASS`를 강한 값으로 설정하세요.

**선택: 스모크 테스트**

```bash
python3 scripts/smoke_test.py --base-url http://127.0.0.1:19000
```

---

## 🐱 고양이와 오피스 구역

에이전트 상태가 바뀌면 고양이가 맞는 구역으로 걸어갑니다.

| 상태 | 오피스 구역 | 의미 |
|------|------------|------|
| `idle` | 라운지 (소파) | 대기 중 / 완료 |
| `talking` | 미팅 자리 | 주인과 대화 중 |
| `writing` | 책상 | 코딩 / 문서 작성 |
| `executing` | 책상 | 태스크 실행 중 |
| `researching` | 리서치 코너 | 검색 / 조사 중 |
| `syncing` | 서버랙 | 동기화 / 백업 중 |
| `error` | 버그 구역 | 에러 / 예외 발생 |

유의어는 서버에서 자동 정규화됩니다 (`working`→`writing`, `run`→`executing`, `chat`→`talking` 등).

---

## 🤝 멀티 에이전트 / 에이전트 연동

다른 에이전트를 오피스에 초대하려면:

1. `join-keys.sample.json`을 참고해 `join-keys.json`에 join key를 추가하세요.
2. 참여할 에이전트에게 3가지 환경변수로 `office-agent-push.py`를 실행하도록 안내합니다.

```bash
OFFICE_URL=http://127.0.0.1:19000 \
OFFICE_JOIN_KEY=ocj_xxx \
OFFICE_AGENT_NAME="my-agent" \
python3 office-agent-push.py
```

- `OFFICE_URL` — 오피스 주소 (기본값 `http://127.0.0.1:19000`)
- `OFFICE_JOIN_KEY` — 오피스 주인에게 받은 join key (`ocj_...`)
- `OFFICE_AGENT_NAME` — 오피스에서 표시될 이름

첫 실행 시 자동 입장(자동 승인)되며 ~15초마다 상태를 푸시합니다. `Ctrl+C`로 종료하면 자동 퇴장합니다.

전체 연동 가이드 (수동 HTTP, 모든 언어): **[docs/AGENT-INTEGRATION.md](docs/AGENT-INTEGRATION.md)**

---

## 🎨 외관 커스터마이징

모든 픽셀 아트는 팔레트 테마 시스템으로 리스킨할 수 있습니다.

**테마 프리셋** — `assets-gen/themes/` 폴더에 `default`, `midnight`, `sakura`, `forest` 네 가지 프리셋이 있습니다.

**테마 적용 (생성 + 설치)**

```bash
cd assets-gen
pip install pillow          # 처음 한 번만

python3 build.py --install                    # 기본 테마
python3 build.py --theme midnight --install   # midnight 테마
```

고양이 스프라이트는 `--cats` 플래그를 추가해 재생성합니다 (rembg 필요).

직접 팔레트를 수정하려면 `assets-gen/pixelkit.py`의 `PALETTE` 딕셔너리를 편집하세요. 자세한 내용은 [assets-gen/README.md](assets-gen/README.md).

---

## 📡 API

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/` | GET | 픽셀 오피스 UI |
| `/status` | GET | 메인 에이전트 상태 조회 |
| `/set_state` | POST | 메인 에이전트 상태 설정 `{"state":"writing","detail":"..."}` |
| `/agents` | GET | 전체 에이전트 목록 |
| `/join-agent` | POST | 에이전트 입장 `{"name":"...","joinKey":"...","state":"..."}` |
| `/agent-push` | POST | 상태 푸시 `{"agentId":"...","joinKey":"...","state":"..."}` |
| `/leave-agent` | POST | 에이전트 퇴장 `{"agentId":"..."}` |
| `/agent-approve` | POST | 에이전트 승인 (관리자) |
| `/agent-reject` | POST | 에이전트 거부 (관리자) |
| `/health` | GET | 헬스체크 |
| `/yesterday-memo` | GET | 어제 일지 조회 (선택적) |
| `/assets/list` | GET | 에셋 목록 |
| `/join` | GET | 에이전트 입장 페이지 |
| `/invite` | GET | 초대 안내 페이지 |

---

## ⚖️ 라이선스

| 구성 요소 | 라이선스 |
|-----------|---------|
| 코드 | MIT |
| 픽셀 아트 에셋 | CC0 1.0 (퍼블릭 도메인) — 상업적 이용 가능, 저작자 표시 불필요 |
| 폰트 (Ark Pixel Font) | SIL OFL 1.1 |

**전체 프로젝트가 상업적 이용 가능합니다.** 원본 Star Office UI(Ring Hyacinth & Simon Lee)의 비상업 아트는 이 포크에 포함되어 있지 않으며, 모든 아트 에셋은 `assets-gen/`의 스크립트로 자체 생성한 오리지널 작업물입니다.

---

## 🙏 크레딧

- 원본 [Star Office UI](https://github.com/ringhyacinth/Star-Office-UI) — Ring Hyacinth & Simon Lee (MIT 코드 기반)
- [Ark Pixel Font](https://github.com/TakWolf/ark-pixel-font) — TakWolf (SIL OFL 1.1)

---
name: log8-office
description: Deploy log8-office — a pixel-art AI office dashboard. Clone, install, run, and push agent state. / log8-office 픽셀 오피스 대시보드 배포 스킬 — 클론, 설치, 실행, 상태 푸시.
---

# log8-office Skill

This skill gets the pixel office running and connects your agent to it.
이 스킬은 픽셀 오피스를 실행하고 에이전트를 연결합니다.

---

## 1. Deploy / 배포

```bash
# Clone
git clone https://github.com/IISweetHeartII/log8-office.git
cd log8-office

# Install
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt

# Run (default port 19000)
.venv/bin/python backend/app.py
```

Open http://127.0.0.1:19000. / 브라우저에서 http://127.0.0.1:19000 열기.

---

## 2. Push your state / 상태 푸시

```bash
# In the project root
python3 set_state.py writing "작업 중"
python3 set_state.py idle
```

States / 상태값: `idle` `talking` `writing` `researching` `executing` `syncing` `error`

---

## 3. Join from another agent / 다른 에이전트 입장

Ask the office owner for a join key, then run:
오피스 주인에게 join key를 받아 실행:

```bash
OFFICE_URL=http://127.0.0.1:19000 \
OFFICE_JOIN_KEY=ocj_xxx \
OFFICE_AGENT_NAME="my-agent" \
python3 office-agent-push.py
```

The script auto-joins and pushes state every ~15 s. `Ctrl+C` leaves the office.
자동 입장 후 ~15초마다 상태 푸시. `Ctrl+C`로 퇴장.

---

## 4. Production hardening / 프로덕션 설정

```bash
cp .env.example .env
# Set strong values for:
#   FLASK_SECRET_KEY   (24+ chars)
#   ASSET_DRAWER_PASS  (8+ chars, not "1234")
```

---

## 5. Notes / 참고

- Only state + a short detail are sent — never task content. / 상태와 짧은 설명만 전송, 작업 내용 미전송.
- Optional Gemini API key enables AI background generation; the office works fully without it. / Gemini API 키는 선택 사항. 없어도 모든 기능 동작.
- Full agent integration guide: `docs/AGENT-INTEGRATION.md`

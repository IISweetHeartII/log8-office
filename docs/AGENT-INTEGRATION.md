# Agent Integration / 에이전트 연동

How any AI agent joins the pixel office and shows its live work state.
어떤 AI 에이전트든 픽셀 오피스에 입장해 실시간 작업 상태를 표시하는 방법.

> Only a **state** (`idle / writing / researching / executing / syncing / error`) and an
> optional short **detail** are sent — never task content or private data.
> 상태와 짧은 detail만 전송 — 작업 내용·프라이버시는 보내지 않습니다.

---

## TL;DR (1 minute)

```bash
OFFICE_URL=http://127.0.0.1:19000 \
OFFICE_JOIN_KEY=ocj_xxx \
OFFICE_AGENT_NAME="my-agent" \
python office-agent-push.py
```

The script auto-joins on first run, then pushes your current state every ~15s.
첫 실행 시 자동 입장 후 ~15초마다 현재 상태를 푸시합니다.

- `OFFICE_URL` — office address (default `http://127.0.0.1:19000`)
- `OFFICE_JOIN_KEY` — the join key (`ocj_...`) the office owner gave you
- `OFFICE_AGENT_NAME` — your display name in the office

It reads your live state from a local OpenClaw workspace if present, else defaults to
`idle`. To drive state manually, write `set_state.py <state> <detail>` or POST `/agent-push`.

---

## Manual HTTP flow (any language)

The push script is just a convenience wrapper around 3 endpoints. To integrate from
your own runtime, call them directly:

### 1. Join
```http
POST {OFFICE_URL}/join-agent
{ "name": "my-agent", "joinKey": "ocj_xxx", "state": "idle", "detail": "just joined" }
```
Returns `{ "agentId": "..." }`. Join keys can allow multiple concurrent agents
(`maxConcurrent` in `join-keys.json`).

### 2. Push state (loop, ~15–30s or on change)
```http
POST {OFFICE_URL}/agent-push
{ "agentId": "...", "joinKey": "ocj_xxx",
  "state": "writing", "detail": "optional short note", "name": "optional rename" }
```
Push your state whenever your activity changes — the cat walks to the matching zone:

| `state` | activity | office zone |
|---|---|---|
| `idle` | standby / done | lounge (sofa) |
| `talking` | talking with the owner | meeting spot (next to Star) |
| `writing` | coding / writing docs | desk |
| `executing` | running a task | desk |
| `researching` | searching / research | research corner |
| `syncing` | syncing / backup | server rack |
| `error` | error / exception | bug zone |

Synonyms are normalized server-side (e.g. `chat`/`meeting`→`talking`, `working`→`writing`,
`run`→`executing`, `search`→`researching`, `sync`→`syncing`). Unknown → `idle`.

### 3. Leave
```http
POST {OFFICE_URL}/leave-agent
{ "name": "my-agent" }
```

`GET {OFFICE_URL}/agents` returns the current visitor list (used by the office UI).

---

## Notes

- On `403` / "not authorized", stop pushing and re-request a join key.
- Default authorization lasts ~24h; re-join after it expires.
- The office owner manages keys in `join-keys.json` (see `join-keys.sample.json`).
- Ask your owner before joining: *"I'll periodically send my work state
  (idle/writing/...) to the office board for visualization — no task content, stoppable
  anytime. OK?"* / 입장 전 주인에게: *"작업 상태만 주기적으로 보내 시각화에 쓸게요(내용 미전송, 언제든 중단). 괜찮을까요?"*

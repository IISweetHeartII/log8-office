# Join the Office — Visitor Agent Skill / 오피스 입장 스킬

Give your agent a desk in the pixel office and show its live work state on the board.
에이전트에게 픽셀 오피스의 자리를 주고 실시간 작업 상태를 보드에 표시합니다.

## Prerequisites / 준비물
- A join key (`ocj_xxx`) from the office owner. / 오피스 주인에게 받은 join key.
- Owner's consent to broadcast your state. / 상태 전송에 대한 주인의 동의.
- Network access to the office URL. / 오피스 URL 접근 가능.

## Quick Start
### 1. Confirm consent with your owner / 주인에게 동의 확인
> "I'll periodically send my work state (idle/writing/researching/executing/syncing/error)
> to the office board — only the state word + a short note, no private content, stoppable
> anytime. OK?" / "작업 상태만 주기적으로 보낼게요(내용 미전송, 언제든 중단). 괜찮을까요?"

### 2. Download the pusher / 푸시 스크립트 다운로드
```bash
curl -o office-agent-push.py "$OFFICE_URL/static/office-agent-push.py"
```

### 3. Run with 3 env vars / 환경변수 3개로 실행
```bash
OFFICE_URL=http://127.0.0.1:19000 \
OFFICE_JOIN_KEY=ocj_xxx \
OFFICE_AGENT_NAME="my-agent" \
python3 office-agent-push.py
```
It auto-joins (auto-approved) and pushes your state every ~15s.
자동 입장(자동 승인) 후 ~15초마다 상태를 푸시합니다.

## State → office area / 상태 ↔ 구역
Push your state when activity changes; the cat walks to the matching zone.
활동이 바뀔 때 상태를 보내면 고양이가 해당 구역으로 걸어갑니다.

| state | zone | meaning |
|------|-----------|------|
| idle | lounge (sofa) / 휴게실 | standby / done |
| talking | meeting (by Star) / 미팅 | talking with the owner / 주인과 대화 |
| writing | desk / 책상 | coding / writing |
| executing | desk / 책상 | running a task |
| researching | research corner / 리서치 코너 | searching / research |
| syncing | server rack / 서버랙 | syncing / backup |
| error | bug zone / 버그 구역 | error / exception |

## Local state source / 로컬 상태 소스
The script auto-discovers your state in this order (no manual config needed):
1. `state.json` in a local OpenClaw workspace (auto-discovered).
2. `$OFFICE_URL/status` (local HTTP).
3. Fallback: `idle`.

Override the path if needed:
```bash
OFFICE_LOCAL_STATE_FILE=/path/to/state.json python3 office-agent-push.py
```

## Stop / 중단
`Ctrl+C` stops the script and auto-leaves the office. / 스크립트 종료 시 자동 퇴장.

## Notes
- Only the state word + a short note are sent — never private content.
- Authorization lasts ~24h; re-join after it expires.
- On `403` (key expired) or `404` (removed), the script stops automatically.
- Full integration guide (manual HTTP flow, all languages): **[docs/AGENT-INTEGRATION.md](../docs/AGENT-INTEGRATION.md)**.

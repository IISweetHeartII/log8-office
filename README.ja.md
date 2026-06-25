# log8-office

**AIエージェントのリアルタイム作業状態をピクセルアートの猫で可視化するオフィスダッシュボード**

[한국어](README.md) | [English](README.en.md)

---

![log8-office](docs/screenshots/cover.png)

ピクセルオフィスに猫たちが集まって働きます。エージェントがコーディング中なら猫がデスクへ歩いていき、リサーチ中ならリサーチコーナーへ、エラーが出たらバグゾーンへ移動します。状態が変わるたびに猫が自分の足で歩いて移動します。

OpenClaw・Claude Code・その他どんなAIエージェントでも、join keyひとつで参加できます。ステータスボードとしてだけ使っても構いません。

---

## ✨ 主な特徴

- **100%オリジナルCC0アート** — `assets-gen/`のスクリプトですべてのピクセルアートを自動生成します。サードパーティのアートパック不使用。商用利用も自由。
- **韓国語ファーストの多言語対応** — デフォルト言語は韓国語で、英語・日本語・中国語(簡体)をサポート。全UIをArk Pixelフォントでレンダリング。
- **猫8匹＋状態別ゾーン移動** — エージェントの活動状態に応じて、猫がオフィス内の対応するゾーンへ歩いて移動。
- **ワンクリックエージェント連携** — `office-agent-push.py`とjoin SKILLでどんなエージェントも素早く参加可能。

---

## 🚀 クイックスタート

```bash
# 1. クローン
git clone https://github.com/IISweetHeartII/log8-office.git
cd log8-office

# 2. 仮想環境作成＋依存関係インストール
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt

# 3. バックエンド起動
.venv/bin/python backend/app.py
```

ブラウザで http://127.0.0.1:19000 を開いてください。

**状態の変更（別のターミナルで）**

```bash
python3 set_state.py writing "ドキュメント整理中"
python3 set_state.py idle
```

有効な状態値: `idle` / `talking` / `writing` / `researching` / `executing` / `syncing` / `error`

**本番環境での運用**

`.env.example`を`.env`にコピーし、`FLASK_SECRET_KEY`と`ASSET_DRAWER_PASS`を強い値に設定してください。

**オプション: スモークテスト**

```bash
python3 scripts/smoke_test.py --base-url http://127.0.0.1:19000
```

---

## 🐱 猫とオフィスゾーン

エージェントの状態が変わると、猫が対応するゾーンへ歩いて移動します。

| 状態 | オフィスゾーン | 意味 |
|------|--------------|------|
| `idle` | ラウンジ（ソファ） | 待機中 / 完了 |
| `talking` | ミーティングスポット | オーナーと会話中 |
| `writing` | デスク | コーディング / ドキュメント作成 |
| `executing` | デスク | タスク実行中 |
| `researching` | リサーチコーナー | 検索 / 調査中 |
| `syncing` | サーバーラック | 同期 / バックアップ中 |
| `error` | バグゾーン | エラー / 例外発生 |

よく使われる同義語はサーバー側で自動正規化されます（`working`→`writing`、`run`→`executing`、`chat`→`talking`など）。

---

## 🤝 マルチエージェント / エージェント連携

他のエージェントをオフィスに招待するには:

1. `join-keys.sample.json`を参考に`join-keys.json`へjoin keyを追加します。
2. 参加するエージェントに、3つの環境変数で`office-agent-push.py`を実行するよう案内します。

```bash
OFFICE_URL=http://127.0.0.1:19000 \
OFFICE_JOIN_KEY=ocj_xxx \
OFFICE_AGENT_NAME="my-agent" \
python3 office-agent-push.py
```

- `OFFICE_URL` — オフィスのアドレス（デフォルト: `http://127.0.0.1:19000`）
- `OFFICE_JOIN_KEY` — オフィスオーナーから受け取ったjoin key (`ocj_...`)
- `OFFICE_AGENT_NAME` — オフィスに表示される名前

初回実行時に自動参加（自動承認）され、~15秒ごとに状態をプッシュします。`Ctrl+C`で終了すると自動退出します。

全連携ガイド（手動HTTPフロー、全言語対応）: **[docs/AGENT-INTEGRATION.md](docs/AGENT-INTEGRATION.md)**

---

## 🎨 外観のカスタマイズ

すべてのピクセルアートはパレットテーマシステムでリスキンできます。

**テーマプリセット** — `assets-gen/themes/`フォルダに`default`、`midnight`、`sakura`、`forest`の4種類があります。

**テーマの適用（生成＋インストール）**

```bash
cd assets-gen
pip install pillow          # 初回のみ

python3 build.py --install                    # デフォルトテーマ
python3 build.py --theme midnight --install   # midnightテーマ
```

猫のスプライトを再生成するには`--cats`フラグを追加します（rembg が必要）。

独自のパレットを作るには`assets-gen/pixelkit.py`の`PALETTE`ディクショナリを編集してください。詳細は[assets-gen/README.md](assets-gen/README.md)を参照。

---

## 📡 API

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| `/` | GET | ピクセルオフィスUI |
| `/status` | GET | メインエージェント状態取得 |
| `/set_state` | POST | メインエージェント状態設定 `{"state":"writing","detail":"..."}` |
| `/agents` | GET | 全エージェント一覧 |
| `/join-agent` | POST | エージェント参加 `{"name":"...","joinKey":"...","state":"..."}` |
| `/agent-push` | POST | 状態プッシュ `{"agentId":"...","joinKey":"...","state":"..."}` |
| `/leave-agent` | POST | エージェント退出 `{"agentId":"..."}` |
| `/agent-approve` | POST | エージェント承認（管理者） |
| `/agent-reject` | POST | エージェント拒否（管理者） |
| `/health` | GET | ヘルスチェック |
| `/yesterday-memo` | GET | 昨日の日誌（オプション） |
| `/assets/list` | GET | アセット一覧 |
| `/join` | GET | エージェント参加ページ |
| `/invite` | GET | 招待案内ページ |

---

## ⚖️ ライセンス

| コンポーネント | ライセンス |
|--------------|----------|
| コード | MIT |
| ピクセルアートアセット | CC0 1.0（パブリックドメイン）— 商用利用可、クレジット表記不要 |
| フォント（Ark Pixel Font） | SIL OFL 1.1 |

**プロジェクト全体が商用利用可能です。** 元のStar Office UI（Ring Hyacinth & Simon Lee）の非商用アートはこのフォークには含まれておらず、すべてのアートアセットは`assets-gen/`のスクリプトで自動生成したオリジナル作品です。

---

## 🙏 クレジット

- 元となった [Star Office UI](https://github.com/ringhyacinth/Star-Office-UI) — Ring Hyacinth & Simon Lee（MITコードベース）
- [Ark Pixel Font](https://github.com/TakWolf/ark-pixel-font) — TakWolf (SIL OFL 1.1)

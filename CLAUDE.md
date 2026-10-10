# ひるメモ（https://hirumemo.com/）公開用リポジトリ

「ヒルナンデス！」で紹介された商品・店・宿をまとめる非公式のアフィリエイトサイト。運営は坂尾さん。

## 仕組み
- `tools/build_site.py` がサイト全体を作る。データ（放送回 `B`、価格比較 `OFFERS` など）もこのファイルの中にある。
- リポジトリ直下で `python3 tools/build_site.py` を実行すると `site/` に全ページが出る。
- `main` の `site/` に push すると、お名前.com のサーバーが10分おきに取り込んで公開する（`site/` の .html/.xml/.txt のみ。削除はしない）。

## 放送回を1つ追加して公開する手順
1. 材料は Claude Docs「ヒルナンデス 紹介商品ログ」（https://claude.ai/code/artifact/e3bb6cf2-6d78-4925-806a-4b883da4854e）の当日の記事下書きと商品データベース。確かめられた事実だけを使う。分からない値は `None`（画面では「確認中」）。
2. `tools/build_site.py` の `B` の先頭に、既存の回（例：`20261009-yokohama-shingo`）と同じ形で1件足す。
   - slug は `YYYYMMDD-地名や店名-英小文字`。
   - 楽天で買える商品は `https://hb.afl.rakuten.co.jp/ichiba/584a3b37.2a4108aa.584a3b38.a1b9d8be/?pc=<商品URLをエンコード>` 形式。楽天以外は `S(...)` ヘルパー（アフィリエイトでないリンク）。
   - 写真がないものは `DISH`。番組の画面写真や販売店の文章のコピーは使わない。
3. `python3 tools/build_site.py` → `node tools/check.js`（はみ出し0・エラー0で終了コード0）。
4. `git add -A && git commit && git push origin main`。
5. 反映確認（push から最大10分）：`https://hirumemo.com/<slug>.html` を開いて表示を確認。
6. Bing への通知（IndexNow）：`https://www.bing.com/indexnow?url=<ページURLをエンコード>&key=b092c025ea1e7d07f8441da1c4355da6`。Google はサイトマップから拾う（Search Console の手動リクエストはブラウザが使えるときだけ）。

## 守ること
- 楽天ウェブサービスのアクセスキーなど秘密の値は絶対に入れない（このリポジトリは公開）。
- 既存のファイルは消さない。`site/` の名前は英小文字・数字・ハイフンのみ。
- 番組・放送局と関係があるような書き方をしない。価格には確認日を添える。

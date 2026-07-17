# 案出し

ChatGPTやClaudeにアイデアを頼んだとき、名前や見た目だけ違う似た案ばかり並ぶことはありませんか？

**案出し**は、候補ごとの「仕組み」を変えて発想し、弱点や確かめ方まで一緒に考えるためのSkillです。CodexとClaude Codeで使えます。商品、サービス、企画、物語、キャラクター、ネーミング、イベント、業務改善などに対応します。

用途を決めずに、言葉やイメージから詩的・不条理な断片だけを広げることもできます。

## まず試してみる

Codexでは `$andashi`、Claude Codeでは `/andashi` を使います。

~~~text
$andashi 読書を続けやすくするサービス案を3つ。通知、連続記録、バッジは禁止。
~~~

~~~text
/andashi 読書を続けやすくするサービス案を3つ。通知、連続記録、バッジは禁止。
~~~

案ごとの違い、弱点、次に小さく試す方法まで返します。

既存案を直したいとき:

~~~text
/andashi この案の良い核は残して、ありきたりな部分を別の仕組みに変えて。
~~~

候補を比較したいとき:

~~~text
/andashi このA案とB案だけを同じ条件で比較して。どちらも駄目ならそう言って。
~~~

意味を決めずに遊びたいとき:

~~~text
/andashi 夜の冷凍倉庫と春休みから、用途も意味も決めない断片を6つ。説明や物語化はしないで。
~~~

Codexでは上記の `/andashi` を `$andashi` に置き換えてください。

## 普通の案出しとの違い

- 名前、色、媒体だけ変えた案を別案として数えません。
- 「AI化」「SNS化」「ポイント化」を、それだけで新しさとは扱いません。
- 効果、需要、商標、法的安全性など、未確認のことを確認済みのように断定しません。
- 必要なら、完成させる前に複数の方向を見せて、どれを深めるか人間に選んでもらいます。
- 自分で作った案に点数を付けて「検証済み」とは言いません。壊れやすい場面と、小さな試し方を示します。

## Codexへインストール

### GitHubから

~~~bash
codex plugin marketplace add akakeishin/andashi
codex plugin add andashi@andashi
~~~

### ZIPから

ZIPを解凍し、そのフォルダで実行します。

~~~bash
cd /path/to/andashi-1.1.0
codex plugin marketplace add .
codex plugin add andashi@andashi
~~~

CodexまたはChatGPTデスクトップアプリを再起動し、新しい会話で `$andashi` を付けて試してください。

## Claude Codeへインストール

### GitHubから

~~~bash
git clone https://github.com/akakeishin/andashi.git
mkdir -p ~/.claude/skills/andashi
cp -R andashi/.claude/skills/andashi/. ~/.claude/skills/andashi/
~~~

### ZIPから

ZIPを解凍したフォルダで実行します。

~~~bash
mkdir -p ~/.claude/skills/andashi
cp -R .claude/skills/andashi/. ~/.claude/skills/andashi/
~~~

新しいClaude Codeセッションを開き、`/andashi` で呼び出します。依頼内容がSkillのdescriptionに一致すると、Claudeが自動で使うこともあります。

このリポジトリ内でClaude Codeを起動した場合は、`.claude/skills/andashi` がプロジェクトSkillとして自動検出されるため、コピーせず試せます。

詳しい導入・更新・削除手順は [INSTALL.md](INSTALL.md) を参照してください。

## 依頼のコツ

テーマだけでも動きますが、次のうち分かるものを加えると案が具体的になります。

- 誰の、どんな場面を変えたいか
- 絶対に守る条件
- 避けたい定番や既存案
- 予算、時間、人数、媒体
- 欲しい案の数と詳しさ

全部を埋める必要はありません。安全に仮定できる部分は、案出し側で仮定を明示して進めます。

## 二つの使い方

### 採用する案を考える

商品、企画、物語、名前など、実際に使う候補が欲しい場合の通常の使い方です。異なる仕組みの候補を作り、制約違反、重複、弱点、次の検証を確認します。

### 意味を決めずに素材を広げる

「用途を決めない」「説明しない」「断片だけ」と明示すると、入力した言葉・音・像の痕跡を残しながら、詩的または不条理な断片を返します。勝手に商品案や物語へまとめません。

## 困ったとき

- Codexで見えない: CodexまたはChatGPTデスクトップアプリを再起動し、新しい会話を開く
- Claude Codeで見えない: 新しいClaude Codeセッションを開き、`/andashi` を入力する
- Codexへの導入確認: `codex plugin list` を実行する
- 削除したい: [INSTALL.md](INSTALL.md) の削除手順を参照する

## 開発者向け

~~~bash
python3 scripts/validate.py
~~~

Codex Plugin本体は [`plugins/andashi`](plugins/andashi)、Claude Code版は [`.claude/skills/andashi`](.claude/skills/andashi) にあります。検証時に両者のSkill本文と参照資料が完全一致することも確認します。Plugin Directory申請用のテストは [`submission/test-cases.json`](submission/test-cases.json) にあります。

## ライセンス

[MIT License](LICENSE)

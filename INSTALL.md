# インストール・更新・削除

## Codexへインストール

ZIPを解凍し、そのフォルダへ移動して実行します。

~~~bash
cd /path/to/andashi-1.1.0
codex plugin marketplace add .
codex plugin add andashi@andashi
~~~

CodexまたはChatGPTデスクトップアプリを再起動し、新しい会話で試します。

~~~text
$andashi 夜の冷凍倉庫と春休みから、用途も意味も決めない断片を6つ。
~~~

### Codex版を更新

新しいZIPへ差し替えた後に実行します。

~~~bash
codex plugin marketplace upgrade andashi
~~~

### Codex版を削除

~~~bash
codex plugin remove andashi
codex plugin marketplace remove andashi
~~~

## Claude Codeへインストール

ZIPを解凍し、そのフォルダへ移動して実行します。

~~~bash
cd /path/to/andashi-1.1.0
mkdir -p ~/.claude/skills/andashi
cp -R .claude/skills/andashi/. ~/.claude/skills/andashi/
~~~

新しいClaude Codeセッションで試します。

~~~text
/andashi 夜の冷凍倉庫と春休みから、用途も意味も決めない断片を6つ。
~~~

Claudeは依頼内容がSkillのdescriptionに一致した場合、`/andashi` を明示しなくてもSkillを使うことがあります。

### Claude Code版を更新

新しいZIPのフォルダでコピーを再実行します。

~~~bash
cp -R .claude/skills/andashi/. ~/.claude/skills/andashi/
~~~

### Claude Code版を削除

~~~bash
rm -rf ~/.claude/skills/andashi
~~~

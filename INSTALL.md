# ZIPからインストールする

## 必要なもの

- Codex CLI
- ChatGPTデスクトップアプリ（アプリで使う場合）
- ZIPを解凍できる環境

## 手順

ZIPを解凍し、ターミナルで解凍したフォルダへ移動して次を実行します。

```bash
cd /path/to/andashi-1.0.0
codex plugin marketplace add .
codex plugin add andashi@andashi
```

ChatGPTデスクトップアプリを使う場合は、再起動後に **Plugins** を開き、Marketplace「案出し」からインストールすることもできます。

新しい会話で `$andashi` を付けて試します。

```text
$andashi 夜の冷凍倉庫と春休みから、用途も意味も決めない断片を6つ。
```

## 更新

新しいZIPへ差し替えた後、次を実行します。

```bash
codex plugin marketplace upgrade andashi
```

## 削除

```bash
codex plugin remove andashi
codex plugin marketplace remove andashi
```

<<<<<<< HEAD
# dl_youtube
=======
# YouTube 4K Downloader (yt-dlp + YAML)

YouTube の動画を **4K優先（なければ最大解像度）で mp4 としてダウンロード** する Python スクリプトです。  
単体URLでも、`urls.yaml` にまとめた複数URLでも一括ダウンロードできます。

---

## 📌 機能

- 🔥 4Kを優先（対象動画に4Kがなければ最大解像度で取得）
- 🎯 YAMLで複数URLを一括ダウンロード
- ✨ MP4へ自動変換（音声・映像結合）
- 🚀 CLI操作で単体URLもすぐダウンロード
- 🐳 Docker環境でも実行可能（環境を汚さない）

---

## 1️⃣ venv（仮想環境）で使う方法（おすすめ）

普段使う分には **venv が最も簡単で柔軟** です。

### 1-1. 事前準備

- Python 3.10 以上
- `ffmpeg` が PATH にあること

### 1-2. セットアップ

```bash
# プロジェクトフォルダへ移動
cd /path/to/project

# 仮想環境の作成
python3 -m venv .venv

# 有効化（macOS / Linux）
source .venv/bin/activate
# Windows: .venv\Scripts\activate

# 必要パッケージのインストール
pip install -r requirements.txt
````

### 1-3. URL リストファイル（任意）

`urls.yaml` 例：

```yaml
urls:
  - "https://www.youtube.com/watch?v=AAAAAAA"
  - "https://www.youtube.com/watch?v=BBBBBBB"
```

### 1-4. 使い方

#### 単体URLをダウンロード

```bash
python dl_4k.py "https://www.youtube.com/watch?v=XXXXXXX"
```

#### YAMLから複数URLをダウンロード

```bash
python dl_4k.py --url_yaml urls.yaml
```

📁 出力先は `downloads/` です

---

## 2️⃣ Dockerで使う方法

環境を汚したくない場合やサーバー利用には Docker が便利です。

### 2-1. Docker image をビルド

```bash
./build.sh
```

または：

```bash
docker build -t yt-4k-dl .
```

### 2-2. ダウンロード実行（例）

`urls.yaml` をプロジェクト直下に置いた状態で：

```bash
docker run --rm -it \
  -v "$(pwd)/downloads:/app/downloads" \
  -v "$(pwd)/urls.yaml:/app/urls.yaml" \
  yt-4k-dl \
  python dl_4k.py --url_yaml urls.yaml
```

📌 ダウンロード結果はホスト側の `downloads/` に保存されます

---

## 3️⃣ 設定ファイル（config.yaml）

品質調整は `config.yaml`で行います：

```yaml
output_dir: "./downloads"
min_height: 2160        # 4K を狙う設定
format: "best"          # 必要に応じて変更
merge_output_format: "mp4"
```

> 注意：
> `format` 条件を厳しくしすぎると、4K非対応動画でエラーが出ます

---

## 4️⃣ urls.yaml フォーマット

```yaml
urls:
  - "https://www.youtube.com/watch?v=XXXXXXX"
  - "https://www.youtube.com/watch?v=YYYYYYY"
```

---

## 5️⃣ トラブルシューティング

| エラー                               | 考えられる原因           | 解決策                       |
| --------------------------------- | ----------------- | ------------------------- |
| Requested format is not available | 指定フォーマットが動画に存在しない | `format: "best"` に変更      |
| Permission denied（Docker）         | root権限のファイル操作     | 基本無視でOK。更新はDockerfile側で固定 |
| ダウンロードが遅い                         | YouTube側制限        | VPN切る / 有線接続 / 再実行        |

---

## 📂 フォルダ構成例

```
project/
├─ dl_4k.py
├─ config.yaml
├─ urls.yaml
├─ downloads/
├─ requirements.txt
├─ Dockerfile
├─ run.sh
└─ build.sh
```

---

## 📝 ライセンス

MIT（予定）

---

## 👤 Author

Shu
GitHub: [https://github.com/](https://github.com/)<あなたのID>

```
>>>>>>> 1c1406e (Initial commit)

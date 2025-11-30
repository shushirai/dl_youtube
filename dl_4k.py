#!/usr/bin/env python3
import os
import argparse
import yt_dlp
import yaml

DEFAULT_CONFIG = {
    "output_dir": "./downloads",
    "min_height": 2160,           # ここを 4K の目安として使う
    "merge_output_format": "mp4", # 最終的なコンテナ
}

def progress_hook(d):
    if d["status"] == "finished":
        print(f"\n✅ ダウンロード完了: {d['filename']}")
    elif d["status"] == "downloading":
        print(
            f"\r⬇️ ダウンロード中: {d.get('_percent_str', '??')} "
            f"{d.get('_eta_str', '--:--')}",
            end="",
        )

def load_config(path: str) -> dict:
    conf = DEFAULT_CONFIG.copy()
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            user = yaml.safe_load(f) or {}
        conf.update(user)
        print(f"🧩 設定ファイルを読み込みました: {path}")
    else:
        print(f"⚠️ 設定ファイルが見つからないためデフォルト設定を使用します: {path}")
    return conf

def load_urls_from_file(path: str) -> list[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"URLファイルが見つかりません: {path}")
    urls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    return urls

def load_urls_from_yaml(path: str) -> list[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"YAMLファイルが見つかりません: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if isinstance(data, list):
        return [str(u).strip() for u in data if u]
    if isinstance(data, dict):
        urls = data.get("urls", [])
        return [str(u).strip() for u in urls if u]
    raise ValueError("urls.yaml はリスト または {urls: [...]} 形式にしてください。")

def print_video_info(info, best, idx, total):
    title = info.get("title", "Unknown Title")
    print(f"\n🎥 [{idx}/{total}] {title}")
    if best and best.get("height"):
        h = best["height"]
        w = best.get("width")
        print(f"📏 ダウンロード予定解像度: {h}p ({w}x{h})")
    else:
        print("📏 解像度情報が見つかりませんでした（best フォーマットを使用）。")

def choose_best_format(formats: list, min_height: int):
    """
    4K優先＋フォールバックロジック：
      1) mp4 かつ min_height 以上
      2) コンテナ不問で min_height 以上
      3) 利用可能な中で最大解像度
    """
    # 映像があるフォーマットのみ対象
    videos = [
        f for f in formats
        if f.get("vcodec") and f["vcodec"] != "none"
    ]
    if not videos:
        return None, "best"

    # 1) mp4 かつ 指定解像度以上
    mp4_candidates = [
        f for f in videos
        if f.get("ext") == "mp4"
        and f.get("height")
        and f["height"] >= min_height
    ]
    if mp4_candidates:
        best = max(mp4_candidates, key=lambda f: f["height"])
        # format_id ベースでもいいが、わかりやすく height 条件にしておく
        fmt = f"bestvideo[ext=mp4][height>={min_height}]+bestaudio/best/best"
        return best, fmt

    # 2) コンテナ不問で min_height 以上
    hi_candidates = [
        f for f in videos
        if f.get("height") and f["height"] >= min_height
    ]
    if hi_candidates:
        best = max(hi_candidates, key=lambda f: f["height"])
        fmt = f"{best['format_id']}+bestaudio/best"
        return best, fmt

    # 3) 仕方ないので最大解像度
    best = max(videos, key=lambda f: f.get("height") or 0)
    fmt = f"{best['format_id']}+bestaudio/best"
    return best, fmt

def download_videos(urls: list[str], config: dict):
    if not urls:
        print("❗ URL が1件も指定されていません。")
        return

    output_dir = config["output_dir"]
    min_height = int(config["min_height"])
    os.makedirs(output_dir, exist_ok=True)

    print(f"📂 保存先: {output_dir}")
    print(f"🎯 4Kターゲット: {min_height}p 以上を優先")
    print(f"📥 ダウンロード対象URL数: {len(urls)}")

    info_opts = {"quiet": True}
    merge_format = config.get("merge_output_format", "mp4")

    try:
        with yt_dlp.YoutubeDL(info_opts) as info_ydl, yt_dlp.YoutubeDL({}) as _:
            pass
    except Exception:
        pass  # 初期化だけ（省略可）

    try:
        with yt_dlp.YoutubeDL(info_opts) as info_ydl:
            for idx, url in enumerate(urls, start=1):
                try:
                    info = info_ydl.extract_info(url, download=False)
                except Exception as e:
                    print(f"\n❌ [{idx}/{len(urls)}] 情報取得エラー: {url} ({e})")
                    continue

                formats = info.get("formats", [])
                best_format, format_str = choose_best_format(formats, min_height)

                # 4K 未満だったら一言コメント
                if best_format and best_format.get("height") and best_format["height"] < min_height:
                    print(
                        f"\nℹ️ この動画の最大解像度は {best_format['height']}p です。"
                        f" 4K(>= {min_height}p) は存在しないため、最大解像度でダウンロードします。"
                    )

                print_video_info(info, best_format, idx, len(urls))

                ydl_opts = {
                    "format": format_str,
                    "merge_output_format": merge_format,
                    "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
                    "postprocessors": [
                        {
                            "key": "FFmpegVideoConvertor",
                            "preferedformat": merge_format,
                        }
                    ],
                    "noplaylist": True,
                    "quiet": False,
                    "progress_hooks": [progress_hook],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

        print("\n🎉 すべてのダウンロード処理が完了しました。")

    except KeyboardInterrupt:
        print("\n⏹ キャンセルされました")
    except Exception as e:
        print(f"\n❌ ダウンロード中にエラーが発生しました: {e}")

def parse_args():
    psr = argparse.ArgumentParser(
        description="YouTube 高解像度 mp4 ダウンローダ（4K優先＋フォールバック）"
    )
    psr.add_argument("url", nargs="?", help="単体URL（指定されていれば最優先）")
    psr.add_argument("--url_file", help="複数URLを1行ずつ書いたテキストファイル")
    psr.add_argument("--url_yaml", help="複数URLを含むYAMLファイル")
    psr.add_argument("--config", default="./config.yaml", help="設定YAMLファイルパス")
    return psr.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)

    if args.url:
        urls = [args.url]
    elif args.url_file:
        urls = load_urls_from_file(args.url_file)
    elif args.url_yaml:
        urls = load_urls_from_yaml(args.url_yaml)
    else:
        print("❗ URL が指定されていません。")
        print("   例）python dl_4k.py <URL>")
        print("       python dl_4k.py --url_file urls.txt")
        print("       python dl_4k.py --url_yaml urls.yaml")
        return

    download_videos(urls, config)

if __name__ == "__main__":
    main()

# ✅ ベースイメージ：軽量かつ信頼性の高い python:3.10-slim
FROM python:3.10-slim

# ✅ 環境変数（ロケール対策や非対話型対応）
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Tokyo \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ✅ 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    sudo \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ✅ ユーザーを作成（権限管理強化）
RUN useradd -m -u 1000 -s /bin/bash shu_docker && \
    echo 'shu_docker ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# ✅ 作業ディレクトリ設定
WORKDIR /app
COPY . /app

# ✅ 任意：Pythonライブラリをインストール（必要なら）
 RUN pip install --no-cache-dir -r requirements.txt

# ✅ 非 root ユーザーで実行
USER shu_docker

# ✅ bash をデフォルトエントリポイントに（対話・デバッグ用）
CMD ["/bin/bash"]

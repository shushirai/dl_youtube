#!/bin/bash
docker run -it --rm \
  -v "$(pwd)":/app \
  --workdir /app \
  yt-dlp-env

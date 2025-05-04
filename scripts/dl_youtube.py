import os
import argparse
from yt_dlp import YoutubeDL

psr = argparse.ArgumentParser()
psr.add_argument('--url_file', default='urls.txt')
psr.add_argument('--output_dir', default='../downloads')
args = psr.parse_args()

os.makedirs(args.output_dir, exist_ok=True)

ydl_opts = {
    'format': 'best',
    'outtmpl': os.path.join(args.output_dir, '%(title)s.%(ext)s')
}

with open(args.url_file, 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

with YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)

print("-- All Done --")

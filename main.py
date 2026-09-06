import os
import subprocess
import gdown

# Google Drive File ID aur YouTube Stream Key
FILE_ID = "1LvBiHPZnWLdqJ47SGncTi3AS6XKoaaE1"
STREAM_KEY = os.environ.get("YOUTUBE_STREAM_KEY")

VIDEO_FILE = "video.mp4"

# Step 1: Video download karna
if not os.path.exists(VIDEO_FILE):
    print("Google Drive se video download ho rahi hai...")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, VIDEO_FILE, quiet=False)

# Step 2: FFmpeg se YouTube par continuous stream karna (Low CPU / Stable Settings)
print("YouTube par stream shuru ho rahi hai...")
ffmpeg_cmd = [
    'ffmpeg',
    '-re',
    '-stream_loop', '-1',
    '-i', VIDEO_FILE,
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-b:v', '1000k',
    '-maxrate', '1200k',
    '-bufsize', '2400k',
    '-pix_fmt', 'yuv420p',
    '-g', '60',
    '-c:a', 'aac',
    '-b:a', '96k',
    '-ar', '44100',
    '-f', 'flv',
    f'rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
]

subprocess.run(ffmpeg_cmd)

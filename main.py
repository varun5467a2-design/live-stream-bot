import os
import subprocess
import gdown

# Google Drive File ID (Apni file ID yahan daalein)
FILE_ID = "1LvBiHPZnWLdqJ47SGncTi3AS6XKoaaE1"
VIDEO_FILE = "stream.mp4"

# Drive se video download karne ke liye
if not os.path.exists(VIDEO_FILE):
    print("Google Drive se video download ho rahi hai...")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, VIDEO_FILE, quiet=False)

# YouTube Stream Key from Render Environment Variables
STREAM_KEY = os.environ.get("YOUTUBE_STREAM_KEY")
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

ffmpeg_cmd = [
    "ffmpeg",
    "-re",
    "-stream_loop", "-1",
    "-i", VIDEO_FILE,
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-b:v", "3000k",
    "-maxrate", "3000k",
    "-bufsize", "6000k",
    "-pix_fmt", "yuv420p",
    "-g", "50",
    "-c:a", "aac",
    "-b:a", "128k",
    "-ar", "44100",
    "-f", "flv",
    RTMP_URL
]

print("Live stream start ho rahi hai...")
subprocess.run(ffmpeg_cmd)

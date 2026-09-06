import os
import subprocess

# Render environment variables se Stream Key uthayega
STREAM_KEY = os.environ.get("YOUTUBE_STREAM_KEY")
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

ffmpeg_cmd = [
    "ffmpeg",
    "-re",
    "-stream_loop", "-1",
    "-i", "stream.mp4",
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

print("Stream shuru ho rahi hai...")
subprocess.run(ffmpeg_cmd)

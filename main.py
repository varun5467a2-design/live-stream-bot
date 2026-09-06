import os
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import gdown

# Render web service health check bypass
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live stream is running...")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Start HTTP server in background thread
threading.Thread(target=run_web_server, daemon=True).start()

# Variables
FILE_ID = "1LvBiHPZnWLdqJ47SGncTi3AS6XKoaaE1"
STREAM_KEY = os.environ.get("YOUTUBE_STREAM_KEY")
VIDEO_FILE = "video.mp4"

# Download video
if not os.path.exists(VIDEO_FILE):
    print("Downloading video from Google Drive...")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, VIDEO_FILE, quiet=False)

# FFmpeg streaming loop
print("Starting stream to YouTube...")
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

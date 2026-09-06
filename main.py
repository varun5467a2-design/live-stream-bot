import os
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import gdown

# Render web service health check bypass server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live stream is running successfully...")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Start background HTTP server
threading.Thread(target=run_web_server, daemon=True).start()

FILE_ID = "1mwrgSvuaDILeNdeiDa8HyF_QCQhPgWj-"
STREAM_KEY = os.environ.get("YOUTUBE_STREAM_KEY", "zv8s-bzza-rwca-6sc2-by5e")
VIDEO_FILE = "video.mp4"

# Download video file directly on Render cloud server
if not os.path.exists(VIDEO_FILE):
    print("Downloading video from Google Drive...")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, VIDEO_FILE, quiet=False)

# ZERO-CPU Direct Copy Stream to YouTube (Fixes speed=0.41x lag)
print("Starting ZERO-LOAD direct stream to YouTube...")
ffmpeg_cmd = [
    'ffmpeg',
    '-re',
    '-stream_loop', '-1',
    '-i', VIDEO_FILE,
    '-c:v', 'copy',
    '-c:a', 'copy',
    '-f', 'flv',
    f'rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
]

subprocess.run(ffmpeg_cmd)

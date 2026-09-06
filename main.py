import os
import time
import subprocess
import threading
from flask import Flask

app = Flask(__name__)

# Web server route for keep-alive ping / health check
@app.route('/')
def home():
    return "Stream Bot is active and running 24/7!"

def run_stream():
    """
    Background worker loop that keeps FFmpeg streaming continuously.
    If FFmpeg crashes or disconnects, it automatically restarts after 5 seconds.
    """
    # Environment variables se RTMP URL aur Stream Key le rahe hain (Fallback values appended if needed)
    rtmp_url = os.environ.get("RTMP_URL", "rtmp://a.rtmp.youtube.com/live2")
    stream_key = os.environ.get("STREAM_KEY", "YOUR_STREAM_KEY_HERE")
    
    stream_target = f"{rtmp_url}/{stream_key}"
    video_input = os.environ.get("VIDEO_PATH", "input.mp4")

    # Complete FFmpeg Command for Infinite Looping Stream
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",                          # Read input at native frame rate
        "-stream_loop", "-1",            # Loop input video endlessly
        "-i", video_input,               # Video source
        "-c:v", "libx264",               # H.264 Video Codec
        "-preset", "veryfast",           # Low CPU usage preset
        "-maxrate", "3000k",             # Max video bitrate
        "-bufsize", "6000k",             # Buffer size
        "-pix_fmt", "yuv420p",           # Standard pixel format
        "-g", "50",                      # Keyframe interval
        "-c:a", "aac",                   # Audio Codec
        "-b:a", "128k",                  # Audio bitrate
        "-ar", "44100",                  # Audio sample rate
        "-f", "flv",                     # FLV format for RTMP streaming
        stream_target
    ]

    print("Starting continuous live stream loop...")
    
    while True:
        try:
            print("Launching FFmpeg process...")
            # Execute FFmpeg process
            process = subprocess.run(ffmpeg_cmd)
            print(f"FFmpeg exited with code: {process.returncode}")
        except Exception as e:
            print(f"Stream encountered an error: {e}")
        
        # Connection loss / process crash retry handling
        print("Stream disconnected or stopped. Retrying connection in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    # Start the streaming thread in background
    stream_thread = threading.Thread(target=run_stream, daemon=True)
    stream_thread.start()

    # Get PORT assigned dynamically by Render (defaults to 8080 if local)
    port = int(os.environ.get("PORT", 8080))
    
    # Run Flask Web Server
    app.run(host="0.0.0.0", port=port)

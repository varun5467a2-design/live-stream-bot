const express = require('express');
const { spawn, execSync } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 10000;

const STREAM_KEY = process.env.STREAM_KEY;
const RTMP_URL = `rtmp://a.rtmp.youtube.com/live2/${STREAM_KEY}`;
const VIDEO_FILE = 'video.mp4';
const DRIVE_FILE_ID = '1Mc-RYkzladb1pjnIFVp-cU6m0dDvb4tl';

function downloadVideo() {
  if (fs.existsSync(VIDEO_FILE)) {
    fs.unlinkSync(VIDEO_FILE);
  }
  console.log('Downloading video from Google Drive using gdown...');
  execSync(`gdown "https://drive.google.com/uc?id=${DRIVE_FILE_ID}" -O ${VIDEO_FILE}`, { stdio: 'inherit' });
  console.log('Download complete.');
}

function startStream() {
  const ffmpeg = spawn('ffmpeg', [
    '-re',
    '-stream_loop', '-1',
    '-i', VIDEO_FILE,
    '-c:v', 'libx264',
    '-preset', 'veryfast',
    '-maxrate', '700k',
    '-bufsize', '1400k',
    '-pix_fmt', 'yuv420p',
    '-g', '48',
    '-keyint_min', '48',
    '-c:a', 'aac',
    '-b:a', '128k',
    '-ar', '44100',
    '-f', 'flv',
    RTMP_URL
  ]);

  ffmpeg.stdout.on('data', (data) => console.log(`ffmpeg: ${data}`));
  ffmpeg.stderr.on('data', (data) => console.log(`ffmpeg: ${data}`));

  ffmpeg.on('close', (code) => {
    console.log(`ffmpeg process exited with code ${code}, restarting...`);
    setTimeout(startStream, 5000);
  });
}

downloadVideo();
startStream();

app.get('/ping', (req, res) => {
  res.send('OK - Stream running');
});

app.listen(PORT, () => {
  console.log(`Health check server running on port ${PORT}`);
});

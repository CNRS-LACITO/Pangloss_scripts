mkdir degrades

for %%a in ("*.wav") do ffmpeg -i "%%a" -ab 128k -ar 44100 "degrades\%%~na.mp3"

for %%a in ("*.mp4") do ffmpeg -i "%%a" -b:v 1500k -b:a 128k -vcodec libx264 -acodec aac -s 320x180  "degrades\%%~na.mp4"

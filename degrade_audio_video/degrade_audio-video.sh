mkdir degrades

for filename in *.wav 
do
  output_filename=${filename/.wav/}
  ffmpeg -i $filename -ab 128k -ar 44100 degrades/${output_filename}.mp3
done

for filename in *.mp4
do
  output_filename=${filename/.mp4/}
  ffmpeg -i $filename  -b:v 1500k -b:a 128k -vcodec libx264 -acodec aac -s 320x180  degrades/${output_filename}.mp4
done


mkdir degrades

for filename in *.wav 
do
  output_filename=${filename/.wav/}
  ffmpeg -i $filename -ab 128k -ar 44100 degrades/${output_filename}.mp3
done

for filename in *.mp4
do
  output_filename=${filename/.mp4/}
  # 16/9
  ffmpeg -i $filename  -b:v 1500k -b:a 128k -vcodec libx264 -acodec aac -s 320x180  degrades/${output_filename}.mp4
  # 4/3
  # ffmpeg -i $filename  -b:v 1500k -b:a 128k -vcodec libx264 -acodec aac -s 320x240 degrades/${output_filename}.mp4
  # autre
  # ffmpeg -i fichier.mp4 -b:v 1500k -b:a 128k -vcodec libx264 -acodec aac -vf scale=320:-2 degrades/${output_filename}.mp4
done

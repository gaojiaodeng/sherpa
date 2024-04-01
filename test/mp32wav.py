import sys
import subprocess

def main(argv):
  mp3_file = argv[0]
  wav_file = argv[1]

  command = [
    "ffmpeg",
    "-i", mp3_file,
    "-acodec", "pcm_s16le",
    "-ar", "16000",
    "-ac", "1",
    "-f", "wav",
    wav_file
  ]

  subprocess.run(command, check=True)


  print("Done!")

if __name__ == "__main__":
    main(sys.argv[1:])


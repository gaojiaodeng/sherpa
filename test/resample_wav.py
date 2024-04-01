import sys
import librosa
import soundfile as sf


def main(argv):
    filename = argv[0]
    output_filename = argv[1]
    original_sample_rate = int(argv[2])
    target_sample_rate = int(argv[3])

    y, sr = librosa.load(filename, sr=original_sample_rate)
    y_resampled = librosa.resample(y, orig_sr=original_sample_rate, target_sr=target_sample_rate)

    sf.write(output_filename, y_resampled, target_sample_rate)

    print(f"Resampled audio saved to {output_filename} at {target_sample_rate} Hz.")


if __name__ == "__main__":
    main(sys.argv[1:])


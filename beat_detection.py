import argparse
import librosa
import os
import subprocess

def convert_to_wav(input_file):
    output_file = "temp.wav"
    subprocess.call(["ffmpeg", "-i", input_file, output_file])
    return output_file

def save_beat_frames(input_file, fps, output_file, mul):
    convert_temp_wav = False

    # Convert input file to WAV if it is not already in WAV format
    if not input_file.lower().endswith('.wav'):
        input_file = convert_to_wav(input_file)
        convert_temp_wav = True

    # Load the audio file
    y, sr = librosa.load(input_file)

    # Use the onset detection function
    onset_env = librosa.onset.onset_strength(y, sr=sr)

    # Detect the beats
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Convert beat frames to frame numbers
    frame_numbers = librosa.frames_to_samples(beat_frames)

    # Calculate the frame numbers corresponding to the beats
    beat_frames_animation = (frame_numbers * fps / sr).astype(int)

    # Generate the frame-by-frame output with multiplier
    output = []
    for i in range(len(y)):
        if i in beat_frames_animation:
            output.append(f"{i}:{1 * mul}")
        else:
            output.append(f"{i}:0")

    # Add .txt extension to the output file if it is not present
    if not output_file.lower().endswith('.txt'):
        output_file = output_file + ".txt"

    # Save the frame-by-frame output to a text file
    with open(output_file, 'w') as f:
        f.write('\n'.join(output))

    print("Frame-by-frame output saved to:", output_file)

    # Delete temporary WAV file if it was converted
    if convert_temp_wav:
        os.remove(input_file)
        print("Temporary WAV file deleted.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Beat detection script')
    parser.add_argument('--input', type=str, help='Path to the input audio file')
    parser.add_argument('--fps', type=int, default=12, help='Frames per second (FPS) of the animation')
    parser.add_argument('--output', type=str, default="data.txt", help='Path to save the frame-by-frame output')
    parser.add_argument('--mul', type=float, default=1.0, help='Value of the kick in the output file')
    args = parser.parse_args()

    save_beat_frames(args.input, args.fps, args.output, args.mul)

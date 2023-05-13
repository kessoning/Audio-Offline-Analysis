import argparse
import librosa
import numpy as np

def save_beat_frames(input_file, fps, output_file):
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

    # Save the beat frames to a text file
    np.savetxt(output_file, beat_frames_animation, fmt='%d')

    print("Beat frames for animation:", beat_frames_animation)
    print("Beat frames saved to:", output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Beat detection script')
    parser.add_argument('--input', type=str, help='Path to the input audio file')
    parser.add_argument('--fps', type=int, help='Frames per second (FPS) of the animation')
    parser.add_argument('--output', type=str, help='Path to save the beat frames')
    args = parser.parse_args()

    save_beat_frames(args.input, args.fps, args.output)

import argparse
import os
import numpy as np
from scipy.io import wavfile
import moviepy.editor
from tqdm import trange
import subprocess

def convert_to_wav(input_file):
    output_file = "temp.wav"
    subprocess.call(["ffmpeg", "-i", input_file, output_file])
    return output_file

def parse_args():
    # Create an argument parser
    parser = argparse.ArgumentParser()
    
    # Define command-line arguments
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="path to audio file to analyze")
    parser.add_argument("-fps", type=int, default=12,
                        help="fps of the desired output")
    parser.add_argument("-o", "--output", type=str, default="data.txt",
                        help="path to save the output")
    parser.add_argument("-f", "--formula", type=str, default="x",
                        help="output formula, default is just x. Use x as the normalized sound volume."
                             "For example, use -formula \"1 + x * 2\"")
    args = parser.parse_args()
    return args


def evaluate_formula(x, formula):
    try:
        # Safely evaluate the formula expression
        result = eval(formula, {}, {'x': x})
        return result
    except Exception as e:
        raise ValueError("Invalid formula: " + str(e))


def main(args):
    convert_temp_wav = False

    input_file = args.input

    # Convert input file to WAV if it is not already in WAV format
    if not input_file.lower().endswith('.wav'):
        input_file = convert_to_wav(input_file)
        convert_temp_wav = True
    
    # Check if the input audio file exists
    if not os.path.exists(input_file):
        # If not, convert the audio using moviepy
        audio_clip = moviepy.editor.AudioFileClip(input_file)
        audio_clip.write_audiofile(input_file, fps=44100, nbytes=2, codec='pcm_s16le')

    # Get the track name from the input file
    track_name = os.path.basename(input_file)[:-4]

    # Read the audio file and convert to mono
    rate, signal = wavfile.read(input_file)
    signal = np.mean(signal, axis=1)

    # Calculate the absolute values of the audio signal
    signal = np.abs(signal)

    # Calculate the duration, frames, and samples per frame
    duration = signal.shape[0] / rate
    frames = int(np.ceil(duration * args.fps))
    samples_per_frame = signal.shape[0] / frames

    # Initialize the audio array
    audio = np.zeros(frames, dtype=signal.dtype)

    # Process each frame and calculate the mean value
    for frame in range(frames):
        start = int(round(frame * samples_per_frame))
        stop = int(round((frame + 1) * samples_per_frame))
        audio[frame] = np.mean(signal[start:stop], axis=0)

    # Normalize the audio data
    audio /= np.max(audio)

    # Create an empty output string
    output = ""

    # Apply the formula to each audio sample and create the output string
    for n in trange(len(audio), desc="Sampling"):
        result = evaluate_formula(audio[n], args.formula)
        output += f"{n}:({result}),"

    output_file = args.output
    # Add .txt extension to the output file if it is not present
    if not output_file.lower().endswith('.txt'):
        output_file = output_file + ".txt"

    # Write the output string to a text file
    with open(output_file, "w") as text_file:
        text_file.write(output)

    # Delete temporary WAV file if it was converted
    if convert_temp_wav:
        os.remove(input_file)
        print("Temporary WAV file deleted.")


if __name__ == "__main__":
    # Parse the command-line arguments
    args = parse_args()

    # Run the main function
    main(args)

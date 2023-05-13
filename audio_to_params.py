import argparse
import os
import numpy as np
from scipy.io import wavfile
import moviepy.editor
from tqdm import trange


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
    # Check if the input audio file exists
    if not os.path.exists(args.input):
        # If not, convert the audio using moviepy
        audio_clip = moviepy.editor.AudioFileClip(args.input)
        audio_clip.write_audiofile(args.input, fps=44100, nbytes=2, codec='pcm_s16le')

    # Get the track name from the input file
    track_name = os.path.basename(args.input)[:-4]

    # Read the audio file and convert to mono
    rate, signal = wavfile.read(args.input)
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

    # Write the output string to a text file
    with open(args.output, "w") as text_file:
        text_file.write(output)


if __name__ == "__main__":
    # Parse the command-line arguments
    args = parse_args()

    # Run the main function
    main(args)

import os
from functions import *

def main():
    video_file_path = "input\\CuckoBirdSound.mp4"  # File path of Input Video
    silence_time = 0.1 # Minimum time to detect silent zone
    min_time_gap = 0.1 # Time for break; It should be less than or equal to silence_time. This ensures that whole silence time internal not removed.
    output_folder = "output"  # Location to Save Output

    # Create output directory if it doesn't exist
    output_directory = os.path.dirname(output_folder + "\\")
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    except OSError as e:
        print(f"Error creating directory {output_directory}: {e}")
        exit(1)

    audio_file_path = os.path.join(output_folder, "audio.mp3")

    # Extract audio from video and save as MP3
    extract_audio_to_mp3(video_file_path, audio_file_path)

    # Calculate threshold dBs for silence detection
    thresold_dbs = calculate_thresold_dbs(audio_file_path)

    # Detect silent parts in audio
    find_index = detect_silence(audio_file_path, silence_time, min_time_gap, thresold_dbs)

    if find_index:
        # Merge non-speaking video clips
        merge_non_speaking_video_clips(video_file_path, find_index, os.path.join(output_folder, "non-speaking.mp4"))
        
        # Merge speaking video clips
        merge_speaking_video_clips(video_file_path, find_index, os.path.join(output_folder, "speaking.mp4"))
    else:
        print("No silent part found.")

if __name__ == "__main__":
    main()

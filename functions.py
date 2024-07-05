import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips
import librosa
import numpy as np

# Extracting audio from video file
def extract_audio_to_mp3(video_path, audio_output_path):
    command = f"ffmpeg -i {video_path} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {audio_output_path}"
    subprocess.run(command, shell=True)


#Calculating thresold db based on given thresold percent
def calculate_thresold_dbs(audio_file):
    y, sr = librosa.load(audio_file)
    max_amplitude = np.max(np.abs(y))
    thresold_amplitude = (max_amplitude * 1)/100
    thresold_dbs = 20 * np.log10(np.abs(thresold_amplitude))
    return thresold_dbs

#Detecting silence parts
def detect_silence(path, time, min_gap, thresold_dbs):
    command = "ffmpeg -i " + path + " -af silencedetect=n="+ str(thresold_dbs) +"dB:d=" + str(time) + " -f null -"
    out = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    s = stdout.decode("utf-8")
    
    k = s.split('[silencedetect @')
    if len(k) == 1:
        return None
    
    start, end = [], []
    for i in range(1, len(k)):
        x = k[i].split(']')[1]
        if i % 2 == 0:
            x = x.split('|')[0]
            x = x.split(':')[1].strip()
            end.append(float(x))
        else:
            x = x.split(':')[1]
            x = x.split('size')[0]
            x = x.replace('\r', '')
            x = x.replace('\n', '').strip()
            start.append(float(x))
    
    # Combine start and end lists into silence_intervals
    silence_intervals = list(zip(start, end))
    
    # Initialize an empty list to store the filtered timestamps
    filtered_list = []
    
    # Iterate through the silence intervals and filter based on min_gap
    for start_time, end_time in silence_intervals:
        duration = end_time - start_time
        if duration > min_gap:
            filtered_list.append((start_time, end_time))
    
    return filtered_list

# cut, merge and paste of non-speaking video
def merge_non_speaking_video_clips(video_file_path, timestamps_list, output_file):
    main_video = VideoFileClip(video_file_path)
    segments = []
    
    for timestamp in timestamps_list:
        start_time = timestamp[0]
        end_time = timestamp[1]
        segment = main_video.subclip(start_time, end_time)
        segments.append(segment)
    
    merged_clip = concatenate_videoclips(segments)
    merged_clip.write_videofile(output_file, codec='libx264', fps=main_video.fps)
    # Explicitly close video clips
    merged_clip.close()
    main_video.close()
    
    print(f"Merged non-speaking video saved as {output_file}")

# cut, merge and paste of speaking video
def merge_speaking_video_clips(video_file_path, timestamps_list, output_file):
    main_video = VideoFileClip(video_file_path)
    segments_outside = []
    start_time_main = 0
    
    for timestamp in timestamps_list:
        start_time = timestamp[0]
        end_time = timestamp[1]
        
        if start_time > start_time_main:
            segment_before = main_video.subclip(start_time_main, start_time)
            segments_outside.append(segment_before)
        
        start_time_main = end_time
    
    if main_video.duration > start_time_main:
        segment_after = main_video.subclip(start_time_main, main_video.duration)
        segments_outside.append(segment_after)
    
    merged_clip = concatenate_videoclips(segments_outside)
    merged_clip.write_videofile(output_file, codec='libx264', fps=main_video.fps)

    # Explicitly close video clips
    merged_clip.close()
    main_video.close()
    
    print(f"Merged speaking video saved as {output_file}")

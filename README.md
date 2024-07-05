**Task - 1:**

Given a video sequence of a single person speaking, write a program that identifies speaking and non speaking parts in the video sequence and export two different videos with speaking and non speaking parts.

Some ideas and hints:
1. Can you do it by audio?
2. Can you write an algorithm that can detect if lips are open or closed?

You can use - opencv, python, ffmpeg, face alignment 

**Answer:**

1. I created a Python script which exports two videos: speaking and non-speaking (based on audio detection).<br><br>
    **Question 1** is the main file. The inputs are:
   - video_file_path: "File path of the input video"
   - silence_time: "Minimum time threshold in seconds to detect silent zones"
   - min_time_gap: "Time for break after removing silent zones; it should be less than or equal to `silence_time`. This ensures that the entire silence time interval is not removed."
   - output_folder: "Location to save output; it saves extracted audio, speaking, and non-speaking parts in this location".<br><br>
   If you do not change the output folder, it will automatically create a folder where the main file exists.

2. I also wrote an algorithm that takes a video as input and displays whether the lips are opened or not while playing the video.<br><br>
    **Question 2** is the algorithm file.

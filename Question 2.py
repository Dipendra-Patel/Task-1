'''

Algorithm to detect whether lips are opened or not:

1. Initialization:
   - Import necessary libraries (cv2 for OpenCV, dlib for face detection and landmark prediction).
   - Load dlib's pre-trained facial landmark detector & input video.

2. Constants Definition:
   - Define constants:
     - THRESHOLD_RATIO: Aspect ratio threshold for determining open/closed lips.
     - CONSECUTIVE_FRAMES_THRESHOLD: Number of minimum consecutive frames where the aspect ratio must be above the threshold to consider the lips open.
     - OPENED_COUNT_THRESHOLD: = Total count of times lips are detected as open throughout the video.

3. Video Input:
   - Start video stream (cap) from a file. Also initialize dlib's facial landmark detector.

4. Processing Loop:
   - Continuously read frames (frame) from the video stream until the end of the video or user interrupts.

5. Face Detection and Landmark Localization:
   - Convert each frame to grayscale.
   - Use detector to detect faces in the grayscale frame (gray).
   - For each detected face, use predictor to localize 68 facial landmarks (landmarks).

6. Lips Region Identification:
   - Extract lips landmarks from the 68 landmarks (typically from 49 to 68).

7. Calculate Lips Aspect Ratio:
   - Compute the lips aspect ratio (MAR) using the formula given in "Soukupová and Čech - 2016 paper".
     where A and B are Euclidean distances between specific lips landmarks, and C is the distance between horizontal landmarks.

8. Determine Lips State:
   - Compare the calculated MAR with THRESHOLD_RATIO.
   - If MAR is above THRESHOLD_RATIO, increment a frame_count variable.
   - Track consecutive frames (frame_count) where the lips remains open.
   - If frame_count reaches CONSECUTIVE_FRAMES_THRESHOLD, consider the lips as open.
   - Track the total count of times the lips is detected as open (opened_count).

9. Visual Feedback:
   - Display visual feedback on the frame:
     - Draw the lips region and display the calculated MAR.
     - Display the current count of times the lips have been detected as open (opened_count).

10. User Interaction:
    - Exit the processing loop when a termination condition is met (end of video or user action).

11. Cleanup:
    - Release the video stream (cap).
    - Close all windows and release any resources used by OpenCV.

    '''
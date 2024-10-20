import cv2
from typing import Final, List, Optional
from numpy import ndarray
import os

def readh264(h264_file: str, nth_frame: Optional[int] = None) -> (List[ndarray], int):
    """
    Read an h264 file and return a list of frames. Optionally, only read every nth frame.
    :param h264_file: The path to the h264 file.
    :param nth_frame: Only read every nth frame. If None, read all frames. If -1, read no frames.
    :return: A list of frames read and the total number of frames in the video(counting non-read frames).
    """
    if os.path.getsize(h264_file) == 0:
        return [], 0
    cap = cv2.VideoCapture(h264_file)

    if not cap.isOpened():
        raise Exception(f"Could not open {h264_file}")

    frames: List[ndarray] = []
    frame_count: int = 0
    consecutive_errors: int = 0
    max_consecutive_errors = 10 # If we encounter n consecutive errors, we assume we have reached the end of the video. Since the h264 files are stream captures, a few errors are expected.

    while True:
        ret, frame = cap.read()
        if not ret:
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                break
        else:
            consecutive_errors = 0
            frame_count += 1
            if nth_frame is not None and (frame_count % nth_frame != 0 or nth_frame == -1):
                continue
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()
    return frames, frame_count

def readh264frame(h264_file: str, frame_index: int) -> ndarray:
    """
    Read a specific frame from an h264 file.
    :param h264_file: The path to the h264 file.
    :param frame_index: The index of the frame to read.
    :return: The frame at the specified index.
    """
    cap = cv2.VideoCapture(h264_file)

    if not cap.isOpened():
        raise Exception(f"Could not open {h264_file}")

    frame = None
    frame_count: int = 0
    consecutive_errors: int = 0
    max_consecutive_errors = 10  # If we encounter n consecutive errors, we assume we have reached the end of the video. Since the h264 files are stream captures, a few errors are expected.

    while frame_count < frame_index:
        ret, frame = cap.read()
        if not ret:
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                break
        else:
            consecutive_errors = 0
            frame_count += 1

    cap.release()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if frame is not None else None
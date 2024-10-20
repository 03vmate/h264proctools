import sys
from readh264 import readh264
import glob
import json
import os

h264_files = sorted(glob.glob(os.path.join(sys.argv[1], '*.h264')))

frame_map = {}
total_count = 0
for h264_file in h264_files:
    frames, frame_count = readh264(h264_file, -1)
    if frame_count == 0:
        continue
    print(f"{h264_file}: {frame_count} frames")
    frame_map[h264_file] = {"frame_count": frame_count, "starting_index": total_count}
    total_count += frame_count

# Create filename that does not exist
base_name = "frame_map"
index = 0
if os.path.exists(f"{base_name}.json"):
    base_name = f"{base_name}_{index}"

while os.path.exists(f"{base_name}_{index}.json"):
    index += 1

# Save the frame map to a JSON file
with open(f"{base_name}_{index}.json", "w") as f:
    json.dump(frame_map, f)
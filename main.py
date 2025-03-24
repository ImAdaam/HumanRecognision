from pathlib import Path
import videoFragmentation
import videoMaker
import request
import time

start_time = time.time()  # Start timer
video_path = "test.mp4"
frame_interval = 2

output_folder = "sightings/extracted_frames"
videoFragmentation.extract_frames_with_classes(video_path, output_folder, frame_interval)

output_video = "00_output_video.mp4"
frame_rate = 14 #30

folder_path = Path("sightings")
for folder in folder_path.iterdir():
    if folder.is_dir():
        folder_name = "sightings/"+folder.name
        video_name = videoMaker.make_video(folder_name, folder_name+'/'+output_video, frame_rate)
        request.post(video_name)

end_time = time.time()  # End timer
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")
from pathlib import Path
import videoFragmentation
import videoMaker
import request

# TODO: how long videos will be coming?
video_path = "test.mp4"
frame_interval = 2

output_folder = "sightings/extracted_frames"
videoFragmentation.extract_frames_with_classes(video_path, output_folder, frame_interval)

output_video = "output_video.mp4"
frame_rate = 16 #30

folder_path = Path("sightings")
for folder in folder_path.iterdir():
    if folder.is_dir():
        folder_name = "sightings/"+folder.name
        videoMaker.make_video(folder_name, folder_name+'/'+output_video, frame_rate)

# TODO: fetch after complete
# request.post()
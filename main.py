from pathlib import Path
import videoFragmentation
import videoMaker

# TODO: how long videos will be coming
# Example usage
video_path = "test.mp4"  # Change this to your video file
frame_interval = 5  # Change this to extract every 10th frame

# Example run
output_folder = "sightings/extracted_frames" # TODO: possible in the other function
videoFragmentation.extract_frames(video_path, output_folder, frame_interval)

output_folder = "sightings/extracted_frames_with_boxes"
videoFragmentation.extract_frames_with_boxes(video_path, output_folder, frame_interval)

# TODO: make video from images
output_video = "output_video.mp4"
frame_rate = 30  # Adjust as needed

folder_path = Path("sightings")
for folder in folder_path.iterdir():
    if folder.is_dir():
        folder_name = "sightings/"+folder.name
        videoMaker.make_video(folder_name, folder_name+'/'+output_video, frame_rate)

# TODO: fetch after complete
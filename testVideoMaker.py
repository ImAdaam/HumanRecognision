import videoMaker

image_folder = "sightings/extracted_frames_0"
output_video = "sightings/extracted_frames_0/output_video.mp4"
frame_rate = 30  # Adjust as needed
videoMaker.make_video(image_folder, output_video, frame_rate)
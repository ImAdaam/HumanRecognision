import cv2
import imageDetection
from sighting import Sighting


def extract_frames_with_classes(video_path, output_folder, frame_interval=1):
    """
    Extract frames from a video runs OD on them and save them as images.

    :param video_path: Path to the input video file
    :param output_folder: Folder where extracted frames will be saved
    :param frame_interval: Extract every nth frame (default is 1, meaning extract every frame)
    """

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0

    sightings = []
    sightings_count = 0
    frames_to_save_after_sighting = 30

    frames_before_sighting = []

    # first sighting if it's empty then there were no sightings
    new_sighting = Sighting([], [], [], sightings_count, output_folder, frames_to_save_after_sighting)
    sightings.append(new_sighting)
    sightings_count += 1

    while True:
        success, frame = cap.read()

        if not success:
            break  # End of video

        # Save every nth frame
        if frame_count % frame_interval == 0:
            observe, boxed_frame = imageDetection.analyse_with_return(frame)
            # save before frames
            for _sighting in sightings:
                _sighting.add_frame_before(frame)

            if observe:
                new_sighting = None  # Sighting class to store the frame
                if sightings[-1].needs_after_frames():
                    new_sighting = sightings[-1]
                else:
                    new_sighting = Sighting([], [], [], sightings_count, output_folder, frames_to_save_after_sighting)
                    sightings.append(new_sighting)
                    sightings_count += 1
                    new_sighting.add_frame_array_before(frames_before_sighting)

                for _sighting in sightings:
                    _sighting.add_sighting(boxed_frame)
        else:
            for _sighting in sightings:
                _sighting.add_frame_after(frame)

        frame_count += 1

    cap.release()
    for _sighting in sightings:
        _sighting.save_frames()
    print(f"Extraction complete! {frame_count} frames saved in '{output_folder}'.")

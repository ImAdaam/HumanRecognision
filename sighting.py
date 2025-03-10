import os
import cv2
from ultralytics.engine.results import Results
import threading

class Sighting:
    def __init__(self, frames_before, sighting, frames_after, number, folder, frames_to_save=60):
        self.frames_before = frames_before
        self.frames_after = frames_after
        self.frames_to_save = frames_to_save
        self.sighting = sighting
        self.frames_to_save_after = frames_to_save
        self.frames_to_save = frames_to_save
        self.number = number
        self.folder = folder
        self.sightings_count = 0

    def add_frame_array_before(self, array):
        self.frames_before = array

    def add_sighting(self, frame):
        if self.frames_to_save_after < self.frames_to_save:
            self.reset_frames_to_save()
        self.sighting.append(frame)
        self.sightings_count += 1

    def add_frame_after(self, frame):
        if self.frames_to_save_after > 1:
            self.frames_after.append(frame)
            self.frames_to_save_after -= 1

    def needs_after_frames(self):
        return self.frames_to_save_after > 0
    
    def reset_frames_to_save(self):
        self.frames_to_save_after = self.frames_to_save
        self.sighting.extend(self.frames_after)
        self.frames_after = []

    def save_frames(self):
        self.folder = self.folder + '_' + str(self.number)
        os.makedirs(self.folder, exist_ok=True)

        t1 = threading.Thread(target=self.save_prev_frames())
        t2 = threading.Thread(target=self.save_sighting_frames())
        t3 = threading.Thread(target=self.save_after_frames())

        t1.start()
        t2.start()
        t3.start()

        # self.save_prev_frames()
        # self.save_sighting_frames()
        # self.save_after_frames()


    def save_prev_frames(self):
        for _id, _frame in enumerate(self.frames_before):
            frame_filename = os.path.join(self.folder + '/', f"a_frame_prev_{_id:04d}.jpg")
            cv2.imwrite(frame_filename, _frame)

    def save_sighting_frames(self):
        for _id, _frame in enumerate(self.sighting):
            frame_filename = os.path.join(self.folder + '/', f"b_frame_{_id:05d}.jpg")
            if isinstance(_frame, Results):
                _frame = _frame.plot()  # Extracts an image (NumPy array) with detections
            cv2.imwrite(frame_filename, _frame)

    def save_after_frames(self):
        for _id, _frame in enumerate(self.frames_after):
            frame_filename = os.path.join(self.folder  + '/', f"c_frame_after_{_id:05d}.jpg")
            cv2.imwrite(frame_filename, _frame)
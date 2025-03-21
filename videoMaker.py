import cv2
import os

def make_video(image_folder, output_video, frame_rate):
    # Get all image files and sort them
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    if len(images) == 0:
        return

    # Read the first image to get dimensions
    first_image = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"avc1")  # Change codec if needed (e.g., 'XVID')
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    # Add images to the video
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    # Release the video writer
    video.release()
    cv2.destroyAllWindows()

    print(f"Video saved as {output_video}")

    return output_video

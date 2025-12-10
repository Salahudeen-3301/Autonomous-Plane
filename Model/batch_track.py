from ultralytics import YOLO
import os

# --- Load your trained YOLOv11 model ---
model = YOLO(r"C:\Users\swnaf\Downloads\yolo11-stl\trained_models\yolo_weights\model8.pt")

# --- Paths ---
video_folder = r"C:\Users\swnaf\OneDrive\Desktop\Model_Videos\test\with_people\Resized1056"          # folder containing all videos
  # resized videos
output_folder = r"C:\Users\swnaf\Downloads\yolo11-stl\runs\full23"  # where results go
tracker_type = r"C:\Users\swnaf\Downloads\yolo11-stl\trained_models\bytetrack.yaml"       # tracker config

os.makedirs(output_folder, exist_ok=True)

# --- Track results summary ---
min_conf = 0.2
min_frames = 8
videos_with_people = 0
total_videos = 0

for video_name in os.listdir(video_folder):
    number = 0
    confidences = []
    found = False
    if not video_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        continue

    total_videos += 1
    video_path = os.path.join(video_folder, video_name)
    print(f"\n🎥 Processing: {video_name}")

    # Run tracking
    results = model.track(
        source=video_path,
        save=True,
        tracker=tracker_type,
        show=False,
        imgsz=(672,1056),
        project=output_folder,
        name="Track",           # prevents subfolders
        exist_ok=True,
        persist=False,
        stream=True,
        verbose=False
    )

    # Collect unique IDs
    unique_ids = set()
    for result in results:
        boxes = getattr(result, "boxes", None)
        if boxes is not None and (boxes.id is not None or boxes.conf is not None):
            if boxes.id is not None:
                ids = boxes.id.cpu().numpy()
                unique_ids.update(ids)
            else:
                for conf in result.boxes.conf:
                    conf=conf.item()
                    # print(conf)
                    if conf >= min_conf:
                        number += 1


    # Print results for this video
    if len(unique_ids) == 0 and  number < min_frames:
        print(f"⚠️  No people detected in {video_name}")
    else:
        print(f"✅ {len(unique_ids)} people detected in {video_name}")
        videos_with_people += 1

# --- Final summary ---
print("\n📊 Final Summary:")
print(f"Total videos processed: {total_videos}")
print(f"Videos with people detected: {videos_with_people}")
print(f"Videos with no detections: {total_videos - videos_with_people}")
print("\n✅ All videos processed successfully!")
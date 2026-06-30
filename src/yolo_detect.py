import pandas as pd

from ultralytics import YOLO
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

# Project root (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Images folder
IMAGE_DIR = PROJECT_ROOT / "data" / "raw" / "images"

# Output CSV
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "yolo_detections.csv"

# Load YOLOv8 Nano model
model = YOLO("yolov8n.pt")

# COCO classes treated as products
PRODUCT_CLASSES = {
    "bottle",
    "cup",
    "wine glass",
    "bowl",
    "vase",
    "cell phone",
    "book",
    "handbag",
    "backpack",
    "sports ball"
}

# ==========================================================
# Find Images (Search All Subfolders)
# ==========================================================

image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

image_files = [
    f for f in IMAGE_DIR.rglob("*")
    if f.is_file() and f.suffix.lower() in image_extensions
]

print("=" * 60)
print("YOLO OBJECT DETECTION")
print("=" * 60)
print("Image directory:", IMAGE_DIR)
print(f"Found {len(image_files)} images\n")

if len(image_files) == 0:
    print("No images found!")
    print("Check your image folder path.")
    exit()

# ==========================================================
# Run Detection
# ==========================================================

results_list = []

for image_path in image_files:

    print(f"Processing: {image_path.name}")

    channel_name = image_path.parent.name
    message_id = image_path.stem

    try:
        prediction = model(str(image_path), verbose=False)[0]

        detected_objects = []
        confidences = []

        has_person = False
        has_product = False

        if prediction.boxes is not None:

            for box in prediction.boxes:

                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])

                detected_objects.append(class_name)
                confidences.append(round(confidence, 3))

                if class_name == "person":
                    has_person = True

                if class_name in PRODUCT_CLASSES:
                    has_product = True

        # --------------------------------------------------
        # Classification
        # --------------------------------------------------

        if has_person and has_product:
            image_category = "promotional"

        elif has_product and not has_person:
            image_category = "product_display"

        elif has_person and not has_product:
            image_category = "lifestyle"

        else:
            image_category = "other"

        confidence_score = max(confidences) if confidences else 0

        results_list.append({
            "message_id": message_id,
            "channel_name": channel_name,
            "image_name": image_path.name,
            "detected_objects": ", ".join(detected_objects),
            "confidence_score": confidence_score,
            "image_category": image_category
        })

    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")

# ==========================================================
# Save CSV
# ==========================================================

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

columns = [
    "message_id",
    "channel_name",
    "image_name",
    "detected_objects",
    "confidence_score",
    "image_category"
]

df = pd.DataFrame(results_list, columns=columns)

df.to_csv(OUTPUT_CSV, index=False)

print("\n" + "=" * 60)
print("Detection Complete")
print("=" * 60)
print(f"Images processed : {len(image_files)}")
print(f"Rows saved       : {len(df)}")
print(f"CSV saved to     : {OUTPUT_CSV}")

print("\nFirst five rows:")
print(df.head())
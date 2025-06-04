import os
import cv2
import torch
import numpy as np
from ultralytics import YOLO
import easyocr
import textsort

os.makedirs('CV/Result', exist_ok=True)
OUTPUT_VIDEO_PATH = os.path.join('Result', 'proce_video1.avi')

model_plate = YOLO('carplate_model/weights/best.pt').to('cuda' if torch.cuda.is_available() else 'cpu')
model_chars = YOLO('carpIate_modeI2/weights/best.pt').to('cuda' if torch.cuda.is_available() else 'cpu')  # Модель для символов
reader = easyocr.Reader(['ru'], gpu=torch.cuda.is_available())

cap = cv2.VideoCapture('videos/sample_short3.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, 24, (1920, 1080))

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    plate_results = model_plate(frame)[0]
    boxes = plate_results.boxes.xyxy.cpu().numpy().astype(np.int32)

    for x1, y1, x2, y2 in boxes:
        plate_roi = frame[y1:y2, x1:x2]

        char_results = model_chars(plate_roi)[0]
        char_boxes = char_results.boxes.xyxy.cpu().numpy().astype(np.int32)
        char_confidences = char_results.boxes.conf.cpu().numpy()
        char_classes = char_results.boxes.cls.cpu().numpy().astype(int)

        chars = []
        for (cx1, cy1, cx2, cy2), conf, cls_id in zip(char_boxes, char_confidences, char_classes):
            if conf > 0.5:
                char = model_chars.names[cls_id]
                chars.append((cx1, char))

        chars.sort(key=lambda x: x[0])
        plate_text = ''.join([char[1] for char in chars])

        plate_gray = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
        img_filter = cv2.bilateralFilter(plate_gray, 15, 20, 20)
        ocr_result = reader.readtext(
            plate_gray,
            allowlist='АВЕКМНОРСТУХ0123456789',
            contrast_ths=8,
            adjust_contrast=0.85,
            add_margin=0.015,
            width_ths=20,
            decoder='beamsearch',
            text_threshold=0.1,
            batch_size=8,
            beamWidth=32
        )

        final_text = plate_text if len(plate_text) > 0 else ''.join([res[1] for res in ocr_result])

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        frame = cv2.putText(frame, final_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        final_text = textsort.text_filter(final_text)
        print(f'Обнаруженный текст:{final_text}')

    video_out.write(frame)
    frame_count += 1
    print(f'Обработан кадр: {frame_count}')

cap.release()
video_out.release()
cv2.destroyAllWindows()

print(f'Обработано кадров: {frame_count}')
print(f'Видео сохранено: {OUTPUT_VIDEO_PATH}')
import cv2

def extract_first_five_frames(video_path, output_path):
    # 打開影片檔案
    cap = cv2.VideoCapture(video_path)

    # 確保影片成功打開
    if not cap.isOpened():
        print("無法打開影片檔案")
        return

    # 計算影片的總幀數
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 限制處理的幀數，這裡設定為前五幀
    num_frames_to_extract = min(5, total_frames)

    # 逐一處理每一幀
    for frame_number in range(120,150,5):
        ret, frame = cap.read()

        # 確保成功讀取一幀
        if ret:
            # 在這裡可以進行進一步的處理，例如儲存或顯示幀
            # 這裡示範將每一幀存為圖片檔
            frame_filename = f"frame_{frame_number + 1}.jpg"
            cv2.imwrite(frame_filename, frame)
            print(f"已儲存 {frame_filename}")
        else:
            print(f"無法讀取第 {frame_number + 1} 幀")

    # 釋放資源
    cap.release()

video_path = "aelzhcnwgf.mp4"  # 輸入你的影片檔案路徑
output_path = "code"  # 輸出路徑，如果不存在，請先建立資料夾

    # 執行函數
extract_first_five_frames(video_path, output_path)

# /usr/bin/env python3
# -*- coding=utf-8 -*-
# 拍摄数据集
import cv2
import os

# 创建保存图片的文件夹
save_folder = '../CocoDataset/images/train2017'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 打开摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

img_index = 1
while True:
    # 读取一帧
    ret, frame = cap.read()
    
    # 如果正确读取帧，ret为True
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # 显示帧
    cv2.imshow('Frame', frame)
    
    # 按下空格键保存图片
    if cv2.waitKey(1) == 32:  # 32是空格键的ASCII码
        filename = os.path.join(save_folder, f"{img_index}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        img_index += 1
    
    # 按下'q'键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()

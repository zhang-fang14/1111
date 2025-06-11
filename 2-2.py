import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像（修改路径为图像2-2的实际路径）
image_path = '2-2.tif'  # 替换为你的图像路径
img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转为 RGB 格式用于展示

# 核大小列表
kernel_sizes = [3, 5, 7]

# 创建图像展示函数
def show_results(title, filtered_images, kernel_sizes):
    plt.figure(figsize=(12, 4))
    for i, (img, k) in enumerate(zip(filtered_images, kernel_sizes)):
        plt.subplot(1, len(filtered_images), i + 1)
        plt.imshow(img)
        plt.title(f'{title} {k}x{k}')
        plt.axis('off')
    plt.tight_layout()
    plt.show()

# 1. 均值滤波
mean_filtered = [cv2.blur(img, (k, k)) for k in kernel_sizes]
show_results("均值滤波", mean_filtered, kernel_sizes)

# 2. 高斯滤波
gaussian_filtered = [cv2.GaussianBlur(img, (k, k), 0) for k in kernel_sizes]
show_results("高斯滤波", gaussian_filtered, kernel_sizes)

# 3. 中值滤波（仅适用于灰度或单通道图像，但 OpenCV 会自动处理彩色图像每个通道）
median_filtered = [cv2.medianBlur(img, k) for k in kernel_sizes]
show_results("中值滤波", median_filtered, kernel_sizes)

import cv2
import matplotlib.pyplot as plt

# 加载图像（灰度模式）
image_path = '2-3.tif'  # 替换为你的图像路径
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 固定阈值
fixed_thresh = 127

# ========== （1）二值化处理 ==========
# 1.1 固定阈值二值化
_, thresh_fixed = cv2.threshold(img, fixed_thresh, 255, cv2.THRESH_BINARY)

# 1.2 Otsu算法阈值
_, thresh_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 1.3 固定阈值 + Otsu 联合（无实际意义，效果和 Otsu 相同，只是演示）
_, thresh_combined = cv2.threshold(img, fixed_thresh, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# ========== （2）自适应阈值处理 ==========
# 使用高斯加权平均法，自适应方式为 ADAPTIVE_THRESH_GAUSSIAN_C
adaptive_gaussian = cv2.adaptiveThreshold(img, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY,
                                          11, 2)

# 使用均值法，自适应方式为 ADAPTIVE_THRESH_MEAN_C
adaptive_mean = cv2.adaptiveThreshold(img, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY,
                                      11, 2)

# ========== 显示图像结果 ==========
titles = ['原图',
          f'固定阈值（T={fixed_thresh}）',
          'Otsu 阈值',
          f'固定+Otsu 阈值',
          '自适应阈值（高斯）',
          '自适应阈值（均值）']
images = [img, thresh_fixed, thresh_otsu, thresh_combined, adaptive_gaussian, adaptive_mean]

plt.figure(figsize=(12, 6))
for i in range(6):
    plt.subplot(2, 3, i+1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')
plt.tight_layout()
plt.show()

import cv2
import numpy as np

# 1. 读取图像
image_path = r"2-1.tif"
img = cv2.imread(image_path)
if img is None:
    print(f"错误：无法读取图像，请检查路径：{image_path}")
    exit()

# 1. 缩放 10%，使用双线性插值
scale_percent = 10
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
cv2.imshow("缩放10% (INTER_LINEAR)", resized)
cv2.imwrite("缩放10%.jpg", resized)

# 2. 以图像中心为旋转中心，向左旋转45°，保持图像大小不变
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M_rotate = cv2.getRotationMatrix2D(center, 45, 1.0)  # 逆时针45°
rotated = cv2.warpAffine(img, M_rotate, (w, h))
cv2.imshow("旋转45° (中心)", rotated)
cv2.imwrite("旋转45°.jpg", rotated)

# 3. 平移：水平10像素，垂直5像素
M_translate = np.float32([[1, 0, 10], [0, 1, 5]])
translated = cv2.warpAffine(img, M_translate, (w, h))
cv2.imshow("平移(10,5)", translated)
cv2.imwrite("平移(10,5).jpg", translated)

# 4. 透视变换：任选4点
pts1 = np.float32([[50, 50], [w-50, 50], [w-50, h-50], [50, h-50]])  # 原图4点
pts2 = np.float32([[10, 100], [w-100, 30], [w-50, h-100], [100, h-30]])  # 新图4点
M_persp = cv2.getPerspectiveTransform(pts1, pts2)
perspective = cv2.warpPerspective(img, M_persp, (w, h))
cv2.imshow("透视变换", perspective)
cv2.imwrite("透视变换.jpg", perspective)

cv2.waitKey(0)
cv2.destroyAllWindows()

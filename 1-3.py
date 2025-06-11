import cv2
import numpy as np

# 创建两个示例图像
# 第一个图像：红色矩形
image1 = np.zeros((300, 300, 3), dtype=np.uint8)
image1[:, :] = (0, 0, 255)  # BGR格式的红色

# 第二个图像：绿色矩形
image2 = np.zeros((300, 300, 3), dtype=np.uint8)
image2[:, :] = (0, 255, 0)  # BGR格式的绿色

# 使用+运算符进行图像加法
add_operator = image1 + image2

# 使用cv2.add函数进行图像加法
add_function = cv2.add(image1, image2)

# 显示结果
cv2.imshow('Image 1 (Red)', image1)
cv2.imshow('Image 2 (Green)', image2)
cv2.imshow('Addition with + operator', add_operator)
cv2.imshow('Addition with cv2.add()', add_function)

# 打印一些像素值进行比较
print("使用+运算符的(0,0)像素值:", add_operator[0, 0])  # 应为(0, 255, 255)
print("使用cv2.add()的(0,0)像素值:", add_function[0, 0])  # 应为(0, 255, 255)

# 等待按键后关闭所有窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
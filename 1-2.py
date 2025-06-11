import cv2
import numpy as np

# 创建50x50的黑色图像(3通道，BGR格式)
black_square = np.zeros((50, 50, 3), dtype=np.uint8)

# 显示黑色正方形
cv2.imshow('Black Square', black_square)

# 保存图像
cv2.imwrite('black_square.jpg', black_square)

# 等待按键后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
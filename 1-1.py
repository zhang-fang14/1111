import cv2
import numpy as np

image_path = "1.tif"
original_img = cv2.imread(image_path)

# 检查图像是否成功加载
if original_img is None:
    print(f"错误：无法读取图像，请检查路径：{image_path}")
else:
    # 2. 获取原始尺寸并减半
    height, width = original_img.shape[:2]
    resized_img = cv2.resize(original_img, (width // 2, height // 2))

    # 3. 显示图像
    cv2.imshow("Original Image", original_img)
    cv2.imshow("Resized Image (50%)", resized_img)

    # 4. 保存缩小后的图像
    output_path = r"D:\天才备忘录\大三下\计算机视觉\实验1\实验1\测试图像（实验一）\图像的读取、写入、显示\resized_output.jpg"
    cv2.imwrite(output_path, resized_img)
    print(f"缩小后的图像已保存至：{output_path}")

# ============================================
# （ii）创建50x50黑色正方形图像
# ============================================

# 1. 创建全黑图像（3通道BGR格式）
black_square = np.zeros((50, 50, 3), dtype=np.uint8)

# 2. 显示和保存
cv2.imshow("Black Square", black_square)
black_square_path = r"D:\天才备忘录\大三下\计算机视觉\实验1\实验1\测试图像（实验一）\图像的读取、写入、显示\black_square.jpg"
cv2.imwrite(black_square_path, black_square)
print(f"黑色正方形已保存至：{black_square_path}")

# ============================================
# 等待按键关闭所有窗口
# ============================================
cv2.waitKey(0)
cv2.destroyAllWindows()
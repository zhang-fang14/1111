import os
import random
import shutil
from sklearn.model_selection import train_test_split

# 原始数据路径
data_dir = r"D:\天才备忘录\大三下\计算机视觉\shijueshiyan\lables\all_data"
image_dir = os.path.join(data_dir, "images")
label_dir = os.path.join(data_dir, "labels")

# 输出路径
output_dir = r"D:\天才备忘录\大三下\计算机视觉\shijueshiyan\lables\split_data"
os.makedirs(output_dir, exist_ok=True)

# 创建子目录
for subset in ["train", "val", "test"]:
    os.makedirs(os.path.join(output_dir, subset, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, subset, "labels"), exist_ok=True)

# 获取所有图像文件名（不带扩展名）
image_files = [f.split(".")[0] for f in os.listdir(image_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

# 设置随机种子以保证可重复性
random.seed(42)

# 划分比例：70%训练，15%验证，15%测试
train_files, test_files = train_test_split(image_files, test_size=0.3, random_state=42)
val_files, test_files = train_test_split(test_files, test_size=0.5, random_state=42)


def copy_files(files, subset):
    """将文件和标签复制到对应的子集目录"""
    for file in files:
        # 查找图像文件（考虑不同扩展名）
        for ext in [".jpg", ".png", ".jpeg"]:
            src_img = os.path.join(image_dir, file + ext)
            if os.path.exists(src_img):
                dst_img = os.path.join(output_dir, subset, "images", file + ext)
                shutil.copy(src_img, dst_img)
                break

        # 复制标签文件
        src_label = os.path.join(label_dir, file + ".txt")
        if os.path.exists(src_label):
            dst_label = os.path.join(output_dir, subset, "labels", file + ".txt")
            shutil.copy(src_label, dst_label)


# 复制文件到各自目录
copy_files(train_files, "train")
copy_files(val_files, "val")
copy_files(test_files, "test")

print("✅ 数据集划分完成！")
print(f"📊 训练集数量: {len(train_files)}")
print(f"📊 验证集数量: {len(val_files)}")
print(f"📊 测试集数量: {len(test_files)}")
print(f"📁 输出路径: {output_dir}")
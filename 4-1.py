import os
import shutil

# 设置你的路径
image_dir = r'D:\天才备忘录\大三下\计算机视觉\shijueshiyan\dataset_raw'
label_dir = r'D:\天才备忘录\大三下\计算机视觉\shijueshiyan\lables'

output_image_dir = os.path.join(label_dir, 'all_data', 'images')
output_label_dir = os.path.join(label_dir, 'all_data', 'labels')

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

# 去前导零的函数
def normalize_filename(f):
    return str(int(os.path.splitext(f)[0]))  # '000001.txt' -> '1'

# 获取文件映射
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
label_files = [f for f in os.listdir(label_dir) if f.lower().endswith('.txt') and f.startswith('000')]

image_map = {normalize_filename(f): f for f in image_files}
label_map = {normalize_filename(f): f for f in label_files}

common_keys = set(image_map.keys()) & set(label_map.keys())

for key in common_keys:
    img_file = image_map[key]
    lbl_file = label_map[key]
    shutil.copy(os.path.join(image_dir, img_file), os.path.join(output_image_dir, img_file))
    shutil.copy(os.path.join(label_dir, lbl_file), os.path.join(output_label_dir, lbl_file))

print(f"✅ 成功配对并合并了 {len(common_keys)} 组图像和标签。")
print(f"📁 图像输出路径: {output_image_dir}")
print(f"📁 标签输出路径: {output_label_dir}")

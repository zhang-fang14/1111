import os
import cv2
import numpy as np
from imgaug import augmenters as iaa
from icrawler.builtin import GoogleImageCrawler

# ========== 第一部分：图像采集 ==========

def download_images(keyword, num_images=60, save_dir='dataset_raw'):
    os.makedirs(save_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={'root_dir': save_dir})
    crawler.crawl(keyword=keyword, max_num=num_images, min_size=(128, 128))

# ========== 第二部分：图像增强 ==========

def augment_images(input_dir='dataset_raw', output_dir='dataset_augmented', augment_per_image=4):
    os.makedirs(output_dir, exist_ok=True)

    # 增强流水线定义
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),                          # 水平翻转
        iaa.Affine(
            scale=(0.8, 1.2),                    # 缩放
            translate_percent=(-0.1, 0.1),       # 平移
            rotate=(-15, 15),                    # 旋转
        ),
        iaa.AddToHueAndSaturation((-20, 20)),    # 色彩扰动
        iaa.Crop(percent=(0, 0.1)),              # 随机裁剪
    ])

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    count = 0

    for file in image_files:
        path = os.path.join(input_dir, file)
        img = cv2.imread(path)
        if img is None:
            print(f"⚠️ 无法读取图像：{file}")
            continue

        # 将图像增强多次
        for i in range(augment_per_image):
            aug_img = seq(image=img)
            out_path = os.path.join(output_dir, f"{count:04d}.jpg")
            cv2.imwrite(out_path, aug_img)
            count += 1

    print(f"\n✅ 图像增强完成：共生成 {count} 张增强图像，已保存至：{output_dir}")

# ========== 主程序入口 ==========

if __name__ == "__main__":
    print("🚀 开始图像下载和增强任务...\n")

    # 步骤 1：爬取不少于 50 张图像
    keyword = "rehabilitation training"
    print(f"🔍 正在下载图像：'{keyword}' ...")
    download_images(keyword=keyword, num_images=60, save_dir='dataset_raw')

    # 步骤 2：增强为不少于 200 张图像（每张图增强 4 次）
    print("\n🧪 开始图像增强...")
    augment_images(input_dir='dataset_raw', output_dir='dataset_augmented', augment_per_image=4)

    print("\n✅ 所有任务完成。你可以在 'dataset_augmented/' 文件夹中查看生成的数据集。")

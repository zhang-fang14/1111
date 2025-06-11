import os
import shutil
import random
import subprocess
import yaml


def create_dataset_yaml(output_dir, class_names):
    yaml_content = {
        'path': os.path.abspath(output_dir),
        'train': 'train/images',
        'val': 'val/images',
        'test': 'test/images',
        'names': {i: name for i, name in enumerate(class_names)}
    }

    yaml_path = os.path.join(output_dir, 'dataset.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_content, f, sort_keys=False)

    return yaml_path


def split_dataset(image_dir, label_dir, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "比例总和必须等于1"
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, split, 'labels'), exist_ok=True)

    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_files)

    num_images = len(image_files)
    train_end = int(num_images * train_ratio)
    val_end = train_end + int(num_images * val_ratio)

    for i, image_file in enumerate(image_files):
        base_name = os.path.splitext(image_file)[0]
        label_file = base_name + '.txt'

        if i < train_end:
            split = 'train'
        elif i < val_end:
            split = 'val'
        else:
            split = 'test'

        shutil.copy(os.path.join(image_dir, image_file),
                    os.path.join(output_dir, split, 'images', image_file))

        label_src = os.path.join(label_dir, label_file)
        if os.path.exists(label_src):
            shutil.copy(label_src, os.path.join(output_dir, split, 'labels', label_file))
        else:
            print(f"警告: 找不到标签文件 {label_src}")

    print(f"数据集划分完成！共处理 {num_images} 张图像")
    print(f"训练集: {train_end} | 验证集: {val_end - train_end} | 测试集: {num_images - val_end}")


def train_and_evaluate_yolov5(data_yaml, weights='yolov5s.pt', img_size=640, batch_size=8, epochs=50):
    yolov5_path = r"D:\shijueshiyan\yolov5-master"

    train_cmd = [
        "python", "train.py",
        "--img", str(img_size),
        "--batch", str(batch_size),
        "--epochs", str(epochs),
        "--data", data_yaml,
        "--weights", weights,
        "--device", "cpu"
    ]

    print("\n开始训练模型...")
    subprocess.run(train_cmd, check=True, cwd=yolov5_path)

    weights_path = os.path.join(yolov5_path, "runs", "train", "exp", "weights", "best.pt")
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"训练后的权重文件不存在: {weights_path}")

    val_cmd = [
        "python", "val.py",
        "--data", data_yaml,
        "--weights", weights_path,
        "--img", str(img_size),
        "--task", "test"
    ]

    print("\n开始评估模型...")
    subprocess.run(val_cmd, check=True, cwd=yolov5_path)

    print("\n检测完成，精度结果保存在 YOLOv5 默认路径下。你可以在 runs/val/exp/ 中查看 precision、recall、mAP 等指标。")


if __name__ == "__main__":
    # 路径设置（已更新）
    base_dir = r'D:\shijueshiyan'
    image_dir = os.path.join(base_dir, 'lables', 'all_data', 'images')
    label_dir = os.path.join(base_dir, 'lables', 'all_data', 'labels')
    output_dir = os.path.join(base_dir, 'split_dataset')

    class_names = ["your_class"]  # 替换为你的实际类别名称

    split_dataset(image_dir, label_dir, output_dir)
    data_yaml = create_dataset_yaml(output_dir, class_names)
    print(f"YAML配置文件已创建: {data_yaml}")

    train_and_evaluate_yolov5(data_yaml)

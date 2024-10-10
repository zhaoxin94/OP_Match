import os
import os.path as osp
import random

def split_data(image_dir, train_file, test_file, train_ratio=0.8, seed=42):
    # 设置随机数种子
    random.seed(seed)

    # image_list路径
    txt_dir = image_dir.replace('image', 'image_list')
    train_file = osp.join(txt_dir, train_file)
    test_file = osp.join(txt_dir, test_file)
    
    # 获取所有类别并分配数字标签
    class_names = sorted(os.listdir(image_dir))
    class_to_idx = {class_name: idx for idx, class_name in enumerate(class_names)}
    
    # 创建保存训练集和测试集路径和标签的文件
    with open(train_file, 'w') as train_f, open(test_file, 'w') as test_f:
        # 遍历每个类别的文件夹
        for class_name in class_names:
            class_path = os.path.join(image_dir, class_name)
            if os.path.isdir(class_path):
                # 获取该类别下的所有图像文件
                images = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
                
                # 随机打乱图像顺序
                random.shuffle(images)
                
                # 按照比例划分训练集和测试集
                split_idx = int(len(images) * train_ratio)
                train_images = images[:split_idx]
                test_images = images[split_idx:]
                
                # 将训练集图像路径和标签写入train_file
                for image in train_images:
                    image_path = os.path.join(class_path, image)
                    train_f.write(f"{image_path} {class_to_idx[class_name]}\n")
                
                # 将测试集图像路径和标签写入test_file
                for image in test_images:
                    image_path = os.path.join(class_path, image)
                    test_f.write(f"{image_path} {class_to_idx[class_name]}\n")

if __name__ == "__main__":
    image_dir = '/home/zhaoxin/data/das/indoor_event_4/image'  # 图像文件夹路径
    train_file = 'train.txt'  # 训练集文件名
    test_file = 'test.txt'    # 测试集文件名
    seed = 2024  # 随机种子，确保可重复性
    
    split_data(image_dir, train_file, test_file, seed=seed)

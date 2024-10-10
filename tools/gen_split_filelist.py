import random
import numpy as np


random.seed(2024)

class_list = ['dig', 'knock', 'shake', 'background', 'water', 'walk']
path = '/home/zhaoxin/data/das/opendas_single_channel_image/train'

n_share = 3
n_source_private = 0
n_source = n_share + n_source_private
source_list = class_list[:n_source]
target_list = class_list[:n_share] + class_list[n_source:]

print(source_list)
print(len(source_list))
print(target_list)
print(len(target_list))

labels = []
with open('filelist/opendas_train.txt', "r") as f:
    for line in f.readlines():
        _, label = line.split()
        label = int(label)
        labels.append(label)
print('length of the train dataset:',len(labels))

labels = np.array(labels)
labeled_idx = []
val_idx = []
unlabeled_idx = []

for i in range(n_source):
    idx = np.where(labels == i)[0]
    num_class = len(idx)
    print(num_class)
    label_per_class = int(0.1 * num_class)
    val_per_class = int(0.2 * num_class)
    idx = np.random.choice(idx, label_per_class + val_per_class, False)
    labeled_idx.extend(idx[:label_per_class])
    val_idx.extend(idx[label_per_class:])

labeled_idx = np.array(labeled_idx)
np.random.shuffle(labeled_idx)

unlabeled_idx = np.array(range(len(labels)))
unlabeled_idx = [idx for idx in unlabeled_idx if idx not in labeled_idx]
unlabeled_idx = [idx for idx in unlabeled_idx if idx not in val_idx]

print('有标签数据的长度:',len(labeled_idx))
print('验证数据的长度', len(val_idx))
print('无标签数据的长度', len(unlabeled_idx))

with open('filelist/opendas_train.txt', "r") as f0:
    with open('filelist/opendas_train_labeled.txt', "w") as f1:
        with open('filelist/opendas_val.txt', "w") as f2:
            with open('filelist/opendas_train_unlabeled.txt', "w") as f3:
                for i, line in enumerate(f0.readlines()):
                    path, label = line.split()
                    label = int(label)
                    if i in labeled_idx:
                        assert label < n_source, "something wrong!"
                        f1.write(line)
                    elif i in val_idx:
                        assert label < n_source, "something wrong!"
                        f2.write(line)
                    elif i in unlabeled_idx:
                        label = label if label < n_source else n_source
                        f3.write('{:} {:}\n'.format(path, label))
                    else:
                        raise NotImplementedError



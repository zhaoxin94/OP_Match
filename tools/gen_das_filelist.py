import os
import os.path as osp


class_list = ['dig', 'knock', 'shake', 'background', 'water', 'walk']
path = '/home/zhaoxin/data/das/opendas_single_channel_image/test'

n_share = 3
n_source_private = 0
n_source = n_share + n_source_private
source_list = class_list[:n_source]
target_list = class_list[:n_share] + class_list[n_source:]

print(source_list)
print(len(source_list))
print(target_list)
print(len(target_list))


with open('filelist/opendas_test.txt', "w") as f:
    for i in range(len(class_list)):
        cla = class_list[i]
        print('class:', cla)
        files = os.listdir(osp.join(path, cla))
        files.sort()
        for file in files:
            label = i if i < n_source else n_source
            f.write('{:} {:}\n'.format(osp.join(path, cla, file), label))

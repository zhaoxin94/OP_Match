python main.py --dataset opendas --out $1 --arch resnet_imagenet --lambda_oem 1.0 --lambda_socr 1.0 \
--batch-size 64 --lr 0.01 --seed 0 --mu 2 --epochs 100 --use-pretrain --staged-lr --gpu-id $2
import os
import os.path as osp
import argparse
import hashlib


def seed_hash(*args):
    """
    Derive an integer hash from all args, for use as a random seed.
    """
    args_str = str(args)
    return int(hashlib.md5(args_str.encode("utf-8")).hexdigest(), 16) % (2**31)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", "-m", default="OpenMatch", help="Method")
    parser.add_argument("--dataset",
                        "-d",
                        default="opendas",
                        help="Dataset",
                        choices=['opendas'])
    parser.add_argument("--n_trials",
                        "-n",
                        default=1,
                        type=int,
                        help="Repeat times")
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--lr', type=float, default=0.03)
    parser.add_argument('--epoch', type=int, default=50)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--exp_name', type=str, default='')
    parser.add_argument("--gpu", "-g", default=0, type=int, help="Gpu ID")
    parser.add_argument('--lambda_oem', type=float, default=0.1)
    parser.add_argument('--lambda_socr', type=float, default=0.5)
    parser.add_argument('--mu', type=int, default=2)
    parser.add_argument('--count-iter', type=str, default='fix_value')
    parser.add_argument('--eval-step',
                        default=1024,
                        type=int,
                        help='number of eval steps to run')
    parser.add_argument("--use-pretrain",
                        type=str2bool,
                        default=False,
                        help="Use Imagenet pretrained model or not.")
    parser.add_argument("--staged-lr",
                        type=str2bool,
                        default=False,
                        help="Use staged lr or not")

    args = parser.parse_args()

    exp_info = args.exp_name
    if exp_info:
        exp_info = '_' + exp_info

    exp_info = exp_info + f'_lr={args.lr}_batch-size={args.batch_size}_epoch={args.epoch}_lambda-oem={args.lambda_oem}_lambda-socr={args.lambda_socr}_count-iter={args.count_iter}'
    if args.use_pretrain:
        exp_info += '_use-pretrain'
    if args.staged_lr:
        exp_info += '_staged-lr'
    if args.count_iter == 'fix_value':
        exp_info += f'_eval-step={args.eval_step}'

    base_dir = osp.join('output', args.method, args.dataset, exp_info)

    for i in range(args.n_trials):
        output_dir = osp.join(base_dir, str(i + 1))
        seed = args.seed
        if args.seed < 0:
            seed = seed_hash(args.method, args.dataset, i)
        else:
            seed += i

        os.system(f'python main.py '
                  f'--dataset {args.dataset} '
                  f'--out {output_dir} '
                  f'--arch resnet_imagenet '
                  f'--lambda_oem {args.lambda_oem} '
                  f'--lambda_socr {args.lambda_socr} '
                  f'--batch-size {args.batch_size} '
                  f'--lr {args.lr} '
                  f'--seed {args.seed} '
                  f'--mu {args.mu} '
                  f'--epochs {args.epoch} '
                  f'--gpu-id {args.gpu} '
                  f'--count-iter {args.count_iter} '
                  f'--use-pretrain {args.use_pretrain} '
                  f'--staged-lr {args.staged_lr}')

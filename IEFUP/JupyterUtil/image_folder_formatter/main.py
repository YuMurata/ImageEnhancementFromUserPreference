from maker import make_folder
from mover import move_folder
from argparse import ArgumentParser


def _get_args():
    parser = ArgumentParser()
    parser.add_argument('-p', '--dl_path', required=True)
    parser.add_argument('-n', '--dl_num', required=True, type=int)

    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    make_folder(args.dl_path, args.dl_num)
    move_folder(args.dl_path)

    print('-- complete! --')

from argparse import ArgumentParser


def set_use_jupyter_args(parser: ArgumentParser):
    parser.add_argument('--jupyter', action='store_true')

    return parser

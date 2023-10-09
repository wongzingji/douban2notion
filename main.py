from argparse import ArgumentParser
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from lib.douban2notion import Douban2Notion
from lib.window import UIWidget


def parse_args():
    parser = ArgumentParser()

    requiredNamed = parser.add_argument_group("required arguments")

    requiredNamed.add_argument(
        '--token',
        required=True,
        help='The integration token of Notion'
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    d2n = Douban2Notion(args.token)

    app = QApplication(sys.argv)
    window = UIWidget(d2n)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
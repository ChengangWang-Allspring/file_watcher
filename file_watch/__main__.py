import sys
from typing import List

from file_watch import app


def main(argv: List[str]) -> int:
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

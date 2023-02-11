"""
A utility to clean up aged files from a directory meeting criteria
useage:
    python file_clean.py  --pat <patterns> --age <age-in-days> --path <absolution-path>
"""
import argparse
import os
import os.path
import sys
import fnmatch
from os import DirEntry
from datetime import datetime, timedelta

MAX_ERROR: int = 10
error_count: int = 0
remove_count: int = 0


def parse_args() -> argparse.Namespace:
    """argument parser"""

    parser = argparse.ArgumentParser(
        description='clean up files from a directory older than age (in days) with specific pattern(s)'
    )
    parser.add_argument(
        '--pat',
        dest='patterns',
        default='*',
        help='file-patterns such as "*.txt|*.log" (seperated by | ). Default pattern is * ',
    )
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--age', dest='age', type=int, help='age-in-days', required=True)
    requiredNamed.add_argument('--path', dest='path', help='absolute-path', required=True)
    return parser.parse_args()


def get_mode_date(entry: DirEntry):
    """get modified date from DirEntry"""
    return datetime.fromtimestamp(entry.stat(follow_symlinks=False).st_mtime)


def match_pattern(patterns: list, entry: DirEntry) -> bool:
    """check if file_name matches pattern"""

    for pat in patterns:
        if fnmatch.fnmatch(entry.name, pat):
            return True
    else:
        return False


def match_age(age: int, entry: DirEntry) -> bool:
    """check if file_age matches age criteria"""

    mod_date = get_mode_date(entry)
    delta: timedelta = datetime.now() - mod_date
    if delta.days >= age:
        return True
    else:
        return False


def may_clean_file(entry: DirEntry, patterns: list, age: int):
    """clean up a file only if criteria are all matched"""

    if not match_pattern(patterns, entry):
        return
    if not match_age(age, entry):
        return

    mod_date = get_mode_date(entry)
    print(f'deleting "{entry.name}": last modified on {mod_date}')
    try:
        os.remove(entry.path)
        global remove_count
        remove_count += 1
    except Exception as ex:
        print(ex, file=sys.stderr)
        global error_count
        error_count += 1
        if error_count > MAX_ERROR:
            print('Too many errors. Reached max allowed errors', file=sys.stderr)
            raise ex  # raise error if maximun allowed error reached


def main():
    """main entry of file_clean"""

    # parse arguments
    args: argparse.Namespace = parse_args()

    print('File clean utility starting ... ')
    print(f'file-patterns: {args.patterns}')
    print(f'age-in-days: {args.age}')
    print(f'abosolute-path: {args.path}')

    # validate arguments
    if not os.path.isdir(args.path):
        print(f'Not a valid path: {args.path}', file=sys.stderr)
        sys.exit(1)

    if args.age < 0:
        print(f'Error: age-in-days must be greater than or equal to 0: {args.age}', file=sys.stderr)
        sys.exit(1)

    if args.age == 0:
        print('Warning: age-in-days = 0, program will skip checking last modified date ')

    if args.patterns is None or args.patterns == '':
        print('Warning: file-patterns is empty. It is set to default * ')

    # convert file patterns into list and trim white spaces
    pats: list = [pat.strip() for pat in args.patterns.split('|')]

    # scan the directory
    try:
        obj = os.scandir(args.path)
        for entry in obj:  # iterate each DirEntry
            if entry.is_file():
                may_clean_file(entry, pats, args.age)

        print(f'File clean up completed with {remove_count} removals and {error_count} errors')
        sys.exit(0)

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()

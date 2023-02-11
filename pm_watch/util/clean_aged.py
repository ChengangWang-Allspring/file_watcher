""" 
A utility to clean aged file
useage:
    python clean_aged_files.py  --file <file_pattern> --days <days> --path <absolute path>

"""
import argparse
import os
import os.path
import sys
import fnmatch
from datetime import datetime
from datetime import timedelta

MAX_ERROR: int = 10

parser = argparse.ArgumentParser(
    description='clean up files from a directory (not including sub-folders) older than certain age (in days) with specific file patterns'
)
parser.add_argument(
    '-f',
    '--file',
    dest='patterns',
    help='file pattern such as "*.txt|*.log" (seperated by | ). Default pattern is *.* ',
    required=True,
)
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-d', '--days', dest='age', type=int, help='age in days', required=True)
requiredNamed.add_argument('-p', '--path', dest='path', help='absolute path', required=True)
args = parser.parse_args()


print('File clean up utility starting ... ')
print(f'file_patterns: {args.patterns}')
print(f'age in days: {args.age}')
print(f'abosolute path: {args.path}')

# validate arguments
if not os.path.isdir(args.path):
    print(f'Not a valid path: {args.path}', file=sys.stderr)
    sys.exit(1)

if args.age < 0:
    print(f'Age in days must be greater than or equal to 0: {args.age}', file=sys.stderr)
    sys.exit(1)

if args.age == 0:
    print('(warning) arg = 0: program will skip checking last modified date ')

if args.patterns is None or args.patterns == '':
    print('(warning) file_patterns is empty. It will be set to default *.* ')

# convert file patterns into list and trim white spaces
pats: list = args.patterns.split('|')
pats: list = [pat.strip() for pat in pats]

# scan the directory
error_count = 0
remove_count = 0
try:
    obj = os.scandir(args.path)
    for entry in obj:  # iterate each DirEntry
        if entry.is_file():
            for pat in pats:  # iterate each pattern
                if fnmatch.fnmatch(entry.name, pat):
                    # get last modified date from file's timestamp
                    last_modified = datetime.fromtimestamp(
                        entry.stat(follow_symlinks=False).st_mtime
                    )
                    # get time delta
                    delta: timedelta = datetime.now() - last_modified
                    if delta.days >= args.age:  # check time delta
                        print(f'deleting "{entry.name}": last modified on {last_modified}')
                        try:
                            os.remove(entry.path)
                            remove_count += 1
                            break
                        except Exception as ex:
                            print(ex)
                            error_count += 1
                            # only error out the whole program if max-error is reached
                            if error_count > MAX_ERROR:
                                print(
                                    'Too many errors. Reached max allowed errors', file=sys.stderr
                                )
                                raise ex

    print(f'File clean up completed with {remove_count} removals and {error_count} errors')
    sys.exit(0)

except Exception as e:
    print(e)
    sys.exit(1)

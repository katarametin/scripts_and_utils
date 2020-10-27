#!/usr/bin/env python3

"""
A script that finds duplicate files in a folder
"""

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from os import walk
from os.path import abspath, exists, join


def main(folder, name):
    # Convert relative paths to absolute paths
    folder_path = abspath(folder)

    # Check if source path exists
    if not exists(folder_path):
        print("Foulder path doesn't exist")
        return 1

    files_found = {}
    duplicate_files = {}

    for root, _, files in walk(folder_path):
        for file in files:
            if name and name != file:
                continue
            full_path = join(root, file)
            if file in files_found:
                duplicate_files[file] = [
                    *duplicate_files.get(file, [files_found[file]]),
                    full_path,
                ]
                continue
            files_found[file] = full_path

    if not duplicate_files:
        print(
            f"Didn't find any duplicate files {f'for {name} ' if name else ''}in {folder_path}"
        )
        return 0

    for file, paths in duplicate_files.items():
        print(f"Found file {file} in the following paths:")
        for path in paths:
            print(path)
        print("---------------------------------------------")
    return 0


def _cli():
    """
    Handle cli arguments
    """

    parser = ArgumentParser(
        description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
    )
    # Define command line arguments
    parser.add_argument(
        "-f",
        "--folder",
        help="The main folder to search for files",
        type=str,
        default=".",
    )
    parser.add_argument("-n", "--name", help="File name to search for", type=str)
    # Parse command line arguments and turn them into a dict
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**_cli()))

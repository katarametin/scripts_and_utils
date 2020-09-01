#!/usr/bin/env python3

"""
A script that traverses through folders and copies files with a specific ending to
the selected destination
"""

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from os import walk
from os.path import abspath, exists, join
from pathlib import Path
from shutil import copy2


def main(source, destination, ending):
    # Convert relative paths to absolute paths
    dest, src = abspath(destination), abspath(source)

    # Check if source path exists
    if not exists(src):
        print("Source path doesn't exist")
        return 1

    # If destination folder already exists, add numbers at the end
    # of the name until we find a folder that doesn't exist
    count = 0
    while True:
        if not exists(dest):
            break

        print("Destination folder already exists, trying to find a new one")
        dest += f"_{str(count)}"
        count += 1

    # Create destination folder
    Path(dest).mkdir(parents=True)

    for root, _, files in walk(src):
        if root == dest:
            continue
        for file in files:
            if file.endswith(ending):
                copy2(
                    join(root, file),
                    join(dest, file),
                )
    print("Done : )")
    print(f"Copied all the files into {dest}")
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
        "-s",
        "--source",
        help="The main folder to search for files",
        type=str,
        default=".",
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="The destination folder to output the files",
        default=join(".", "kat_sims_4_mods"),
        type=str,
    )
    parser.add_argument(
        "-e", "--ending", help="File ending to copy", default=".package", type=str
    )
    # Parse command line arguments and turn them into a dict
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**_cli()))

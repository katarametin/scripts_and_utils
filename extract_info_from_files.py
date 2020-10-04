#!/usr/bin/env python3

"""
A script that traverses through folders, opens files with a specific ending
and writes their content to the destination file
"""

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, FileType
from os import walk
from os.path import abspath, exists, join


def main(source, destination, ending):
    # Convert relative paths to absolute paths
    source = abspath(source)

    # Check if source path exists
    if not exists(source):
        print("Source path doesn't exist")
        return 1

    for root, _, file_names in walk(source):
        content = ""
        for file_name in file_names:
            full_path = join(root, file_name)
            # Skip opening the destination file or if the file doesn't end with the ending
            if full_path == destination or not file_name.endswith(ending):
                continue
            # Read the content of the file and save it's content
            with open(full_path, "r") as file:
                content += file.read().strip()
            # Add newline at the end if it doesn't exist
            if not content.endswith("\n"):
                content += "\n"

        # Write the content of all the files to the destination
        destination.write(content)

    print("Done :)")
    return 0


def _cli():
    """
    Handle cli arguments
    """
    # Init argument parser
    parser = ArgumentParser(
        description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
    )
    # Define command line arguments
    parser.add_argument(
        "-s",
        "--source",
        help="Folder to search in",
        type=str,
        default="./",
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="The destination file to output the collected info",
        default=join(".", "output.txt"),
        type=FileType("w+", encoding="UTF-8"),
    )
    parser.add_argument(
        "-e", "--ending", help="File ending to open", default=".txt", type=str
    )
    # Parse command line arguments and turn them into a dict
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**_cli()))

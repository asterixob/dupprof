import os
import hashlib
from collections import defaultdict
import argparse


def calculate_file_hash(file_path, block_size=65536):
    """Calculate the hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def find_duplicate_files(directory):
    """Find files with identical content in the given root directory."""
    file_hash_map = defaultdict(list)
    file_size_map = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file_name in files:
            # This takes care of OS file errors like broken links, it's too broad and needs improving, OSError etc
            try:
                file_path = os.path.join(root, file_name)
                file_size = os.path.getsize(file_path)
                # add to dictionary
                file_size_map[file_size].append(file_path)
            except Exception:
                pass

    # Filter out files with unique sizes, if size is uniq, content is uniq too i guess.
    duplicate_candidate_paths = [file_paths for file_paths in file_size_map.values() if len(file_paths) > 1]

    # Calculate hashes for duplicate candidates
    for file_paths in duplicate_candidate_paths:
        for file_path in file_paths:
            try:    # This takes care of trying to hash a socket and others
                file_hash = calculate_file_hash(file_path)
                file_hash_map[file_hash].append(file_path)
            except Exception:
                pass

    # Filter out files with unique content hashes
    duplicate_files = [file_paths for file_paths in file_hash_map.values() if len(file_paths) > 1]

    return duplicate_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find duplicate files with identical content given a root directory.")
    parser.add_argument("directory", help="The directory to scan for duplicate files.")
    args = parser.parse_args()

    directory_to_scan = args.directory
    duplicate_files = find_duplicate_files(directory_to_scan)

    if not duplicate_files:
        print("No duplicate files found.")
    else:
        print("Duplicate files found:")
        for files in duplicate_files:
            print("Files with identical content:")
            for file_path in files:
                print(file_path)
            print("=" * 40)


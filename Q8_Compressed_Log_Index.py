"""Q8: Build/search a normalized inverted index and archive logs plus pickle index."""
import os
import re
import sys
import pickle
import zipfile
from collections import defaultdict

TOKEN = re.compile(r"\b[\w-]+\b", re.UNICODE)

def build_index(folder, archive_name):
    index = defaultdict(list); total_lines = total_files = 0
    index_path = os.path.abspath("log_index.pkl")
    with zipfile.ZipFile(archive_name, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for root, _, filenames in os.walk(folder):
            for filename in sorted(filenames):
                path = os.path.join(root, filename)
                if os.path.abspath(path) == os.path.abspath(archive_name) or path == index_path:
                    continue
                try:
                    with open(path, encoding="utf-8", errors="replace") as handle:
                        relative = os.path.relpath(path, folder)
                        total_files += 1
                        archive.write(path, arcname=os.path.join("logs", relative))
                        for line_number, line in enumerate(handle, 1):
                            total_lines += 1
                            for token in set(t.casefold() for t in TOKEN.findall(line)):
                                index[token].append((relative, line_number))
                except OSError as exc:
                    print(f"Skipping {path}: {exc}", file=sys.stderr)
        with open(index_path, "wb") as handle:
            pickle.dump(dict(index), handle, protocol=pickle.HIGHEST_PROTOCOL)
        archive.write(index_path, arcname="log_index.pkl")
    print(f"FILES {total_files}")
    print(f"LINES {total_lines}")
    print(f"TOKENS {len(index)}")

def search_index(pickle_path, queries):
    with open(pickle_path, "rb") as handle:
        index = pickle.load(handle)
    for query in queries:
        matches = index.get(query.casefold(), [])
        print(f"{query}:")
        for filename, line in matches:
            print(f"{filename}:{line}")
        if not matches: print("NOT_FOUND")

def main():
    parts = sys.stdin.read().split()
    try:
        mode = parts[0].upper()
        if mode == "BUILD" and len(parts) == 3:
            build_index(parts[1], parts[2])
        elif mode == "SEARCH" and len(parts) >= 3:
            search_index(parts[1], parts[3:3+int(parts[2])])
        else:
            raise ValueError("Use BUILD folder archive.zip or SEARCH index.pkl q token1 ...")
    except (OSError, ValueError, IndexError, pickle.UnpicklingError) as exc:
        print(f"Error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

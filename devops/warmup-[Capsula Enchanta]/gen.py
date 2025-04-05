import os
import random
import string

# Configuration
ROOT_DIR = "files"
MAX_DEPTH = 4
MAX_SUBFOLDERS = 7
MAX_FILES_PER_FOLDER = 5
FILE_SIZE_RANGE = (50, 300)  # bytes

def random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def create_random_file(path):
    file_name = random_name() + ".txt"
    file_path = os.path.join(path, file_name)
    content = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(*FILE_SIZE_RANGE)))
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"  └─ Created file: {file_path}")

def create_random_structure(base_path, depth=0):
    if depth > MAX_DEPTH:
        return

    indent = "  " * depth
    print(f"{indent}Entering folder: {base_path}")

    # Create files
    num_files = random.randint(1, MAX_FILES_PER_FOLDER)
    for _ in range(num_files):
        create_random_file(base_path)

    # Create subfolders
    num_subfolders = random.randint(0, MAX_SUBFOLDERS)
    for _ in range(num_subfolders):
        folder_name = random_name()
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"{indent}├─ Created folder: {folder_path}")
        create_random_structure(folder_path, depth + 1)

if __name__ == "__main__":
    os.makedirs(ROOT_DIR, exist_ok=True)
    print(f"Starting random file/folder generation in '{ROOT_DIR}' (max depth {MAX_DEPTH})\n")
    create_random_structure(ROOT_DIR)
    print("\nDone.")

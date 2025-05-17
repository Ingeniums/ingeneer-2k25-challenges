import os
import random
import string
import sys
import datetime
import base64

def generate_random_string(length_range=(5, 10)):
    """Generates a random string of letters and digits with random length within the range."""
    characters = string.ascii_letters + string.digits
    length = random.randint(*length_range)
    return ''.join(random.choice(characters) for _ in range(length))

def generate_filler_log(num_lines=random.randint(10, 30)):
    """Generates realistic-looking filler log content."""
    log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
    messages = [
        "Processing request for user {}",
        "Database connection established.",
        "File {} not found.",
        "Operation completed successfully.",
        "Starting background task.",
        "Received data: {}",
        "Configuration loaded from {}",
        "Attempting to connect to external service.",
        "Service responded with status {}",
        "Handling exception: {}"
    ]
    content = []
    start_time = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 60))

    for i in range(num_lines):
        timestamp = start_time + datetime.timedelta(seconds=i*random.uniform(0.1, 2.0))
        level = random.choice(log_levels)
        message_template = random.choice(messages)
        # Fill in placeholders with random data
        filler_data = generate_random_string((3, 8)) if "{}" in message_template else ""
        message = message_template.format(filler_data) if filler_data else message_template
        content.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - {level} - {message}")

    return "\n".join(content)

def generate_filler_encrypted(min_length=100, max_length=500):
    """Generates realistic-looking filler base64-encoded data."""
    # Generate random bytes and encode them in Base64
    byte_length = random.randint(min_length, max_length)
    random_bytes = os.urandom(byte_length)
    return base64.b64encode(random_bytes).decode('utf-8')

def recursive_generate_tree(current_path, current_depth, target_min_depth, target_max_depth, all_leaf_paths):
    """
    Recursively generates a full random folder tree.
    Copies files with filler data to leaf nodes within the target depth range.
    """
    # Base Case 1: Exceeded max depth, stop recursion
    if current_depth > target_max_depth:
        return

    # Base Case 2: Within target depth range, this is a leaf node for file placement
    if target_min_depth <= current_depth <= target_max_depth:
        # Create the files with filler data
        output_encrypted_path = os.path.join(current_path, 'output.encrypted')
        script_log_path = os.path.join(current_path, 'script.log')

        try:
            with open(output_encrypted_path, 'w') as f:
                f.write(generate_filler_encrypted())
            # print(f"Created filler output.encrypted at {output_encrypted_path}") # Optional logging

            with open(script_log_path, 'w') as f:
                f.write(generate_filler_log())
            # print(f"Created filler script.log at {script_log_path}") # Optional logging

            all_leaf_paths.append(os.path.abspath(current_path)) # Add this leaf path to the list

        except IOError as e:
            print(f"Error creating filler files in {current_path}: {e}")

        # Even if it's a leaf for file placement, continue generating children
        # if current_depth is less than max_depth to build a full tree.
        if current_depth == target_max_depth:
             return # Stop recursion if max depth is reached

    # Recursive Step: Create children and continue recursion
    num_children = random.randint(2, 4)
    for _ in range(num_children):
        child_name = generate_random_string()
        child_path = os.path.join(current_path, child_name)
        os.makedirs(child_path, exist_ok=True)
        recursive_generate_tree(child_path, current_depth + 1, target_min_depth, target_max_depth, all_leaf_paths)


def generate_full_folder_tree_with_filler_files(start_path, min_depth, max_depth):
    """
    Generates a full random folder tree starting at start_path with 2-4 children per node.
    Copies files with filler data to ALL leaf nodes at depths between min_depth and max_depth.
    Returns a list of absolute paths of all leaf nodes where the files were placed.
    """
    # Ensure the start path exists
    os.makedirs(start_path, exist_ok=True)

    all_leaf_paths = []
    # Start the recursive generation from depth 1
    recursive_generate_tree(start_path, 1, min_depth, max_depth, all_leaf_paths)

    return all_leaf_paths


if __name__ == "__main__":
    # The script expects one argument:
    # 1. The starting directory where the random structure will be created.
    if len(sys.argv) != 2:
        print("Usage: python generate_folders.py <start_directory>")
        sys.exit(1)

    start_directory = sys.argv[1]

    # Define depth range for the leaf containing the files
    min_depth = 5
    max_depth = 7

    # Generate the structure and get all leaf paths
    all_leaf_paths = generate_full_folder_tree_with_filler_files(start_directory, min_depth, max_depth)

    if all_leaf_paths:
        print(random.choice(all_leaf_paths))
    else:
        print("\nFailed to generate folder structure or place files.")


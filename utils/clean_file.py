# utils/clean_file.py

def contains_null_byte(file_path):
    """Check if a file contains any null bytes."""
    with open(file_path, 'rb') as f:
        return b'\x00' in f.read()


def remove_null_bytes(input_path, output_path=None):
    """
    Remove null bytes from a file.
    If output_path is not provided, overwrite the input file.
    """
    output_path = output_path or input_path

    with open(input_path, 'rb') as f_in:
        content = f_in.read()

    cleaned = content.replace(b'\x00', b'')

    with open(output_path, 'wb') as f_out:
        f_out.write(cleaned)

    return len(content) - len(cleaned)


def clean_file_if_needed(file_path):
    """Check and clean a file if it contains null bytes."""
    if contains_null_byte(file_path):
        print(f"⚠️ Null byte(s) found in '{file_path}' — cleaning file...")
        removed = remove_null_bytes(file_path)
        print(f"✅ Removed {removed} null byte(s). File cleaned.")
    else:
        print(f"✅ '{file_path}' is clean. No null bytes found.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python clean_file.py <file_path>")
        sys.exit(1)

    file_to_check = sys.argv[1]
    clean_file_if_needed(file_to_check)
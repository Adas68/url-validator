import os

def contains_null_byte(file_path):
    with open(file_path, 'rb') as f:
        return b'\x00' in f.read()

def scan_folder(folder_path):
    null_byte_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if contains_null_byte(file_path):
                    null_byte_files.append(file_path)
    return null_byte_files

if __name__ == '__main__':
    folders = ['utils', 'tests']

    print("🔍 Scanning for null bytes in .py files...\n")
    for folder in folders:
        print(f"📂 Scanning folder: {folder}/")
        files_with_null = scan_folder(folder)
        if files_with_null:
            print("❌ Found null bytes in the following files:")
            for file in files_with_null:
                print(f"   - {file}")
        else:
            print("✅ No null bytes found.")
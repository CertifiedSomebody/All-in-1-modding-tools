import os
import shutil
import time
import sys

# Ensure UTF-8 encoding to avoid Unicode errors
sys.stdout.reconfigure(encoding='utf-8')

def delete_folder(folderpath):
    """Safely deletes a folder, retrying if access is denied."""
    if os.path.exists(folderpath) and os.path.isdir(folderpath):
        for _ in range(5):  # Retry up to 5 times
            try:
                # Remove read-only restrictions (fix for Windows)
                for root, dirs, files in os.walk(folderpath):
                    for file in files:
                        filepath = os.path.join(root, file)
                        os.chmod(filepath, 0o777)  # Grant full permissions

                shutil.rmtree(folderpath)
                print(f"✅ Successfully deleted: {folderpath}")
                return
            except PermissionError:
                print(f"⚠️ Permission denied for {folderpath}, retrying in 2 seconds...")
                time.sleep(2)  # Wait before retrying
        print(f"❌ Failed to delete {folderpath}. Close any program using it.")
    else:
        print(f"❌ Folder not found: {folderpath}")

def delete_file(filepath):
    """Safely deletes a file if it exists."""
    if os.path.exists(filepath):
        try:
            os.chmod(filepath, 0o777)  # Grant full permissions
            os.remove(filepath)
            print(f"✅ Deleted file: {filepath}")
        except PermissionError:
            print(f"⚠️ Permission denied: {filepath}. Close any program using it.")
    else:
        print(f"❌ File not found: {filepath}")

def cleanup():
    """Deletes extracted APK files, APK, and dump files."""
    print("🧹 Cleaning Dump Folder...")
    delete_folder("dumps")  # Dumps folder where `.so` files are stored

    print("🧹 Cleaning Decompiled APKs...")
    delete_folder("decompiled_apks")  # Decompiled files

    print("🧹 Cleaning Merged APK files...")
    delete_folder("extracted_apk")  # Extracted APKs

    print("🧹 Cleaning Game APK file...")
    delete_file("game.apk")  # Game APK file

    print("✅ Cleanup Process Completed!")

# Run the cleanup process
if __name__ == "__main__":
    cleanup()

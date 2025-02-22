import os
import shutil

def delete_folder(folderpath):
    """Deletes a folder and its contents if it exists."""
    if os.path.exists(folderpath) and os.path.isdir(folderpath):
        shutil.rmtree(folderpath)
        print(f"🗑️ Deleted folder: {folderpath}")
    else:
        print(f"⚠️ Folder not found: {folderpath}")

def delete_file(filepath):
    """Deletes a file if it exists."""
    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.remove(filepath)
        print(f"🗑️ Deleted: {filepath}")
    else:
        print(f"⚠️ File not found: {filepath}")

def cleanup():
    """Deletes extracted APK files, merged APK, temp folders, dump files, and AndroidManifest.xml."""
    delete_folder("extracted_apk")  
    delete_folder("temp_extracted")  # Delete temp folder after merging
    delete_folder("dumps")  
    delete_file("merged.apk")  # Cleanup merged APK
    delete_file("game.apk")  
    delete_file("AndroidManifest.xml")  

    print("\n✅ Cleanup completed! Ready for a new APK.")

if __name__ == "__main__":
    cleanup()

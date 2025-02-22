import os
import sys
import shutil
import zipfile
import subprocess

def extract_xapk(xapk_path, extract_to):
    """Extracts XAPK or Split APKs to a directory."""
    if not os.path.exists(xapk_path):
        print(f"Error: XAPK file '{xapk_path}' not found!")
        sys.exit(1)

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    with zipfile.ZipFile(xapk_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    print(f"Extracted {xapk_path} to {extract_to}")

def extract_apks(apk_folder, extracted_apk_folder):
    """Extracts all APK files from the extracted XAPK directory."""
    if not os.path.exists(extracted_apk_folder):
        os.makedirs(extracted_apk_folder)

    apk_files = [f for f in os.listdir(apk_folder) if f.endswith('.apk')]

    if not apk_files:
        print("Error: No APK files found in the extracted folder!")
        sys.exit(1)

    for apk in apk_files:
        apk_path = os.path.join(apk_folder, apk)
        with zipfile.ZipFile(apk_path, 'r') as apk_zip:
            apk_zip.extractall(extracted_apk_folder)

    print(f"Extracted all APKs to {extracted_apk_folder}")

def merge_apks(extracted_apk_folder, output_apk):
    """Repackages extracted APK contents into a new APK."""
    with zipfile.ZipFile(output_apk, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
        for root, _, files in os.walk(extracted_apk_folder):
            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, extracted_apk_folder)
                apk_zip.write(file_path, archive_path)

    print(f"Merged extracted APK contents into {output_apk}")

def sign_apk(apk_path, keystore_path, key_alias, key_password):
    """Signs the APK using jarsigner."""
    if not os.path.exists(apk_path):
        print("Error: APK to be signed does not exist!")
        sys.exit(1)

    # Check if Java is installed
    try:
        subprocess.run(['java', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        print("Error: Java is not installed. Install Java before running this script.")
        sys.exit(1)

    # Check if keystore exists, create if missing
    if not os.path.exists(keystore_path):
        print("Keystore not found. Creating one...")
        subprocess.run([
            'keytool', '-genkeypair', '-v', '-keystore', keystore_path,
            '-alias', key_alias, '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
            '-storepass', key_password, '-keypass', key_password,
            '-dname', 'CN=Unknown, OU=Unknown, O=Unknown, L=Unknown, S=Unknown, C=Unknown'
        ], check=True)
        print(f"Keystore created at {keystore_path}")

    # Sign APK
    subprocess.run([
        'jarsigner', '-verbose', '-sigalg', 'SHA256withRSA', '-digestalg', 'SHA-256',
        '-keystore', keystore_path, '-storepass', key_password,
        apk_path, key_alias
    ], check=True)
    
    print(f"Signed APK: {apk_path}")

def cleanup_temp(folder, exclude_files=[]):
    """Deletes the temporary extracted folder but excludes specified files."""
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in exclude_files:
                    os.remove(file_path)

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)

        try:
            os.rmdir(folder)  # Remove the main folder if empty
        except OSError:
            pass  # Ignore error if the folder is not empty

        print(f"Deleted temporary folder: {folder} (excluding {exclude_files})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merge_and_sign.py <path_to_xapk>")
        sys.exit(1)

    xapk_path = sys.argv[1]
    extract_to = "temp_extracted"
    extracted_apk_folder = "temp_apk_extracted"
    output_apk = "merged.apk"
    keystore_path = "my_keystore.jks"
    key_alias = "mykey"
    key_password = "password123"

    extract_xapk(xapk_path, extract_to)
    extract_apks(extract_to, extracted_apk_folder)
    merge_apks(extracted_apk_folder, output_apk)
    sign_apk(output_apk, keystore_path, key_alias, key_password)

    # Cleanup but **keep** the keystore file
    cleanup_temp(extract_to)
    cleanup_temp(extracted_apk_folder)

    print("\n✅ APK merging and signing completed successfully!")

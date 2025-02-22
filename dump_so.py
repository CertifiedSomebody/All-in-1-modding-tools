import os
import subprocess

# Paths
IL2CPP_DUMPER_PATH = "Il2CppDumper-win-v6.7.40/Il2CppDumper.exe"  # Update path if needed
LIBIL2CPP_PATH = "extracted_apk/lib/arm64-v8a/libil2cpp.so"  # Update with actual path
METADATA_PATH = "extracted_apk/assets/bin/Data/Managed/Metadata/global-metadata.dat"
OUTPUT_FOLDER = "dumps"

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def dump_il2cpp():
    command = [
        IL2CPP_DUMPER_PATH,
        LIBIL2CPP_PATH,
        METADATA_PATH,
        OUTPUT_FOLDER
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Dumping completed! Check the {OUTPUT_FOLDER} folder.")
    except subprocess.CalledProcessError as e:
        print(f"Error during dumping: {e}")

if __name__ == "__main__":
    dump_il2cpp()


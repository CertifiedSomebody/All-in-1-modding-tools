from pyaxmlparser import APK
from lxml.etree import tostring

def decode_manifest(apk_path, output_file="AndroidManifest.xml"):
    apk = APK(apk_path)
    manifest_xml = apk.get_android_manifest_xml()
    
    # Convert XML to string
    manifest_str = tostring(manifest_xml, pretty_print=True, encoding="utf-8").decode("utf-8")

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(manifest_str)

    print(f"Manifest saved to {output_file}")

# Example usage
apk_file = "game.apk"  # Ensure the APK file is present in the directory
decode_manifest(apk_file)

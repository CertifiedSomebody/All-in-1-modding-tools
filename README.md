
# All-in-1 Modding Tools

**All-in-1 Modding Tools** is a versatile suite designed for modding Android games using Python. It includes a range of features for APK patching, Unity `.so` file dumping, and easy-to-use GUI tools. This repository provides developers and modders with a powerful toolkit to decompile, modify, and repackage Android APKs and Unity-based games.

---

## 🚀 **Features**

- **APK Decompiling**: Decompile APK files using `JADX` (Java) or `Apktool` (Full resources & Smali).
- **Unity Game Modding**: Dump `.so` files from Unity-based games using **Il2CppDumper**.
- **APK Patching**: Modify APKs and repack them.
- **Virtual Environment Setup**: Automatically handle Python dependencies with `venv`.
- **Comprehensive File Management**: Easily manage and clean up merged APKs and decompiled files.

---

## 🛠 **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CertifiedSomebody/All-in-1-modding-tools.git
   cd All-in-1-modding-tools
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # For Linux/MacOS
   .venv\Scripts\activate      # For Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 **Usage**

### Decompile APK

- **JADX (Java Decompilation)**:
  Decompile Java source code from APK files.

- **Apktool (Full Resource & Smali Decompilation)**:
  Use Apktool to decompile APKs and get all resources along with smali code.

### Dump `.so` Files from Unity Games

- Automatically dump `.so` files using **Il2CppDumper** to get Unity-specific libraries, enabling you to analyze and modify Unity-based games.

### Clean Up Merged APKs

- Clean up merged APK files post-installation with the `merged_apk_cleanup.py` script.

---

## 🔐 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💡 **Contributing**

Feel free to contribute by opening an issue or creating a pull request! Here are some ways you can contribute:

- Report bugs or suggest new features.
- Improve documentation.
- Help with code improvements and optimizations.

---

## 📝 **Disclaimer**

This project is intended for educational and research purposes only. Use at your own risk, and ensure that you comply with all relevant legal regulations in your region regarding modding and reverse-engineering software.

---

## 📧 **Contact**

For any inquiries, please contact [CertifiedSomebody](mailto:sanjjha093@gmail.com).

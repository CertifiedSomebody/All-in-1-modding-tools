import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, 
    QMessageBox, QTextEdit, QLabel
)
from PyQt5.QtCore import QThread, pyqtSignal

class ProcessWorker(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        for line in process.stdout:
            self.output.emit(line.strip())
        process.wait()
        self.finished.emit()

class ModMakerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("🔧 Mod Maker - APK Tool")
        layout.addWidget(self.label)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.merge_button = QPushButton("Merge & Sign XAPK")
        self.merge_button.clicked.connect(self.merge_and_sign)
        layout.addWidget(self.merge_button)

        self.clean_merged_button = QPushButton("Clean Merged APK")
        self.clean_merged_button.clicked.connect(self.clean_merged_apk)
        layout.addWidget(self.clean_merged_button)

        self.decompile_button = QPushButton("Decompile APK")
        self.decompile_button.clicked.connect(self.decompile_apk)
        layout.addWidget(self.decompile_button)

        self.dump_so_button = QPushButton("Dump .so Files")
        self.dump_so_button.clicked.connect(self.dump_so_files)
        layout.addWidget(self.dump_so_button)

        self.clean_decompiled_button = QPushButton("Clean Decompiled APKs")
        self.clean_decompiled_button.clicked.connect(self.clean_decompiled_apks)
        layout.addWidget(self.clean_decompiled_button)

        self.clean_dump_button = QPushButton("Clean Dump Folder")
        self.clean_dump_button.clicked.connect(self.clean_dump_folder)
        layout.addWidget(self.clean_dump_button)

        self.setLayout(layout)
        self.setWindowTitle("Mod Maker")
        self.setGeometry(100, 100, 400, 400)

    def log(self, message):
        self.log_output.append(message)
        print(message)

    def run_command(self, cmd):
        self.worker = ProcessWorker(cmd)
        self.worker.output.connect(self.log)
        self.worker.finished.connect(self.on_task_finished)
        self.worker.start()

        # Disable buttons while the task is running
        self.merge_button.setEnabled(False)
        self.clean_merged_button.setEnabled(False)
        self.decompile_button.setEnabled(False)
        self.dump_so_button.setEnabled(False)
        self.clean_decompiled_button.setEnabled(False)
        self.clean_dump_button.setEnabled(False)

    def on_task_finished(self):
        # Re-enable buttons after task completion
        self.merge_button.setEnabled(True)
        self.clean_merged_button.setEnabled(True)
        self.decompile_button.setEnabled(True)
        self.dump_so_button.setEnabled(True)
        self.clean_decompiled_button.setEnabled(True)
        self.clean_dump_button.setEnabled(True)

        self.log("✅ Process Completed!\n")

    def select_file(self, file_filter):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter, options=options)
        return file_path

    def merge_and_sign(self):
        xapk_path = self.select_file("XAPK Files (*.xapk)")
        if not xapk_path or not os.path.exists(xapk_path):
            self.log("❌ XAPK file not found or invalid.")
            return
        xapk_name = os.path.basename(xapk_path).replace(".xapk", "")
        merged_apk = f"{xapk_name} merged.apk"
        self.log(f"🔄 Merging & Signing XAPK: {xapk_path}")
        self.run_command(f'python "merge_and_sign.py" "{xapk_path}" "{merged_apk}"')

    def clean_merged_apk(self):
        merged_apk = self.select_file("APK Files (*.apk)")
        if merged_apk and os.path.exists(merged_apk):
            self.log(f"🧹 Cleaning Merged APK: {merged_apk}")
            self.run_command(f'python "cleanup.py" "{merged_apk}"')
        else:
            self.log("❌ Merged APK file not found.")

    def decompile_apk(self):
        apk_path = self.select_file("APK Files (*.apk)")
        if not apk_path:
            return
        response = QMessageBox.question(
            self, "Choose Decompilation Method",
            "Use JADX for Java decompilation? (No for Apktool)",
            QMessageBox.Yes | QMessageBox.No
        )
        xapk_name = os.path.basename(apk_path).replace(".apk", "")
        output_dir = os.path.join("decompiled_apks", xapk_name)
        if response == QMessageBox.Yes:
            cmd = f'jadx -d "{output_dir}" "{apk_path}"'
            decompiler = "JADX"
        else:
            apktool_path = "C:/apktool/apktool.jar"
            cmd = f'java -jar "{apktool_path}" d -o "{output_dir}" "{apk_path}"'
            decompiler = "Apktool"
        self.log(f"🔄 Starting {decompiler} Decompilation...")
        self.run_command(cmd)
        self.worker.finished.connect(lambda: self.log(f"\n🎉 {decompiler} Decompilation Complete!\nFiles saved to: {output_dir}"))

    def dump_so_files(self):
        so_file = self.select_file("Shared Object Files (*.so)")
        if not so_file:
            return
        metadata_file = self.select_file("Metadata Files (*global-metadata.dat)")
        if not metadata_file:
            return
        output_dir = "dumps"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.log("🔄 Dumping .so Files...")
        cmd = f'python "dump_so.py" "{so_file}" "{metadata_file}" "{output_dir}"'
        self.run_command(cmd)

    def clean_decompiled_apks(self):
        response = QMessageBox.question(
            self, "Confirm Cleanup",
            "Are you sure you want to clean the Decompiled APKs folder?",
            QMessageBox.Yes | QMessageBox.No
        )
        if response == QMessageBox.Yes:
            self.log("🧹 Cleaning Decompiled APKs...")
            self.run_command('python "cleanup.py" "decompiled_apks"')

    def clean_dump_folder(self):
        response = QMessageBox.question(
            self, "Confirm Cleanup",
            "Are you sure you want to clean the Dump folder?",
            QMessageBox.Yes | QMessageBox.No
        )
        if response == QMessageBox.Yes:
            self.log("🧹 Cleaning Dump Folder...")
            self.run_command('python "cleanup.py" "dumps"')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModMakerGUI()
    window.show()
    sys.exit(app.exec_())

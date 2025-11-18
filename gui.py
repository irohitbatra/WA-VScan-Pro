# gui.py - PyQt5 GUI for WA-VScan Pro
import sys, os, threading, webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QFileDialog, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt
from scanner import scan_target

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WA-VScan Pro v2 - PyQt GUI")
        self.setGeometry(200, 200, 600, 450)

        layout = QVBoxLayout()

        title = QLabel("<h2>WA-VScan Pro v2</h2>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter target URL (only scan authorized systems)")
        layout.addWidget(self.url_input)

        self.start_btn = QPushButton("Start Scan")
        self.start_btn.clicked.connect(self.start_scan)
        layout.addWidget(self.start_btn)

        self.report_btn = QPushButton("Open Latest Report")
        self.report_btn.clicked.connect(self.open_report)
        layout.addWidget(self.report_btn)

        self.export_btn = QPushButton("Export Results Folder")
        self.export_btn.clicked.connect(self.export_results)
        layout.addWidget(self.export_btn)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # infinite animation
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

    def log(self, msg):
        self.log_box.append(msg)

    def start_scan(self):
        target = self.url_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Input Required", "Please enter a target URL.")
            return

        self.start_btn.setEnabled(False)
        self.progress.setVisible(True)

        t = threading.Thread(target=self.scan_worker, args=(target,))
        t.start()

    def scan_worker(self, target):
        try:
            self.log(f"[*] Starting scan: {target}")
            results = scan_target(target)

            self.log("[+] Scan Completed")
            self.log("[+] Report: " + results["html"])
            self.log("[+] JSON: " + results["json"])
            self.log("[+] CSV: " + results["csv"])

            self.progress.setVisible(False)
            self.start_btn.setEnabled(True)

            QMessageBox.information(self, "Scan Finished", "Report has been generated.")

            webbrowser.open("file://" + os.path.abspath(results["html"]))

        except Exception as e:
            self.log("[!] Error: " + str(e))
            self.progress.setVisible(False)
            self.start_btn.setEnabled(True)

    def open_report(self):
        path = os.path.join("results", "report_v2.html")
        if os.path.exists(path):
            webbrowser.open("file://" + os.path.abspath(path))
        else:
            QMessageBox.warning(self, "No Report", "No report found. Run a scan first.")

    def export_results(self):
        folder = QFileDialog.getExistingDirectory(self, "Select destination folder")
        if folder:
            import shutil
            shutil.copytree("results", os.path.join(folder, "WA-VScan-Pro-results"), dirs_exist_ok=True)
            QMessageBox.information(self, "Exported", "Results exported successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

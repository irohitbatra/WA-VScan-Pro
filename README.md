# 🚀 WA-VScan Pro — Advanced Web Application Vulnerability Scanner  
*A Modern, Fast, and Professional Web Scanner with GUI + HTML Reporting*

WA-VScan Pro is a lightweight yet powerful vulnerability scanner designed to perform quick audits of web applications.  
It offers a **PyQt5-based GUI**, **multithreaded scanning**, and a **professional HTML report with charts**, making it perfect for:

 
- Bug bounty beginners  
- Developers testing their own apps  
- Security automation labs  

---

## 📌 Features

### 🔍 Vulnerability Detection
- Server Banner Disclosure  
- Missing Security Headers (CSP, HSTS, XSS Protection, Frame Options,    Content Type Options)  
- Directory Listing Detection  
- Exposed Backup Files  
- Reflection-Based XSS Detection  
- Basic SQL Injection Detection  
- And more checks coming soon…

### 🖥️ GUI (PyQt5)
- Clean, modern interface  
- Progress indication  
- One-click report opening  
- Export results folder  

### 📊 Professional HTML Report
- Dark-themed report  
- Severity summary  
- Doughnut chart visualization  
- Executive summary  
- Detailed table of findings  


### ⚡ Performance
- Multithreaded scanning engine  
- Fast response handling with timeouts  
- URL normalization  

---

## 🏗️ Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python 3 |
| GUI | PyQt5 |
| Report | HTML + Chart.js |
| HTTP Engine | requests |
| Multithreading | threading / concurrent.futures |

---

## 📥 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/WA-VScan-Pro.git
cd WA-VScan-Pro
```

### 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 4️⃣ Ensure Tkinter/PyQt Dependencies Are Installed
(For GUI mode)
```bash
sudo apt install python3-pyqt5
```

---

## 🚀 Usage

### 🖥️ Run GUI Scanner
```bash
python3 gui.py
```

### 🔧 Run CLI Scanner
```bash
python3 scanner.py https://target.com
```

### 📁 Reports & Output
All reports are saved here:

```
results/report_v2.html
results/results.json
results/results.csv
```

---

## 📸 Screenshots

### 🔹 GUI Interface

```
![GUI Screenshot](/home/kali/Downloads/WA-VScan-Pro-Final/Report/Gui.png)
```

### 🔹 Professional HTML Report
```
![Report Screenshot](/home/kali/Downloads/WA-VScan-Pro-Final/Report.png)
```

---

## ⚠️ Legal Disclaimer


This tool is strictly for:

- Educational purposes  
- Testing your **own applications**  
- Use in **authorized environments**

Unauthorized scanning of websites **you do not own** is illegal and punishable under cybercrime laws.

**You are responsible for all actions performed with this tool.**

---

## 🤝 Contributing
Pull requests are welcome!  
Planned upgrades include:

- More vulnerability checks  
- Export to PDF format  
- Plugin-based architecture  
- Login/authentication scanning  

---

## 💙 Credits
Made with ❤️ by **Rohit Batra**

If you like this project, please ⭐ star the repo!

---

## 🛡️ License
MIT License — Free for personal & commercial use.

# ✅ **Contributing to ExifPlus**

Thank you for your interest in contributing to **ExifPlus**, a Python-based EXIF/XMP/IPTC metadata viewer and editor with a modern Tkinter + ttkbootstrap GUI.

All contributions are welcome — including code improvements, bug fixes, documentation, UI enhancements, feature ideas, and optimization.

---

## 🚀 Getting Started

### 1. Fork the Repository
Click **Fork** at the top-right of the GitHub page.

### 2. Clone Your Fork
```bash
git clone https://github.com/<your-username>/ExifPlus.git
cd ExifPlus
````

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Install ExifPlus in Editable Mode (Optional)

```bash
pip install -e .
```

### 5. Run ExifPlus Locally

```bash
python -m exifplus
```

---

## 🛠️ How to Contribute Code

### 1. Create a Branch

```bash
git checkout -b feature/my-change
```

### 2. Make Your Changes

You can contribute to:

* Metadata parsing improvements
* Additional metadata formats
* GUI improvements (layout, theme, icons)
* New features (batch editing, drag-and-drop, file explorer, etc.)
* Performance optimizations
* Code cleanup or refactoring
* Packaging and CI improvements
* Documentation (README, examples, guides)

### 3. Test Your Changes

Run the app and test the GUI:

```bash
python -m exifplus
```

Make sure your changes do not break core functionality.

### 4. Commit and Push

```bash
git commit -m "Add: short description of change"
git push origin feature/my-change
```

### 5. Open a Pull Request

Go to GitHub → Submit a PR → Describe your change clearly.

---

## 🐞 Reporting Bugs

Please open issues with:

* Clear description
* Steps to reproduce
* OS + Python version
* Screenshots (if GUI)
* Error log if applicable

👉 Issues: [https://github.com/ZahidServers/ExifPlus/issues](https://github.com/ZahidServers/ExifPlus/issues)

---

## 💡 Suggesting Features

Open an issue labeled **enhancement**.
Good ideas include:

* Export metadata to CSV/JSON
* Batch EXIF editor
* Image preview panel
* Compare metadata between images

---

## 🧹 Code Style

* Follow Python best practices
* Keep GUI code readable and modular
* Avoid placing long logic in the GUI thread (use `threading`)
* Use descriptive variable names
* Keep functions small and focused

---

## ❤️ Thank You

Every contribution improves ExifPlus and helps the open-source community.
Thank you for your support and ideas!


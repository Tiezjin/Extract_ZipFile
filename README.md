# Tkinter Zip Extractor
Tkinkter GUI with Unzip Utility

A lightweight and fast GUI tool for extracting ZIP archives, built because the Windows built-in extractor is significantly slower than Python's native libraries.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## Why This Exists

Extracting large ZIP files in Windows Explorer can be frustratingly slow. This tool leverages the speed of Python's built-in `zipfile` library to extract archives much faster, all through a simple and user-friendly graphical interface.

**Stop waiting. Extract faster.**

## Features

*   **🚀 Faster Extraction:** Bypass Windows Explorer's slow extraction process.
*   **🧹 Clean GUI:** Simple and intuitive interface built with Tkinter.
*   **📁 Directory Selection:** Easily choose both your ZIP file and output destination.
*   **⚙️ Lightweight:** A single `.exe` file, no installation needed.
*   **🆓 Free & Open Source:** MIT Licensed. Use it, modify it, share it.

## Installation & Download

### Option 1: Download the Executable (For End Users)
1.  Go to the [Releases](../../releases) page.
2.  Download the latest `ZipExtractor.exe` file.
3.  Run the executable. No installation required.

### Option 2: Run from Source (For Developers)
If you have Python installed, you can run the tool directly from the source code.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
2.  **(Optional) Create a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```
3.  **Run the application:**
    ```bash
    python src/main.py
    ```

## How to Use

1.  **Launch** the application.
2.  Click **"Select ZIP File"** to choose the archive you want to extract.
3.  Click **"Select Output Folder"** to choose where to put the extracted files.
4.  Click the big **"Extract!"** button.
5.  Wait for the success message! A timer will show after finishing the extraction.

## For Developers: Building from Source

This project uses `PyInstaller` to package the Python script into a standalone executable.

1.  Install the required library:
    ```bash
    pip install pyinstaller
    ```
2.  Run the build command:
    ```bash
    pyinstaller --onefile --windowed --name "ZipExtractor" src/main.py
    ```
    The executable will be created in the `dist/` folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

*   Built with Python and the amazing `tkinter` and `zipfile` modules.
*   Developed with the assistance of Google Gemini, which provided guidance on code structure, implementation details, and troubleshooting.
*   Icon drawn by Google Gemini
*   Text written by DeepSeek

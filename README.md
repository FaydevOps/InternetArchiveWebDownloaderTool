# ArchiveDirectDownloader

ArchiveDirectDownloader is a modern graphical desktop utility designed to facilitate the rapid, direct download and digital preservation of open-access media collections, text resources, and public domain historical files hosted across web platforms like the [Internet Archive](https://archive.org/).

Built with an intuitive user interface, the tool safely processes public URLs to handle download streams efficiently without relying on command-line operations.

## ✨ Features

- **Modern GUI Dashboard:** Built with a clean, dark-themed responsive layout using `customtkinter`.
- **Direct Extraction Engine:** Utilizes a decoupled implementation of `yt-dlp` running purely via a generic extractor to pull direct resource streams.
- **Multithreaded Operations:** Downloads run in background worker threads, preventing the user interface from freezing during heavy file streaming.
- **Self-Updating Architecture:** Features a silent background manager that updates the underlying download framework directly via `pip` without needing terminal execution.
- **Anti-Crash Safety Net:** Includes strict level-0 `multiprocessing` locks and delayed initialization logic, ensuring high stability when packed into a standalone binary (`.exe`).
- **Dynamic Diagnostics:** Automatically logs setup or library import exceptions into `ERROR_LIBRERIAS.txt` or `CRASH_LOG.txt` for easier troubleshooting.

## 🚀 Prerequisites

Before launching the utility from source code, ensure your environment meets the following conditions:

- **Python:** Version 3.8 or higher.
- **Dependencies:** The application relies on the following libraries:
  - `customtkinter` (Modern UI framework)
  - `yt_dlp` (Stream extraction engine)
  - `Pillow` (Image processing for branding assets)

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ArchiveDownloader.git](https://github.com/YOUR_USERNAME/ArchiveDownloader.git)
   cd ArchiveDownloader

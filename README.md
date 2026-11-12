# ArchiveDirectDownloader

A small desktop app (Python + `customtkinter`) for downloading files by direct link (audio, video, text, PDF…) from open-access collections such as the [Internet Archive](https://archive.org/). Paste the URL, pick a folder and click **INICIAR DESCARGA**. No command line needed.

> The interface is in Spanish.

## ✨ Features

- **Simple dark-mode GUI** built with `customtkinter`.
- **`yt-dlp` engine** in generic mode: it follows redirects (for example `archive.org/download/...` → `iaXXXX.us.archive.org`) and downloads the file directly.
- **Real progress**: a progress bar plus MB downloaded / total in the status line.
- **Downloads in the background**: the window stays responsive while a file downloads.
- **Clean file names**: taken from the URL (decoded, with any `?query` and `#fragment` removed, and with characters Windows rejects replaced). If the URL has no extension, the server's title and extension are used.
- **Engine auto-update**: when run from source, `yt-dlp` updates itself silently on startup (the new version takes effect the next time you open the app). This is turned off in the `.exe`, where it can't work.
- **Diagnostics**: missing libraries are written to `ERROR_LIBRERIAS.txt` and unexpected crashes to `CRASH_LOG.txt`.

## 🚀 Requirements

- Python **3.8+** (with `tkinter`, which ships with the official installer)
- The dependencies in [`requirements.txt`](requirements.txt): `customtkinter`, `yt-dlp`, `Pillow`

## 🛠️ Installation

```bash
git clone https://github.com/FaydevOps/InternetArchiveWebDownloaderTool.git
```

```bash
cd InternetArchiveWebDownloaderTool
```

```bash
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python ArchiverDownloader.py
```

1. Paste the file URL, for example `https://archive.org/download/<identifier>/<file>.mp3`
   (on an item's page on archive.org, look under **DOWNLOAD OPTIONS → SHOW ALL** and copy the file's link).
2. Click **CARPETA** to choose the destination folder (default: `~/Downloads`).
3. Click **INICIAR DESCARGA** and follow the progress in the bar.

Optional: put a `logo.png` next to the script to show it in the window header.

## 📦 Building a `.exe` (Windows)

```bash
pip install pyinstaller
```

```bash
pyinstaller --noconsole --onefile --collect-all customtkinter --add-data "logo.png;." ArchiverDownloader.py
```

Leave out `--add-data` if you don't have a `logo.png`. The executable ends up in `dist/`. In the `.exe` the `yt-dlp` version is fixed at build time: to update it, rebuild.

## ❓ Troubleshooting

| Problem | Fix |
|---|---|
| The app won't open and `ERROR_LIBRERIAS.txt` appears | Run `pip install -r requirements.txt` |
| `HTTP Error 403` / "Cloudflare anti-bot challenge" | The site blocks automated downloads; this isn't an app bug |
| The download fails on an archive.org item | Some files are restricted (lending / account login required) |
| The bar doesn't move but MB keep going up | The server doesn't report the total size; the download continues normally |

## ⚖️ Responsible use

Only download content that is in the public domain, openly licensed, or that you have the right to download. Respect the terms of use of each platform.

## 📄 License

[MIT](LICENSE)

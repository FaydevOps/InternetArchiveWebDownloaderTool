import os
import sys
import multiprocessing

# --- BLOQUEO DE SEGURIDAD NIVEL 0 (ANTES DE CUALQUIER IMPORT) ---
if __name__ == "__main__":
    multiprocessing.freeze_support()
    # Si no es el proceso principal, terminamos ANTES de cargar tkinter
    if multiprocessing.current_process().name != 'MainProcess':
        sys.exit(0)

# --- IMPORTACIONES CARGADAS SOLO EN EL PROCESO PRINCIPAL ---
import threading
import subprocess
import re  
from urllib.parse import unquote

# Importamos tkinter y ctk aquí dentro para evitar el error de carpetas temporales
try:
    from tkinter import messagebox as MessageBox
    from tkinter import filedialog, BOTH, LEFT, X, StringVar, BOTTOM
    import customtkinter as ctk
    from yt_dlp import YoutubeDL
    from PIL import Image
except ImportError as e:
    # Esto ayuda a diagnosticar si faltan librerías en el entorno
    with open("ERROR_LIBRERIAS.txt", "w") as f:
        f.write(str(e))
    sys.exit(1)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Configuración inicial
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ArchiveDirectDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Archive Pro - Gestor de Descarga Directa")
        self.geometry("750x850")
        self.PRIMARY_BLUE = "#4AB8FF"
        self.ACCENT_GREEN = "#4CAF50"
        self.url_var = StringVar()
        self.output_path = StringVar(value=os.path.expanduser("~/Downloads"))
        self.setup_ui()

    def update_engine(self):
        """ Actualización sin necesidad de Python instalado en el sistema """
        def run_update():
            try:
                # Usamos banderas para ocultar totalmente la consola de pip
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    shell=True,
                    creationflags=0x08000000 
                )
                self.after(0, lambda: self.status_label.configure(text="Motor actualizado"))
            except:
                pass
        threading.Thread(target=run_update, daemon=True).start()

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

        # Logo Recuperado
        try:
            ruta_img = resource_path("logo.png")
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(ruta_img),
                dark_image=Image.open(ruta_img),
                size=(300, 200) 
            )
            self.image_label = ctk.CTkLabel(self.main_frame, image=self.logo_image, text="")
            self.image_label.pack(pady=15)
        except:
            self.image_label = ctk.CTkLabel(self.main_frame, text="[ logo.png ]", text_color="gray")
            self.image_label.pack(pady=20)

        ctk.CTkLabel(self.main_frame, text="GESTOR DE DESCARGAS DIRECTAS", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=5)

        self.url_entry = ctk.CTkEntry(self.main_frame, textvariable=self.url_var, width=580, height=40, corner_radius=10)
        self.url_entry.pack(pady=10, padx=20)

        self.folder_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.folder_frame.pack(pady=10, fill=X, padx=60)
        ctk.CTkEntry(self.folder_frame, textvariable=self.output_path, state='readonly', width=420).pack(side=LEFT, padx=(0, 10))
        ctk.CTkButton(self.folder_frame, text="CARPETA", fg_color=self.ACCENT_GREEN, text_color="black",
                      font=ctk.CTkFont(weight="bold"), width=100, command=self.browse_directory).pack(side=LEFT)

        self.download_btn = ctk.CTkButton(self.main_frame, text="INICIAR DESCARGA", command=self.start_download, 
                                          fg_color=self.PRIMARY_BLUE, height=50, width=300, font=ctk.CTkFont(size=16, weight="bold"))
        self.download_btn.pack(pady=25)

        self.status_label = ctk.CTkLabel(self.main_frame, text="Esperando...", font=('Segoe UI', 11, 'italic'))
        self.status_label.pack()
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=580, height=15)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Donaciones Recuperadas
        self.don_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e", corner_radius=10)
        self.don_frame.pack(side=BOTTOM, fill=X, padx=30, pady=20)
        ctk.CTkLabel(self.don_frame, text="¿Te ha servido el programa?", font=("Segoe UI", 11)).pack(pady=(5,0))
        ctk.CTkButton(self.don_frame, text="☕ Invítame a un Café (Donar)", fg_color="#f39c12", text_color="black",
                      font=ctk.CTkFont(weight="bold"),
                      command=lambda: subprocess.run(["explorer", "https://paypal.me/FaycraxE"])).pack(pady=10)

    def browse_directory(self):
        d = filedialog.askdirectory()
        if d: self.output_path.set(d)

    def start_download(self):
        url = self.url_var.get().strip()
        if not url: return
        self.download_btn.configure(state="disabled")
        threading.Thread(target=self.download_logic, args=(url,), daemon=True).start()

    def download_logic(self, url):
        raw_filename = unquote(url.split('/')[-1]).split('?')[0]
        filename = re.sub(r'[<>:"/\\|?*]', '_', raw_filename)
        if not filename or "." not in filename: filename = "descarga.bin"
        full_dest = os.path.join(self.output_path.get(), filename)
        ydl_opts = {'outtmpl': full_dest, 'progress_hooks': [self.update_progress], 'force_generic_extractor': True}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            MessageBox.showinfo("Éxito", "Descarga completada")
        except Exception as e:
            MessageBox.showerror("Error", str(e))
        finally:
            self.download_btn.configure(state="normal")

    def update_progress(self, d):
        if d['status'] == 'downloading':
            try:
                p = float(d.get('_percent_str', '0%').replace('%','')) / 100
                self.progress_bar.set(p)
            except: pass

if __name__ == "__main__":
    # Solo llegamos aquí si somos el MainProcess gracias al bloqueo inicial
    try:
        app = ArchiveDirectDownloader()
        # Retraso largo para evitar conflictos con la extracción de archivos temporales
        app.after(15000, app.update_engine) 
        app.mainloop()
    except Exception as e:
        with open("CRASH_LOG.txt", "w") as f:
            f.write(str(e))
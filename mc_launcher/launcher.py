import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import os
import sys
import shutil
import webbrowser

# ── Config ──────────────────────────────────────────────────────────────────
MC_VERSION    = "1.12.2"
FORGE_VERSION = "1.12.2-14.23.5.2860"
FORGE_PAGE    = "https://files.minecraftforge.net/net/minecraftforge/forge/index_1.12.2.html"

MOD_FILENAME = "gradle-wrapper.jar"

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOD_SRC = os.path.join(BASE_DIR, MOD_FILENAME)

if sys.platform == "win32":
    MC_DIR = os.path.join(os.environ.get("APPDATA", ""), ".minecraft")
else:
    MC_DIR = os.path.join(os.path.expanduser("~"), ".minecraft")

MODS_DIR = os.path.join(MC_DIR, "mods")

# ── Theme ────────────────────────────────────────────────────────────────────
BG        = "#0d0f14"
PANEL     = "#13161e"
ACCENT    = "#4ade80"
ACCENT2   = "#22d3ee"
YELLOW    = "#facc15"
TEXT      = "#e2e8f0"
SUBTEXT   = "#64748b"
FONT_HEAD = ("Courier New", 22, "bold")
FONT_BODY = ("Courier New", 10)
FONT_BTN  = ("Courier New", 11, "bold")
FONT_LOG  = ("Courier New", 9)


class MinecraftLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MC Launcher 1.12.2 — Forge Edition")
        self.geometry("720x580")
        self.resizable(False, False)
        self.configure(bg=BG)

        # ── Header ──
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(28, 0))
        tk.Label(header, text="⛏  MINECRAFT LAUNCHER", font=FONT_HEAD,
                 fg=ACCENT, bg=BG).pack(anchor="w")
        tk.Label(header, text=f"  v{MC_VERSION}  ·  Forge  ·  Custom Mod Pack",
                 font=FONT_BODY, fg=SUBTEXT, bg=BG).pack(anchor="w")
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x", padx=30, pady=(12, 0))

        # ── Info panel ──
        info = tk.Frame(self, bg=PANEL, padx=20, pady=14)
        info.pack(fill="x", padx=30, pady=(14, 0))
        self._row(info, "Minecraft", MC_VERSION, 0)
        self._row(info, "Forge",     FORGE_VERSION.split("-", 1)[1], 1)
        self._row(info, "Mod",       MOD_FILENAME, 2)
        self._row(info, "Mods dir",  MODS_DIR, 3)

        # ── Log box ──
        log_frame = tk.Frame(self, bg=PANEL, padx=14, pady=10)
        log_frame.pack(fill="both", expand=True, padx=30, pady=(14, 0))
        tk.Label(log_frame, text="// LOG OUTPUT", font=FONT_LOG,
                 fg=SUBTEXT, bg=PANEL).pack(anchor="w")
        self.log_text = tk.Text(log_frame, bg="#0a0c10", fg=ACCENT2,
                                font=FONT_LOG, bd=0, state="disabled",
                                wrap="word", height=9)
        self.log_text.pack(fill="both", expand=True, pady=(4, 0))

        # ── Progress ──
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("G.Horizontal.TProgressbar",
                        troughcolor=BG, background=ACCENT, thickness=6)
        self.progress = ttk.Progressbar(self, style="G.Horizontal.TProgressbar",
                                        mode="indeterminate")
        self.progress.pack(fill="x", padx=30, pady=(10, 0))

        # ── Buttons row 1 ──
        btn_row1 = tk.Frame(self, bg=BG)
        btn_row1.pack(fill="x", padx=30, pady=(12, 4))

        self.mod_btn = tk.Button(
            btn_row1, text="[ INSTALL MOD ]",
            font=FONT_BTN, fg=BG, bg=ACCENT, activebackground="#22c55e",
            relief="flat", cursor="hand2", padx=16, pady=10,
            command=self._install_mod)
        self.mod_btn.pack(side="left", padx=(0, 10))

        self.forge_dl_btn = tk.Button(
            btn_row1, text="[ DOWNLOAD FORGE ]",
            font=FONT_BTN, fg=BG, bg=YELLOW, activebackground="#eab308",
            relief="flat", cursor="hand2", padx=16, pady=10,
            command=self._open_forge_page)
        self.forge_dl_btn.pack(side="left", padx=(0, 10))

        self.forge_run_btn = tk.Button(
            btn_row1, text="[ RUN FORGE INSTALLER ]",
            font=FONT_BTN, fg=BG, bg=ACCENT2, activebackground="#06b6d4",
            relief="flat", cursor="hand2", padx=16, pady=10,
            command=self._run_forge)
        self.forge_run_btn.pack(side="left")

        # ── Buttons row 2 ──
        btn_row2 = tk.Frame(self, bg=BG)
        btn_row2.pack(fill="x", padx=30, pady=(0, 20))

        self.launch_btn = tk.Button(
            btn_row2, text="[ LAUNCH MINECRAFT ]",
            font=FONT_BTN, fg=BG, bg="#a78bfa", activebackground="#7c3aed",
            relief="flat", cursor="hand2", padx=16, pady=10,
            command=self._launch_minecraft)
        self.launch_btn.pack(side="left")

        self._log("Welcome! Follow these steps:", "ok")
        self._log("1. Click INSTALL MOD  →  copies mod to .minecraft/mods")
        self._log("2. Click DOWNLOAD FORGE  →  opens browser to download Forge")
        self._log("3. Click RUN FORGE INSTALLER  →  browse to the downloaded .jar")
        self._log("4. Click LAUNCH MINECRAFT  →  open the Minecraft Launcher")

    def _row(self, parent, label, value, row):
        tk.Label(parent, text=f"{label}:", font=FONT_BODY,
                 fg=SUBTEXT, bg=PANEL, width=14, anchor="w").grid(
            row=row, column=0, sticky="w", pady=2)
        tk.Label(parent, text=value, font=FONT_BODY,
                 fg=TEXT, bg=PANEL, anchor="w").grid(
            row=row, column=1, sticky="w", pady=2)

    def _log(self, msg, tag="default"):
        self.log_text.configure(state="normal")
        self.log_text.tag_configure("ok",      foreground=ACCENT)
        self.log_text.tag_configure("err",     foreground="#f87171")
        self.log_text.tag_configure("default", foreground=ACCENT2)
        self.log_text.tag_configure("warn",    foreground=YELLOW)
        self.log_text.insert("end", f"> {msg}\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # ── Step 1: Install mod ──────────────────────────────────────────────────
    def _install_mod(self):
        try:
            os.makedirs(MODS_DIR, exist_ok=True)
            dest = os.path.join(MODS_DIR, MOD_FILENAME)
            if os.path.exists(MOD_SRC):
                shutil.copy2(MOD_SRC, dest)
                self._log(f"Mod copied to mods folder!", "ok")
            else:
                self._log(f"ERROR: {MOD_FILENAME} not found next to launcher.", "err")
                self._log(f"Expected at: {MOD_SRC}", "err")
        except Exception as e:
            self._log(f"Error: {e}", "err")

    # ── Step 2: Open Forge download page ────────────────────────────────────
    def _open_forge_page(self):
        webbrowser.open(FORGE_PAGE)
        self._log("Opened Forge download page in your browser.", "ok")
        self._log("Download the Installer for 14.23.5.2860, then click RUN FORGE INSTALLER.", "warn")

    # ── Step 3: Browse to Forge jar and run it ───────────────────────────────
    def _run_forge(self):
        # Check common download locations first
        default_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        forge_jar = filedialog.askopenfilename(
            title="Select the Forge Installer .jar",
            initialdir=default_dir,
            filetypes=[("JAR files", "*.jar"), ("All files", "*.*")]
        )
        if not forge_jar:
            self._log("No file selected.", "warn")
            return
        try:
            java = self._find_java()
            self._log(f"Running: {os.path.basename(forge_jar)}")
            threading.Thread(
                target=lambda: self._run_jar(java, forge_jar), daemon=True).start()
        except FileNotFoundError as e:
            self._log(str(e), "err")

    def _run_jar(self, java, jar):
        self.progress.start(12)
        try:
            subprocess.run([java, "-jar", jar], check=False)
            self._log("Forge installer closed.", "ok")
            self._log("Now click LAUNCH MINECRAFT and select the Forge profile!", "ok")
        except Exception as e:
            self._log(f"Error running installer: {e}", "err")
        finally:
            self.progress.stop()

    # ── Step 4: Launch Minecraft Java Edition ────────────────────────────────
    def _launch_minecraft(self):
        try:
            java_launcher_paths = [
                r"C:\XboxGames\Minecraft Launcher\Content\gamelaunchhelper.exe",
                r"C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe",
                r"C:\Program Files\Minecraft Launcher\MinecraftLauncher.exe",
                r"C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe",
                r"C:\Program Files\Minecraft\MinecraftLauncher.exe",
                r"C:\Program Files (x86)\Minecraft\MinecraftLauncher.exe",
                os.path.join(os.environ.get("LOCALAPPDATA", ""),
                             "Packages", "Microsoft.4297127D64EC6_8wekyb3d8bbwe",
                             "LocalCache", "Local", "runtime", "jre-x64",
                             "bin", "javaw.exe"),
            ]
            for p in java_launcher_paths:
                if os.path.exists(p):
                    subprocess.Popen([p])
                    self._log("Minecraft Java Launcher opened!", "ok")
                    self._log("Select the 'forge' profile then click Play!", "warn")
                    return

            # Fallback: open launcher via launcher.jar in .minecraft
            javaw = shutil.which("javaw")
            launcher_jar = os.path.join(MC_DIR, "launcher.jar")
            if javaw and os.path.exists(launcher_jar):
                subprocess.Popen([javaw, "-jar", launcher_jar])
                self._log("Launched via launcher.jar!", "ok")
                return

            self._log("Could not find Java Edition launcher.", "err")
            self._log("Open 'Minecraft Launcher' (NOT Bedrock) from Start Menu.", "warn")
            os.startfile(MC_DIR)
            self._log("Opened your .minecraft folder for reference.", "default")
        except Exception as e:
            self._log(f"Error: {e}", "err")
            self._log("Open Minecraft Java Launcher manually from Start Menu.", "warn")

    # ── Java finder ──────────────────────────────────────────────────────────
    def _find_java(self):
        for candidate in ["java", "javaw"]:
            path = shutil.which(candidate)
            if path:
                return path
        for root in [r"C:\Program Files\Java",
                     r"C:\Program Files (x86)\Java",
                     r"C:\Program Files\Eclipse Adoptium",
                     r"C:\Program Files\Microsoft"]:
            if os.path.isdir(root):
                for jdir in sorted(os.listdir(root), reverse=True):
                    j = os.path.join(root, jdir, "bin", "java.exe")
                    if os.path.exists(j):
                        return j
        raise FileNotFoundError(
            "Java not found. Install Java 8 from java.com then try again.")


if __name__ == "__main__":
    app = MinecraftLauncher()
    app.mainloop()

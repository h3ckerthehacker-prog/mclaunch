# MC Launcher 1.12.2 — Forge Edition

A custom desktop launcher for Minecraft 1.12.2 with Forge and your mod bundled in.

## What it does
- Copies `gradle-wrapper.jar` into your `.minecraft/mods/` folder automatically
- Downloads the Forge 1.12.2 installer and runs it
- Has a Launch button to open the official Minecraft Launcher

---

## How to build the .exe (Windows)

### Requirements
- Python 3.8+ → https://www.python.org/downloads/
  - ✅ Tick "Add Python to PATH" during install
- Java 8 → https://www.java.com/en/download/
- Internet connection (to download Forge)

### Steps

1. Put these files all in the same folder:
   ```
   launcher.py
   build.bat
   gradle-wrapper.jar     ← your mod
   ```

2. Double-click `build.bat`

3. When it finishes, find your launcher at:
   ```
   dist\MC-Launcher-1.12.2.exe
   ```

4. Copy `MC-Launcher-1.12.2.exe` anywhere you like and run it!

---

## Using the launcher

| Button | What it does |
|---|---|
| **[ INSTALL FORGE + MOD ]** | Downloads Forge installer, runs it, copies the mod to `.minecraft/mods/` |
| **[ LAUNCH MINECRAFT ]** | Opens the official Minecraft Launcher |

### First-time setup order:
1. Click **INSTALL FORGE + MOD**
2. Complete the Forge installer window that pops up (click "Install client" → OK)
3. Click **LAUNCH MINECRAFT**
4. In the Minecraft Launcher, select the **"forge"** profile from the dropdown
5. Hit Play!

---

## Troubleshooting

**"Java not found"** — Install Java 8 from https://www.java.com

**Forge installer doesn't open** — Make sure Java is installed and associated with `.jar` files

**Mod not loading in-game** — Confirm Forge profile is selected in the Minecraft Launcher
---
## Quick Things!!!
Im currently working on a MacOS build and Linux So yeah Enjoy!!

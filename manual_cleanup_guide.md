# Manual Python Cleanup Guide 🧹

This guide will help you safely remove unnecessary Python installations and keep only `C:\Python313\python.exe`.

## ⚠️ Important Safety Notes

1. **Create a system restore point** before starting
2. **Close all Python applications** and IDEs
3. **Run Command Prompt as Administrator** for some steps
4. **Test each step** before moving to the next

---

## Step 1: Identify What You Have 🔍

Open Command Prompt and run these commands to see all Python installations:

```cmd
where python
where python3
py -0
```

Expected output shows multiple paths - we want to keep only `C:\Python313\python.exe`.

---

## Step 2: Disable Windows Store Python Aliases 🚫

The Windows Store Python aliases cause confusion. Disable them:

1. **Open Settings** (`Win + I`)
2. Go to **Apps** > **Advanced app settings** > **App execution aliases**
3. Find **Python** entries and **turn them OFF**:
   - `python.exe`
   - `python3.exe`

Or manually rename the files:
```cmd
cd %USERPROFILE%\AppData\Local\Microsoft\WindowsApps
ren python.exe python.exe.disabled
ren python3.exe python3.exe.disabled
```

---

## Step 3: Clean Up PATH Environment Variable 🛤️

### Check Current PATH:
```cmd
echo %PATH%
```

### Edit PATH:
1. **Open System Properties** (`Win + R` → `sysdm.cpl`)
2. Click **Environment Variables**
3. Select **PATH** in User variables → **Edit**
4. **Remove** entries containing:
   - `C:\Users\...\AppData\Local\Microsoft\WindowsApps` (if it has Python)
   - Any Python paths EXCEPT `C:\Python313` and `C:\Python313\Scripts`
5. Select **PATH** in System variables → **Edit**
6. **Remove** the same types of entries
7. Click **OK** to save

### Verify PATH is clean:
```cmd
# Close and reopen Command Prompt
echo %PATH%
```

---

## Step 4: Remove MSYS2 Python (if not needed) 🗑️

**⚠️ WARNING:** Only remove if you don't use Git Bash, MinGW, or MSYS2 for development.

If you want to remove MSYS2 Python:
1. **Uninstall MSYS2** from Control Panel > Programs
2. Or delete the folder: `C:\msys64` (if you're sure you don't need it)

**Alternative:** Keep MSYS2 but ensure it doesn't interfere:
- Don't add MSYS2 paths to your system PATH
- Use full path when needed: `C:\msys64\ucrt64\bin\python.exe`

---

## Step 5: Remove Other Python Installations 🗂️

**Check these common locations** and remove if found:

### User-installed Python:
```
%USERPROFILE%\AppData\Local\Programs\Python\
```

### Other system locations:
```
C:\Program Files\Python*
C:\Program Files (x86)\Python*
```

### How to remove:
1. **Uninstall via Control Panel** (preferred):
   - Control Panel > Programs > Uninstall a program
   - Look for "Python 3.x" entries (keep only Python 3.13.11)

2. **Manual deletion** (if uninstaller not available):
   - Delete the installation folders
   - Clean registry entries (advanced users only)

---

## Step 6: Clean Registry Entries (Advanced) 🔧

**⚠️ Only if comfortable with registry editing:**

1. **Open Registry Editor** (`Win + R` → `regedit`)
2. **Backup registry** (File > Export)
3. **Delete these keys** if they exist (and don't point to Python313):
   ```
   HKEY_CURRENT_USER\Software\Python
   HKEY_LOCAL_MACHINE\Software\Python
   HKEY_LOCAL_MACHINE\Software\WOW6432Node\Python
   ```
4. **Keep entries** that point to `C:\Python313`

---

## Step 7: Verify Your Clean Installation ✅

After cleanup, test your installation:

```cmd
# Test Python works
python --version
python -c "print('Hello World')"

# Test numpy works
python -c "import numpy; print('numpy', numpy.__version__)"

# Test sympy works
python -c "import sympy; print('sympy', sympy.__version__)"

# Test py launcher works
py --version
py -3.13 --version
```

**Expected results:**
- All commands should work
- All should point to `C:\Python313\python.exe`
- numpy and sympy should import successfully

---

## Step 8: Configure Your IDE 🔧

### VS Code:
1. **Open VS Code**
2. Press `Ctrl + Shift + P`
3. Type "Python: Select Interpreter"
4. Choose `C:\Python313\python.exe`

### PyCharm:
1. **File** > **Settings**
2. **Project** > **Python Interpreter**
3. Set to `C:\Python313\python.exe`

### Other IDEs:
- Set Python interpreter to `C:\Python313\python.exe`

---

## Step 9: Test Your Crypto Project 🎯

```cmd
cd A:\Python\Crypto

# Test basic imports
py -3.13 test_hill_imports.py

# Test your Hill cipher
py -3.13 hill\server.py

# Test package installation
py -3.13 -m pip install --upgrade numpy
```

---

## Troubleshooting 🔧

### If `python` command not found:
```cmd
# Add to PATH manually
set PATH=C:\Python313;C:\Python313\Scripts;%PATH%

# Or always use:
py -3.13 script.py
```

### If imports still fail:
```cmd
# Reinstall packages
py -3.13 -m pip install --force-reinstall numpy sympy
```

### If py launcher not working:
```cmd
# Repair Python installation
# Download Python 3.13 installer and choose "Repair"
```

---

## Final Recommendations 💡

### Always use these commands:
```cmd
# Run Python scripts
py -3.13 script_name.py

# Install packages
py -3.13 -m pip install package_name

# Check what's installed
py -3.13 -m pip list
```

### Create aliases (optional):
Add to your PowerShell profile:
```powershell
function python { py -3.13 $args }
function pip { py -3.13 -m pip $args }
```

---

## Backup & Recovery 💾

### Before cleanup, backup:
1. **System Restore Point**
2. **Export registry**: `HKEY_LOCAL_MACHINE\Software\Python`
3. **List installed packages**: `py -3.13 -m pip freeze > packages.txt`

### If something breaks:
1. **Restore system** restore point
2. **Reinstall Python 3.13** from python.org
3. **Reinstall packages**: `py -3.13 -m pip install -r packages.txt`

---

## Success Checklist ✅

- [ ] Windows Store aliases disabled
- [ ] PATH cleaned (only Python313 entries)
- [ ] Other Python installations removed
- [ ] `python --version` works
- [ ] `py -3.13 --version` works  
- [ ] numpy and sympy import successfully
- [ ] IDE configured to use `C:\Python313\python.exe`
- [ ] Crypto project runs without import errors
- [ ] Can install new packages with `py -3.13 -m pip install`

---

🎉 **Congratulations!** You now have a clean Python environment with only one installation, preventing future conflicts and import errors.
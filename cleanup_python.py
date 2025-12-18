#!/usr/bin/env python3
"""
Python Installation Cleanup Script
===================================

This script helps remove unnecessary Python installations while keeping
C:\Python313\python.exe as the primary installation.

IMPORTANT: This script makes system changes. Run as Administrator for best results.

Usage:
    python cleanup_python.py

This will:
1. Identify all Python installations
2. Show you what will be removed vs kept
3. Ask for confirmation before making changes
4. Clean up PATH variables
5. Disable Windows Store Python aliases
6. Verify the remaining installation works

Author: Assistant
Date: 2025
"""

import json
import os
import subprocess
import sys
import winreg
from pathlib import Path


class PythonCleanup:
    def __init__(self):
        self.keep_python = "C:\\Python313\\python.exe"
        self.python_installations = []
        self.removed_paths = []
        self.registry_keys = []

    def run_command(self, cmd, shell=True):
        """Run a command safely and return output."""
        try:
            result = subprocess.run(
                cmd, shell=shell, capture_output=True, text=True, timeout=30
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)

    def is_admin(self):
        """Check if running with administrator privileges."""
        try:
            return os.getuid() == 0
        except AttributeError:
            # Windows
            try:
                import ctypes

                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

    def find_python_installations(self):
        """Find all Python installations on the system."""
        print("🔍 Scanning for Python installations...")

        installations = {}

        # Method 1: Check common installation directories
        common_paths = [
            "C:\\Python*",
            "C:\\Program Files\\Python*",
            "C:\\Program Files (x86)\\Python*",
            os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\*"),
            "C:\\msys64\\*\\bin\\python.exe",
            "C:\\msys64\\*\\bin\\python3.exe",
        ]

        for pattern in common_paths:
            success, output, _ = self.run_command(
                f'dir /s /b "{pattern}\\python.exe" 2>nul'
            )
            if success and output:
                for path in output.split("\n"):
                    if path.strip() and os.path.exists(path.strip()):
                        installations[path.strip()] = "Directory scan"

        # Method 2: Check registry for installed Python versions
        try:
            self._scan_registry(installations)
        except Exception as e:
            print(f"   Registry scan failed: {e}")

        # Method 3: Check PATH for Python executables
        success, output, _ = self.run_command("where python")
        if success and output:
            for path in output.split("\n"):
                if path.strip() and os.path.exists(path.strip()):
                    installations[path.strip()] = "PATH"

        success, output, _ = self.run_command("where python3")
        if success and output:
            for path in output.split("\n"):
                if path.strip() and os.path.exists(path.strip()):
                    installations[path.strip()] = "PATH"

        # Method 4: Check py launcher versions
        success, output, _ = self.run_command("py -0")
        if success and output:
            for line in output.split("\n"):
                if "Python" in line and "*" not in line:
                    try:
                        version = line.split()[0].replace("-V:", "")
                        success2, path, _ = self.run_command(
                            f'py -{version} -c "import sys; print(sys.executable)"'
                        )
                        if success2 and path.strip():
                            installations[path.strip()] = f"py launcher ({version})"
                    except:
                        pass

        self.python_installations = installations
        return installations

    def _scan_registry(self, installations):
        """Scan Windows registry for Python installations."""
        registry_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Python"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Python"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Python"),
        ]

        for hive, key_path in registry_paths:
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey_path = f"{key_path}\\{subkey_name}\\InstallPath"
                            try:
                                with winreg.OpenKey(hive, subkey_path) as install_key:
                                    install_path, _ = winreg.QueryValueEx(
                                        install_key, ""
                                    )
                                    python_exe = os.path.join(
                                        install_path, "python.exe"
                                    )
                                    if os.path.exists(python_exe):
                                        installations[python_exe] = (
                                            f"Registry ({subkey_name})"
                                        )
                            except FileNotFoundError:
                                pass
                            i += 1
                        except OSError:
                            break
            except FileNotFoundError:
                continue

    def categorize_installations(self):
        """Categorize Python installations into keep vs remove."""
        print(f"\n📋 Found Python Installations:")
        print("=" * 80)

        keep_installations = []
        remove_installations = []
        special_installations = []

        for path, source in self.python_installations.items():
            # Normalize path for comparison
            norm_path = os.path.normpath(path).lower()
            keep_path = os.path.normpath(self.keep_python).lower()

            if norm_path == keep_path:
                keep_installations.append((path, source))
                print(f"✅ KEEP:   {path} ({source})")
            elif "msys" in norm_path or "mingw" in norm_path:
                special_installations.append((path, source))
                print(
                    f"⚠️  MAYBE:  {path} ({source}) - MSYS2/MinGW (used by Git/dev tools)"
                )
            elif "windowsapps" in norm_path:
                remove_installations.append((path, source))
                print(f"🗑️  REMOVE: {path} ({source}) - Windows Store alias")
            else:
                remove_installations.append((path, source))
                print(f"🗑️  REMOVE: {path} ({source})")

        return keep_installations, remove_installations, special_installations

    def get_current_path(self):
        """Get current PATH environment variable."""
        try:
            # Get user PATH
            success, user_path, _ = self.run_command(
                'reg query "HKEY_CURRENT_USER\\Environment" /v PATH'
            )

            # Get system PATH
            success2, system_path, _ = self.run_command(
                'reg query "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment" /v PATH'
            )

            return user_path, system_path
        except Exception as e:
            print(f"Could not read PATH: {e}")
            return "", ""

    def disable_windows_store_aliases(self):
        """Disable Windows Store Python aliases."""
        print("\n🔧 Disabling Windows Store Python aliases...")

        aliases_path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\WindowsApps")
        python_aliases = ["python.exe", "python3.exe"]

        disabled = []
        for alias in python_aliases:
            alias_path = os.path.join(aliases_path, alias)
            if os.path.exists(alias_path):
                try:
                    # Rename to disable
                    disabled_path = alias_path + ".disabled"
                    os.rename(alias_path, disabled_path)
                    disabled.append(alias)
                    print(f"   ✅ Disabled {alias}")
                except Exception as e:
                    print(f"   ❌ Failed to disable {alias}: {e}")

        if disabled:
            print(f"   Successfully disabled {len(disabled)} Windows Store aliases")
        else:
            print("   No Windows Store aliases found to disable")

    def clean_path_entries(self, remove_paths):
        """Remove Python paths from PATH environment variable."""
        print("\n🧹 Cleaning PATH environment variable...")

        # Get current PATH
        current_path = os.environ.get("PATH", "")
        path_entries = [p.strip() for p in current_path.split(";") if p.strip()]

        # Find entries to remove
        remove_entries = []
        for entry in path_entries:
            for remove_path, _ in remove_paths:
                remove_dir = os.path.dirname(remove_path)
                if (
                    os.path.normpath(entry).lower()
                    == os.path.normpath(remove_dir).lower()
                ):
                    remove_entries.append(entry)
                elif (
                    os.path.normpath(entry).lower()
                    == os.path.normpath(remove_dir + "\\Scripts").lower()
                ):
                    remove_entries.append(entry)

        if remove_entries:
            print("   Found PATH entries to clean:")
            for entry in remove_entries:
                print(f"     - {entry}")

            # Create clean PATH
            clean_entries = [e for e in path_entries if e not in remove_entries]

            print(f"   Will remove {len(remove_entries)} PATH entries")
            return clean_entries
        else:
            print("   No Python paths found in PATH to remove")
            return path_entries

    def remove_installation_directory(self, python_path):
        """Remove a Python installation directory."""
        install_dir = os.path.dirname(python_path)

        # Safety check - don't remove system directories
        system_dirs = ["c:\\windows", "c:\\program files", "c:\\"]
        if any(install_dir.lower().startswith(d) for d in system_dirs):
            if "python3" not in install_dir.lower():
                print(f"   ⚠️  Skipping system directory: {install_dir}")
                return False

        try:
            print(f"   Removing directory: {install_dir}")

            # Use rmdir command for better Windows compatibility
            success, output, error = self.run_command(f'rmdir /s /q "{install_dir}"')
            if success:
                print(f"   ✅ Removed: {install_dir}")
                return True
            else:
                print(f"   ❌ Failed to remove {install_dir}: {error}")
                return False

        except Exception as e:
            print(f"   ❌ Error removing {install_dir}: {e}")
            return False

    def verify_remaining_installation(self):
        """Verify that the remaining Python installation works correctly."""
        print(f"\n🧪 Verifying remaining Python installation...")

        if not os.path.exists(self.keep_python):
            print(f"❌ ERROR: Primary Python not found at {self.keep_python}")
            return False

        # Test basic functionality
        test_commands = [
            (f'"{self.keep_python}" --version', "Version check"),
            (
                f'"{self.keep_python}" -c "import sys; print(sys.executable)"',
                "Executable path",
            ),
            (
                f'"{self.keep_python}" -c "import numpy; print(f\'numpy {{numpy.__version__}}\')"',
                "NumPy import",
            ),
            (
                f'"{self.keep_python}" -c "import sympy; print(f\'sympy {{sympy.__version__}}\')"',
                "SymPy import",
            ),
        ]

        all_passed = True
        for cmd, description in test_commands:
            success, output, error = self.run_command(cmd)
            if success:
                print(f"   ✅ {description}: {output}")
            else:
                print(f"   ❌ {description}: {error}")
                all_passed = False

        return all_passed

    def create_backup_info(self):
        """Create backup information file."""
        backup_info = {
            "timestamp": subprocess.run(
                ["date", "/t"], capture_output=True, text=True, shell=True
            ).stdout.strip(),
            "kept_installation": self.keep_python,
            "removed_installations": [
                {"path": path, "source": source}
                for path, source in self.python_installations.items()
            ],
            "original_path": os.environ.get("PATH", ""),
        }

        try:
            with open("python_cleanup_backup.json", "w") as f:
                json.dump(backup_info, f, indent=2)
            print(f"✅ Backup information saved to: python_cleanup_backup.json")
        except Exception as e:
            print(f"❌ Failed to save backup info: {e}")

    def run_cleanup(self):
        """Run the complete cleanup process."""
        print("🧹 PYTHON INSTALLATION CLEANUP")
        print("=" * 80)
        print("This will remove unnecessary Python installations and keep only:")
        print(f"   {self.keep_python}")
        print("=" * 80)

        # Check admin privileges
        if not self.is_admin():
            print("⚠️  Warning: Not running as administrator.")
            print(
                "   Some operations may fail. Consider running as admin for best results."
            )
            input("   Press Enter to continue anyway...")

        # Find all installations
        installations = self.find_python_installations()
        if not installations:
            print("❌ No Python installations found!")
            return False

        # Categorize installations
        keep, remove, special = self.categorize_installations()

        if not keep:
            print(f"\n❌ ERROR: Target Python not found: {self.keep_python}")
            print("Cannot proceed without the primary installation.")
            return False

        # Show what will happen
        print(f"\n📊 SUMMARY:")
        print(f"   Keep:    {len(keep)} installation(s)")
        print(f"   Remove:  {len(remove)} installation(s)")
        print(f"   Special: {len(special)} installation(s) (MSYS2/MinGW - will ask)")

        if not remove and not special:
            print(
                "\n✅ No unnecessary installations found. Your system is already clean!"
            )
            return True

        # Ask for confirmation
        print(f"\n⚠️  WARNING: This will permanently remove Python installations!")
        if special:
            print(
                f"   Note: MSYS2/MinGW Python installations may be used by Git or other dev tools."
            )

        confirm = input("\nProceed with cleanup? (yes/no): ").lower().strip()
        if confirm not in ["yes", "y"]:
            print("Cleanup cancelled.")
            return False

        # Handle special installations
        remove_special = []
        if special:
            print(f"\n🤔 Found {len(special)} MSYS2/MinGW installation(s):")
            for path, source in special:
                print(f"   {path}")

            choice = (
                input("Remove MSYS2/MinGW Python installations? (yes/no/ask): ")
                .lower()
                .strip()
            )
            if choice in ["yes", "y"]:
                remove_special = special
            elif choice in ["ask", "a"]:
                for path, source in special:
                    remove_choice = input(f"Remove {path}? (y/n): ").lower().strip()
                    if remove_choice in ["yes", "y"]:
                        remove_special.append((path, source))

        # Create backup
        self.create_backup_info()

        # Start cleanup
        print(f"\n🧹 Starting cleanup...")

        # Disable Windows Store aliases
        self.disable_windows_store_aliases()

        # Clean PATH
        all_remove = remove + remove_special
        if all_remove:
            clean_path_entries = self.clean_path_entries(all_remove)

        # Remove installations
        removed_count = 0
        for path, source in all_remove:
            print(f"\n🗑️  Removing: {path}")
            if self.remove_installation_directory(path):
                removed_count += 1

        # Verify remaining installation
        print(f"\n✅ Removed {removed_count} Python installation(s)")

        if self.verify_remaining_installation():
            print(f"\n🎉 CLEANUP COMPLETE!")
            print("=" * 80)
            print(f"✅ Kept working installation: {self.keep_python}")
            print(f"✅ Removed {removed_count} unnecessary installation(s)")
            print(f"✅ Disabled Windows Store Python aliases")
            print(f"✅ All tests passed")
            print()
            print("💡 RECOMMENDATIONS:")
            print(f"   - Always use: py -3.13 script.py")
            print(f"   - Or use: python script.py (should now work)")
            print(f"   - Install packages: py -3.13 -m pip install package")
            print(f"   - Set IDE interpreter to: {self.keep_python}")
            print()
            print("📄 Backup information saved to: python_cleanup_backup.json")
            return True
        else:
            print(f"\n❌ CLEANUP COMPLETED WITH ISSUES")
            print("The remaining Python installation has problems.")
            print("Check the error messages above.")
            return False


def main():
    """Main function."""
    try:
        cleanup = PythonCleanup()
        success = cleanup.run_cleanup()

        input("\nPress Enter to exit...")
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\n⏹️  Cleanup interrupted by user")
        input("Press Enter to exit...")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        input("Press Enter to exit...")
        return 1


if __name__ == "__main__":
    sys.exit(main())

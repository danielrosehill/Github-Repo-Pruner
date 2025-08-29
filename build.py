#!/usr/bin/env python3
"""
Build script for GitHub Repository Pruner
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    print("GitHub Repository Pruner - Build Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("Error: main.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    
    # Determine the activation script path based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Install PyInstaller if not already installed
    if not run_command(f"{pip_cmd} install pyinstaller", "Installing PyInstaller"):
        sys.exit(1)
    
    # Clean previous build
    dist_dir = Path("dist")
    build_dir = Path("build")
    
    if dist_dir.exists():
        print("\nRemoving previous dist directory...")
        shutil.rmtree(dist_dir)
    
    if build_dir.exists():
        print("Removing previous build directory...")
        shutil.rmtree(build_dir)
    
    # Build the executable
    pyinstaller_cmd = f"{python_cmd} -m PyInstaller repopruner.spec"
    if not run_command(pyinstaller_cmd, "Building executable with PyInstaller"):
        sys.exit(1)
    
    # Check if build was successful
    executable_path = dist_dir / "repopruner"
    if os.name == 'nt':
        executable_path = executable_path.with_suffix('.exe')
    
    if executable_path.exists():
        print(f"\n✓ Build successful!")
        print(f"✓ Executable created: {executable_path.absolute()}")
        print(f"✓ Size: {executable_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # Make executable on Unix systems
        if os.name != 'nt':
            os.chmod(executable_path, 0o755)
            print("✓ Made executable")
        
        print(f"\nTo run: ./{executable_path}")
    else:
        print("✗ Build failed - executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()
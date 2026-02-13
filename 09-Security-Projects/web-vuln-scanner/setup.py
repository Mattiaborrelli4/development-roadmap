"""
Web Vulnerability Scanner - Setup Script
Automated installation and setup
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_step(text):
    """Print formatted step"""
    print(f"\n[*] {text}")


def print_success(text):
    """Print success message"""
    print(f"[✓] {text}")


def print_error(text):
    """Print error message"""
    print(f"[✗] {text}")


def check_python_version():
    """Check Python version"""
    print_step("Checking Python version...")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print_error(f"Python 3.10+ required. Found: {version.major}.{version.minor}")
        return False

    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_virtual_environment():
    """Create virtual environment"""
    print_step("Creating virtual environment...")

    venv_path = Path("venv")

    if venv_path.exists():
        print_success("Virtual environment already exists")
        return True

    try:
        subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            check=True,
            capture_output=True
        )
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create venv: {e}")
        return False


def get_pip_path():
    """Get pip path in venv"""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/pip")
    else:  # Unix
        return Path("venv/bin/pip")


def install_dependencies():
    """Install dependencies"""
    print_step("Installing dependencies...")

    pip_path = get_pip_path()
    requirements_path = Path("requirements.txt")

    if not requirements_path.exists():
        print_error("requirements.txt not found!")
        return False

    try:
        subprocess.run(
            [str(pip_path), "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProgressError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    print_step("Creating directories...")

    directories = [
        "reports",
        "logs",
        "scans"
    ]

    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)

    print_success("Directories created")


def create_env_file():
    """Create .env file from example"""
    print_step("Creating .env file...")

    env_example = Path(".env.example")
    env_file = Path(".env")

    if env_file.exists():
        print_success(".env file already exists")
        return

    if env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print_success(".env file created from .env.example")
    else:
        # Create basic .env
        with open(env_file, 'w') as f:
            f.write("# Web Vulnerability Scanner Configuration\n")
            f.write("TARGET_URL=http://localhost:8080\n")
            f.write("MAX_PAGES=50\n")
            f.write("SAFE_MODE=true\n")
        print_success("Basic .env file created")


def verify_installation():
    """Verify installation"""
    print_step("Verifying installation...")

    try:
        # Try importing main modules
        sys.path.insert(0, str(Path(__file__).parent))

        from scanners.crawler import WebCrawler
        from scanners.sql_injection import SQLiScanner
        from scanners.xss_scanner import XSSScanner
        from reporters.report_generator import ReportGenerator

        print_success("All modules imported successfully")
        return True
    except ImportError as e:
        print_error(f"Import failed: {e}")
        return False


def print_final_message():
    """Print final setup message"""
    print_header("Setup Complete!")

    print("\nYou can now use the scanner:")
    print("\n1. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix
        print("   source venv/bin/activate")

    print("\n2. Run scanner:")
    print("   python main.py --help")

    print("\n3. See disclaimer:")
    print("   python main.py disclaimer")

    print("\n4. Quick scan:")
    print("   python main.py scan https://example.com")

    print("\n" + "="*60)
    print("⚠️  IMPORTANT: Always have permission before scanning!")
    print("="*60 + "\n")


def main():
    """Main setup function"""
    print_header("Web Vulnerability Scanner - Setup")

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Create directories
    create_directories()

    # Create .env file
    create_env_file()

    # Verify installation
    if not verify_installation():
        print_error("Installation verification failed")
        print("\nPlease check the error messages above and try again.")
        sys.exit(1)

    # Print final message
    print_final_message()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

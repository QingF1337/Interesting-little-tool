# Check if Python is installed
try {
    python --version | Out-Null
} catch {
    Write-Host "Error: Python not found. Please install Python 3.6+ first." -ForegroundColor Red
    Write-Host "Visit https://www.python.org/downloads/ to download and install." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is installed
try {
    pip --version | Out-Null
} catch {
    Write-Host "Error: pip not found. Please make sure pip was selected during Python installation." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install PyInstaller
Write-Host "Installing PyInstaller..." -ForegroundColor Green
pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install PyInstaller" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Package the program
Write-Host "Packaging the program..." -ForegroundColor Green
pyinstaller --onefile --windowed --name "PC Optimization Master" main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Packaging failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Packaging successful!" -ForegroundColor Green
Write-Host "Executable file is located at dist\PC Optimization Master.exe" -ForegroundColor Green
Write-Host "Please run the file as administrator" -ForegroundColor Green
Read-Host "Press Enter to exit"

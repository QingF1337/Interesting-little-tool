# PC Optimization Master

A Python-based PC optimization program that helps clean up system junk and optimize system performance.

## Features

- ✅ Clean system temporary files
- ✅ Clean registry junk
- ✅ Manage startup items (view and disable)
- ✅ Disk defragmentation
- ✅ Optimize system services
- ✅ Intuitive graphical interface
- ✅ Detailed logging
- ✅ Automatic admin privilege request
- ✅ Support for packaging as executable file

## Environment Requirements

- Windows 7/8/10/11 operating system
- Python 3.6 or higher
- Administrator privileges (required when running the program)

## Installation Steps

### Method 1: Run directly (requires Python environment)

1. **Install Python**
   - Visit https://www.python.org/downloads/ to download and install Python 3.6+
   - Select "Add Python to PATH" during installation

2. **Download the program**
   - Download the program files to your local folder

3. **Run the program**
   - Run Command Prompt as administrator
   - Navigate to the program directory
   - Execute command: `python main.py`

### Method 2: Use executable file (no Python environment required)

1. **Package the program**
   - On a computer with Python environment, run the `build.bat` script
   - The script will automatically install PyInstaller and package the program

2. **Use the packaged file**
   - After packaging is complete, the executable file is located at `dist\电脑优化大师.exe`
   - Copy this file to any Windows computer
   - Run the file as administrator

## Packaging Instructions

1. **Run the packaging script**
   - Double-click to run the `build.bat` file
   - The script will automatically check the Python environment and install necessary dependencies

2. **Get the executable file**
   - After successful packaging, the executable file will be generated in the `dist` directory
   - The file name is `电脑优化大师.exe`

3. **Distribute the executable file**
   - You can share the generated executable file with friends who don't have Python environment
   - They just need to run the file as administrator

## Usage

1. **Run the program**
   - Run the program as administrator
   - The program will automatically check and request administrator privileges

2. **Perform one-click optimization**
   - In the main interface, select the optimization options you want to execute (all selected by default)
   - Click the "Start Optimization" button
   - Wait for the optimization to complete and view the optimization results

3. **Manage startup items**
   - Click the "Manage Startup Items" button
   - View all startup items in the pop-up window
   - Select unnecessary startup items and click the "Disable Selected" button
   - Click the "Refresh" button to update the startup item list
   - Click the "Close" button when done

## Notes

- Administrator privileges are required when running the program
- The optimization process may temporarily occupy system resources
- It is recommended to run the optimization program regularly to maintain system performance

## Program Structure

- `main.py` - Program entry point
- `optimizer.py` - System optimization core functions
- `gui.py` - Graphical user interface
- `logger.py` - Logging functionality
- `build.bat` - Packaging script
- `README.md` - Chinese user manual
- `README_EN.md` - English user manual
- `logs/` - Log file storage directory

## Technical Notes

- Uses tkinter library to create graphical interface
- Uses subprocess to call system commands
- Uses winreg to operate Windows registry
- Uses multi-threading to avoid interface lag
- Detailed error handling and logging

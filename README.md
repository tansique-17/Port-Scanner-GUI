# Port-Scanner

This Port Scanner is a professional-grade graphical tool built using Python and CustomTkinter to scan open TCP ports on a given IP address or URL. The program allows users to specify a target, start port, and end port for scanning and displays the results in a user-friendly table format.

## Features
- **Scan Open Ports**: Identify open TCP ports on a specified target.
- **Custom Port Range**: Specify the start and end ports for scanning.
- **Automatic Host Resolution**: Supports both IP addresses and domain names.
- **Threaded Scanning**: Utilizes multithreading for faster scanning.
- **Interactive GUI**: Intuitive graphical interface built with CustomTkinter.
- **Service Detection**: Attempts to detect the service running on open ports.
- **Progress Updates**: Displays the current scanning progress.
- **Professional Design**: Enhanced UI with consistent styling and modern look.

## Requirements
To run this program, you need the following:

- Python 3.7 or later
- Required Python libraries:
  - `socket`
  - `threading`
  - `concurrent.futures`
  - `customtkinter`
  - `tkinter`

You can install the required libraries using pip:
```bash
pip install customtkinter
```

## Installation
1. Clone or download the repository to your local machine.
2. Ensure you have Python installed.
3. Install the required libraries if not already installed.

## Usage
1. Run the program:
   ```bash
   python port_scanner.py
   ```
2. Enter the target (IP address or URL) in the "Target" field.
3. Optionally specify the start and end ports for scanning (default is 1-1024).
4. Click the "Start Scan" button or press `Enter` to begin scanning.
5. View the results in the table below.

## Screenshot
Below is a screenshot of the Port Scanner in action:

![Port Scanner](https://github.com/user-attachments/assets/3ffcb80c-b1e6-4ae5-8c8b-cdc75ea1b462)


## GUI Components
- **Toolbar**:
  - **About**: Displays information about the program.
  - **Exit**: Closes the application.
  - **Screenshot**: Displays a reference screenshot of the tool.
- **Input Section**:
  - Enter the target, start port, and end port.
  - Click "Start Scan" to begin the scan.
- **Status Label**: Displays the current scanning status.
- **Results Table**: Shows open ports, their status, and detected services.

## Error Handling
- Validates the target input (IP or URL).
- Ensures the port range is valid (1-65535).
- Displays error messages for invalid inputs.

## About
**Author**: Tansique Dasari  
**Version**: 1.0  
**Description**: This tool scans open TCP ports on a target machine.  
**Contact**: [tansique.17@gmail.com](mailto:tansique.17@gmail.com)  
**GitHub**: [tansique-17](https://github.com/tansique-17)

## License
This project is licensed under the MIT License. See the LICENSE file for details.


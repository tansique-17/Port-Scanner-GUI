import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk
from tkinter import ttk, messagebox

# Function to validate input
def validate_input(input_data):
    try:
        socket.inet_aton(input_data)
        return 'ip', input_data
    except socket.error:
        try:
            ip = socket.gethostbyname(input_data)
            return 'url', ip
        except socket.gaierror:
            raise ValueError("Invalid input: " + input_data)

# Clear results table
def clear_table():
    for row in tree.get_children():
        tree.delete(row)

# Update the status message
def update_status_message(message):
    status_label.configure(text=message)
    app.update()

# Function to scan a single port
def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                service = socket.getservbyport(port, "tcp") if port <= 65535 else "Unknown"
                update_table(port, "Open", service)
    except Exception:
        pass

# Threaded scanning function using ThreadPoolExecutor
def scan_ports(host, start_port, end_port):
    clear_table()  # Clear previous results
    total_ports = end_port - start_port + 1

    # Progress tracker
    def progress_update(future, port):
        current = progress_counter["current"] + 1
        progress_counter["current"] = current
        update_status_message(f"Scanning {port}/{end_port}")

    progress_counter = {"current": 0}

    # Use ThreadPoolExecutor for managing threads
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {}
        for port in range(start_port, end_port + 1):
            future = executor.submit(scan_port, host, port)
            futures[future] = port

        for future in futures:
            port = futures[future]
            future.add_done_callback(lambda f, p=port: progress_update(f, p))
            future.result()

    update_status_message("Scan Complete")

# Update the results table
def update_table(port, status, service):
    tree.insert("", "end", values=(port, status, service))

# Start scanning process
def start_scan(event=None):
    target = entry_target.get().strip()

    # Use default values if fields are empty
    start_port_text = entry_start_port.get().strip()
    end_port_text = entry_end_port.get().strip()

    start_port = int(start_port_text) if start_port_text.isdigit() else 1
    end_port = int(end_port_text) if end_port_text.isdigit() else 1024

    try:
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            raise ValueError("Invalid port range.")

        _, validated_host = validate_input(target)
        update_status_message("Starting scan...")
        threading.Thread(target=scan_ports, args=(validated_host, start_port, end_port), daemon=True).start()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        update_status_message("Error: Invalid input.")

# Function to show About information
def show_about():
    messagebox.showinfo("About", "Port Scanner by Tansique Dasari\nVersion 1.0\n\nThis tool scans open TCP ports.\nContact: tansique.17@gmail.com\ngithub: tansique-17")

# Function to exit the application
def exit_application():
    app.destroy()

# GUI Setup
app = ctk.CTk()
app.title("Port Scanner by Tansique Dasari")
app.geometry("700x400")  # Adjusted the window size to make it shorter and narrower
app.configure(bg="black")

# Toolbar Section
toolbar = ctk.CTkFrame(app, fg_color="black")
toolbar.pack(fill="x", pady=5)

about_button = ctk.CTkButton(toolbar, text="About", command=show_about, text_color="black", fg_color="white",
                             border_color="white", font=("Arial", 12), width=100)
about_button.pack(side="left", padx=10, pady=5)

exit_button = ctk.CTkButton(toolbar, text="Exit", command=exit_application, text_color="black", fg_color="white",
                            border_color="white", font=("Arial", 12), width=100)
exit_button.pack(side="left", padx=10, pady=5)

# Input Section
frame_input = ctk.CTkFrame(app, fg_color="black")
frame_input.pack(pady=5)  # Reduced vertical padding

label_target = ctk.CTkLabel(frame_input, text="Target (IP/URL):", text_color="white", font=("Arial", 14))
label_target.grid(row=0, column=0, padx=5, pady=5)
entry_target = ctk.CTkEntry(frame_input, width=300, placeholder_text="Enter IP or URL", placeholder_text_color="gray",
                            border_color="white", fg_color="black", text_color="white", font=("Arial", 14))
entry_target.grid(row=0, column=1, padx=5, pady=5)

label_start_port = ctk.CTkLabel(frame_input, text="Start Port:", text_color="white", font=("Arial", 14))
label_start_port.grid(row=1, column=0, padx=5, pady=5)
entry_start_port = ctk.CTkEntry(frame_input, width=100, placeholder_text="1", placeholder_text_color="gray",
                                border_color="white", fg_color="black", text_color="white", font=("Arial", 14))
entry_start_port.grid(row=1, column=1, padx=5, pady=5, sticky="w")

label_end_port = ctk.CTkLabel(frame_input, text="End Port:", text_color="white", font=("Arial", 14))
label_end_port.grid(row=2, column=0, padx=5, pady=5)
entry_end_port = ctk.CTkEntry(frame_input, width=100, placeholder_text="1024", placeholder_text_color="gray",
                              border_color="white", fg_color="black", text_color="white", font=("Arial", 14))
entry_end_port.grid(row=2, column=1, padx=5, pady=5, sticky="w")

entry_target.bind("<Return>", start_scan)
entry_start_port.bind("<Return>", start_scan)
entry_end_port.bind("<Return>", start_scan)

scan_button = ctk.CTkButton(frame_input, text="Start Scan", command=start_scan, text_color="black", fg_color="white",
                            border_color="white", font=("Arial", 14))
scan_button.grid(row=3, columnspan=2, pady=5)  # Reduced vertical padding

status_label = ctk.CTkLabel(app, text="Waiting for input...", text_color="white", font=("Arial", 14))
status_label.pack(pady=5)

# Results Table
frame_table = ctk.CTkFrame(app, fg_color="black", height=200)  # Reduced height of the result box
frame_table.pack(fill="both", expand=True, pady=5)  # Reduced vertical padding

columns = ("Port", "Status", "Service")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", style="Custom.Treeview")

# Configure Treeview styling
style = ttk.Style()
style.theme_use("default")
style.configure("Custom.Treeview", background="black", foreground="white", rowheight=20, fieldbackground="black",
                font=("Arial", 12), borderwidth=0)
style.configure("Custom.Treeview.Heading", background="black", foreground="white", font=("Arial Bold", 12))

for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, anchor="center", width=150)

# Add scrollbars for the Treeview
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=lambda *args: (scrollbar.set(*args), update_scrollbar(*args)))

# Show scrollbar only when necessary
def update_scrollbar(*args):
    if tree.yview() == (0.0, 1.0):  # Fully visible
        scrollbar.pack_forget()
    else:
                scrollbar.pack(side="right", fill="y")

tree.pack(fill="both", expand=True)

# Initial focus
entry_target.focus()

# Handle window close with Exit
app.protocol("WM_DELETE_WINDOW", exit_application)

app.mainloop()

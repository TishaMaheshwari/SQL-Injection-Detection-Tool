import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from manual_test import manual_scan
from auto_test import auto_scan
from report import report
from pdf_report import generate_pdf
import time
import subprocess
import os

# Allowed Targets (Ethical Protection)
allowed_targets = [
    "localhost",
    "127.0.0.1",
    "testphp.vulnweb.com"
]

# Variables to store last scan for PDF
last_target = ""
last_manual = ""
last_payloads = []
last_auto = ""
last_severity = ""
last_time = 0

# Dynamic show PDF button placeholder
show_pdf_button = None

# Calculate Severity
def calculate_severity(payloads):
    if any("UNION" in p for p in payloads):
        return "HIGH"
    elif any("OR" in p for p in payloads):
        return "MEDIUM"
    elif payloads:
        return "LOW"
    else:
        return "NONE"

# View Scan History
def show_history():
    try:
        with open("history.txt","r") as file:
            data = file.read()
        output_text.delete(1.0,tk.END)
        output_text.insert(tk.END,"===== SCAN HISTORY =====\n\n","system")
        output_text.insert(tk.END,data,"info")
    except:
        output_text.insert(tk.END,"No History Found\n","warning")

# Open PDF report
def open_pdf():
    pdf_path = "SQL_Report.pdf"
    if os.path.exists(pdf_path):
        if os.name == 'nt':  # Windows
            os.startfile(pdf_path)
        elif os.name == 'posix':  # Linux / Mac
            subprocess.run(['xdg-open', pdf_path])
    else:
        output_text.insert(tk.END,"PDF not found!\n","warning")

# Generate PDF and show button
def create_pdf():
    global show_pdf_button

    if last_target == "":
        output_text.insert(tk.END,"Run Scan First Before Generating PDF\n","warning")
        return

    # Generate PDF
    generate_pdf(
        last_target,
        last_manual,
        last_payloads,
        last_auto,
        last_severity,
        last_time
    )

    output_text.insert(tk.END,"PDF Report Generated (SQL_Report.pdf)\n","system")

    # Remove old button if exists
    try:
        show_pdf_button.destroy()
    except:
        pass

    # Create new Show PDF button
    show_pdf_button = tk.Button(
        pdf_button_frame,
        text="Show PDF",
        font=("Arial",12),
        command=open_pdf
    )
    show_pdf_button.pack(side=tk.LEFT,pady=5)

# Scan Function
def start_scan():
    global last_target, last_manual, last_payloads, last_auto, last_severity, last_time

    target = target_entry.get().strip()
    if not target:
        output_text.insert(tk.END,"Enter Target URL First\n","warning")
        return
    if not any(a in target for a in allowed_targets):
        output_text.insert(tk.END,"WARNING: Unauthorized Target\n","warning")
        output_text.insert(tk.END,"Use DVWA or TestPHP Only\n\n","warning")
        return

    output_text.delete(1.0,tk.END)
    progress['value'] = 0
    window.update_idletasks()
    start_time = time.time()

    # Target Info
    output_text.insert(tk.END,"Target:\n","system")
    output_text.insert(tk.END,target+"\n\n","info")

    # Manual Scan
    output_text.insert(tk.END,"Starting Manual Scan...\n","info")
    manual_result,payloads = manual_scan(target)
    severity = calculate_severity(payloads)
    color = "red" if manual_result=="VULNERABLE" else "green"
    output_text.insert(tk.END,f"Manual Result: {manual_result}\n",color)
    output_text.insert(tk.END,f"Severity: {severity}\n","purple")
    output_text.insert(tk.END,"Payloads Tested:\n","system")
    for p in payloads:
        output_text.insert(tk.END,"• "+p+"\n","info")
    output_text.insert(tk.END,"\n")
    progress['value'] = 50
    window.update_idletasks()

    # Automated Scan
    output_text.insert(tk.END,"Starting Automated Scan (SQLmap)...\n","info")
    auto_result = auto_scan(target)
    color = "red" if auto_result=="VULNERABLE" else "green"
    output_text.insert(tk.END,f"Automated Result: {auto_result}\n\n",color)
    progress['value'] = 100
    window.update_idletasks()

    # Vulnerability Details
    output_text.insert(tk.END,"Vulnerability Details\n","system")
    if manual_result=="VULNERABLE" or auto_result=="VULNERABLE":
        output_text.insert(tk.END,"Type: SQL Injection\n","info")
        output_text.insert(tk.END,"Impact: Database Access Possible\n\n","info")
    else:
        output_text.insert(tk.END,"No SQL Injection Detected\n\n","green")

    # Scan Time
    end_time = time.time()
    total_time = round(end_time-start_time,2)
    output_text.insert(tk.END,f"Scan Time: {total_time} seconds\n\n","purple")

    # Save last scan results for PDF
    last_target = target
    last_manual = manual_result
    last_payloads = payloads
    last_auto = auto_result
    last_severity = severity
    last_time = total_time

    # Generate Report (text file)
    report(target,manual_result,payloads,auto_result)
    output_text.insert(tk.END,"Report Generated\n","system")
    output_text.insert(tk.END,"Scan History Updated\n","system")

# GUI Theme
style = Style(theme="darkly")
window = style.master
window.title("SQL Injection Detection Tool")
window.geometry("820x650")

# Title
title = tk.Label(window,text="SQL Injection Detection Tool",font=("Arial",20))
title.pack(pady=10)

# Target URL Box
frame = tk.Frame(window)
frame.pack(pady=5)
tk.Label(frame,text="Target URL:").pack(side=tk.LEFT)
target_entry = tk.Entry(frame,width=60)
target_entry.pack(side=tk.LEFT)

# Buttons Frame
btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)
scan_button = tk.Button(btn_frame,text="Start Scan",font=("Arial",12),command=start_scan)
scan_button.pack(side=tk.LEFT,padx=10)
history_button = tk.Button(btn_frame,text="View History",font=("Arial",12),command=show_history)
history_button.pack(side=tk.LEFT,padx=10)
pdf_button = tk.Button(btn_frame,text="Generate PDF Report",font=("Arial",12),command=create_pdf)
pdf_button.pack(side=tk.LEFT,padx=10)

# Dynamic PDF Button Frame
pdf_button_frame = tk.Frame(window)
pdf_button_frame.pack(pady=5)

# Progress Bar
progress = ttk.Progressbar(window,orient='horizontal',length=750,mode='determinate')
progress.pack(pady=10)

# Output Window
output_text = tk.Text(window,height=25,width=95)
output_text.pack(pady=10)

# Color Styles
output_text.tag_config("info",foreground="cyan")
output_text.tag_config("red",foreground="red",font=("Arial",11,"bold"))
output_text.tag_config("green",foreground="lime",font=("Arial",11,"bold"))
output_text.tag_config("warning",foreground="orange",font=("Arial",11,"bold"))
output_text.tag_config("purple",foreground="violet")
output_text.tag_config("system",foreground="yellow",font=("Arial",11,"bold"))

window.mainloop()

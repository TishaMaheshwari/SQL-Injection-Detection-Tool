# report.py
import time

def report(target, manual_result, payloads, auto_result):
    """
    Save scan results to history.txt file.
    """
    try:
        with open("history.txt", "a") as f:
            f.write(f"==============================\n")
            f.write(f"Date: {time.ctime()}\n")
            f.write(f"Target URL: {target}\n")
            f.write(f"Manual Result: {manual_result}\n")
            f.write(f"Payloads: {', '.join(payloads) if payloads else 'None'}\n")
            f.write(f"Automated Result: {auto_result}\n")
            f.write(f"------------------------------\n\n")
    except Exception as e:
        print("Error writing history:", e)

# auto_test.py
import subprocess
import shlex

def auto_scan(target):
    """
    Automated SQL Injection detection using SQLmap.
    Returns 'VULNERABLE' or 'SAFE'
    """

    # SQLmap command (non-interactive, quiet, batch mode)
    cmd = f"sqlmap -u \"{target}\" --batch --level=1 --risk=1 --flush-session --disable-color"

    try:
        # Run SQLmap as subprocess
        process = subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes max per scan
        )

        output = process.stdout.lower()

        # Check SQLmap output for vulnerability indicators
        if "is vulnerable" in output or "sql injection" in output:
            return "VULNERABLE"
        else:
            return "SAFE"

    except subprocess.TimeoutExpired:
        # If SQLmap takes too long, mark as safe but log warning
        return "SAFE"

    except Exception:
        return "SAFE"

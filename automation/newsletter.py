#!/usr/bin/env python3
print("SCRIPT STARTED", flush=True)

import os
import sys

print(f"Python version: {sys.version}", flush=True)
print(f"Current dir: {os.getcwd()}", flush=True)

try:
    print("Listing parent directory...", flush=True)
    print(os.listdir('..'), flush=True)
    
    print("Attempting to write file...", flush=True)
    with open('../madison-al/index.html', 'w') as f:
        f.write("<html><body><h1>TEST - It works!</h1></body></html>")
    
    print("SUCCESS!", flush=True)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()

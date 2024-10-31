import time
import os
import subprocess
import sys

def run_code_from_file(filename):
    process = subprocess.Popen(['python', filename])
    return process

def watch_file(filename, interval=1):
    last_modified = os.path.getmtime(filename)
    process = run_code_from_file(filename)
    
    while True:
        try:
            current_modified = os.path.getmtime(filename)
            if current_modified != last_modified:
                print("\n--- Executing Code ---")
                process.terminate()
                process = run_code_from_file(filename)
                last_modified = current_modified
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStop Monitoring.")
            process.terminate()
            break

if len(sys.argv) > 1:
	link = sys.argv[1]
	watch_file(link)
else:
	print("input not found.")
import subprocess
import sys

def run_clients(commands):
    processes = []

    for cmd in commands:
        print(f"Running command: {' '.join(cmd)}")
        processes.append(subprocess.Popen(cmd))

    # Optionally, wait for all clients to finish
    for process in processes:
        process.wait()

if __name__ == "__main__":
    commands = [
        ["python3", "client.py", "54321", "example.com.", "A", "5"],
        ["python3", "client.py", "54321", "example.com.", "A", "1"],
        ["python3", "client.py", "54321", "bar.example.com.", "CNAME", "5"],
        ["python3", "client.py", "54321", ".", "NS", "5"],
        ["python3", "client.py", "54321", "bar.example.com.", "A", "5"],
        ["python3", "client.py", "54321", "foo.example.com.", "A", "5"],
        ["python3", "client.py", "54321", "example.org.", "A", "5"],
        ["python3", "client.py", "54321", "example.org.", "CNAME", "5"],
        ["python3", "client.py", "54321", "example.org.", "NS", "5"],
        ["python3", "client.py", "54321", "www.metalhead.com.", "A", "5"]
    ]

    run_clients(commands)

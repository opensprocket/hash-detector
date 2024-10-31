import os
import hashlib

# List of known malicious hashes
malicious_hashes = [
    "4bc8448b818a983db84f44a4fafd60c4",
    "8e5d5629672fcf8664bc28f42f79453f",
    "d35482baeab98cd49621866021e9e6fa",
    "5d80aaea305d1cb46b2e987270a3aa95"
]

# Directories to be scanned
directories = ['/etc', '/home', '/var', '/dev', '/bin']

def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def scan_and_remove():
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = md5(file_path)
                if file_hash in malicious_hashes:
                    print(f"Malicious file found: {file_path} (hash: {file_hash})")
                    # os.remove(file_path)
                    print(f"Removed: {file_path}")

def check_apache():
    response = os.system("curl -Is http://localhost | head -n 1")
    if response == 0:
        print("Apache server is running correctly.")
    else:
        print("Apache server is not running correctly.")
        # Restart Apache if needed
        # os.system("sudo service apache2 restart")

if __name__ == "__main__":
    scan_and_remove()
    check_apache()
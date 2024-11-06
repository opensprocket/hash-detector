import os
import hashlib
import subprocess

# list of malicious hashes
malicious_hashes = [
    "4bc8448b818a983db84f44a4fafd60c4",
    "8e5d5629672fcf8664bc28f42f79453f",
    "d35482baeab98cd49621866021e9e6fa",
    "5d80aaea305d1cb46b2e987270a3aa95",
    "d3724e3ec16d6f87e3b30197e05f6dd2",
    "919761b28a10d94b52194c85512135c3",
    "d2c0d67b375afc00569e17786db2b523",
    # "bd940531c84bf45f725836189cc9a7df",
]

# directories to be scanned
dirs_to_scan = ['/etc', '/home', '/var', '/dev', '/bin']

# directories to exclude when chasing symlinks
excluded_dirs = ['/proc', '/sys', '/run', '/tmp', '/mnt', '/media', '/dev/core']

# excluded files and "files"
excluded_files = ['/dev/core',]

# statistics
stats = {}

'''
Return the hexdigest of a file given a file_path
'''
def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

'''
Check if service is running
'''
def check_service(service_name):
    status = subprocess.runsystem(f'systemctl is-active {service_name}')
    if status == "active":
        return True
    else:
        return False

'''
Scan each directory for files that match the above hash list
'''
def scan_and_remove():
    malicious_files_found = 0
    for directory in dirs_to_scan:
        for current_dir, dirs, files in os.walk(directory):

            # exclude directories listed above using slicing
            dirs[:] = [dir for dir in dirs if os.path.join(current_dir, dir) not in excluded_dirs]

            for file in files:
                file_path = os.path.join(current_dir, file)
                # print(f'Scanning: {file_path}')

                # check if it is a file and not a unix socket or otherwise
                if os.path.isfile(file_path) and file_path not in excluded_files:
                    file_hash = md5(file_path)
                    if file_hash in malicious_hashes:
                        print(f"Malicious file found: {file_path} (hash: {file_hash})")
                        os.remove(file_path)
                        print(f"Removed: {file_path}")

                        # stats 
                        malicious_files_found += 1

                        # add count if present, otherwise start tracking
                        if file_hash in stats:
                            stats[file_hash] += 1
                        else:
                            stats[file_hash] = 1

    print(f'Number of malicous files found: {malicious_files_found}')
    print('Frequency of malware by hash:')
    print(stats)

def check_apache():
    
    # check index.php integrity
    print("Checking index.php file integrity...")

    index_good_hash = "dc7e3ef52926cea2938b8398591a4a7e"
    temp_index_hash = md5("/var/www/html/index.php")

    # restore if broken
    if temp_index_hash != index_good_hash:
        os.system('sudo cp /home/blueteam/index.php /var/www/html/index.php')
        os.system('sudo chmod 644 /var/www/html/index.php')
        print("Replaced corrupted index.php")
    else:
        print("No file integrity issues, continuing...")

    # check service status
        svc_status = check_service("apache2")
    if svc_status:
        print("Service is active, continuing...")
    else:
        # unmask service
        os.system('sudo systemctl unmask apache2')

        # check for other processes using port 80
        result = subprocess.run(['sudo', 'lsof', '-i :80'], stdout=subprocess.PIPE)
        lsof_output = result.stdout.decode()
        lsof_results = lsof_output.splitlines()
        
        del lsof_results[0] # remove headers from data
        
        for line in lsof_results:
            temp = line.split() # strip all whitespace
            
            # kill processes using port 80 that aren't apache
            if temp[0] != 'apache2':
                print(f'Stopping ')
                os.system(f'kill -9 {temp[1]}')
                


    # restart apache
    os.system("sudo service apache2 restart")
    print("Apache service restarted...")
    

    # # check response code
    # response = os.system("curl -Is http://localhost | head -n 1")
    # if '200 OK' in response:
    #     print("Return code OK, continuing...")
    # else:


    # check index.php


if __name__ == "__main__":
    scan_and_remove()
    check_apache()
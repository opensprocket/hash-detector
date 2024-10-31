import os
import hashlib

bad_hashes = [
    "4bc8448b818a983db84f44a4fafd60c4",
    "8e5d5629672fcf8664bc28f42f79453f",
    "d35482baeab98cd49621866021e9e6fa",
    "5d80aaea305d1cb46b2e987270a3aa95"
]

dirs_to_scan = [
    '/etc', '/home', '/var', '/dev', '/bin'
]

def hash_file(input_file):
    '''
    Takes an input_file and reads it 4KiB at a time and returns a hex digest.
    '''
    
    # create object to iterate over
    hash_value = hashlib.md5()
    
    # open file for reading
    with open(input_file, 'rb') as file:
        # iterate chuck by chunk until EOF
        for chunk in iter(lambda: file.read(4096), b""):
            hash_value.update(chunk)
    # return hexdigest for comparision
    return hash_value.hexdigest()

def scan_directory(dir):
    
    scan_results = {}
    
    # recursively iterate over directory and hash each file
    for root, _, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            scan_results[file_path] = hash_file(file_path)
                
    return scan_results
    
def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'Removed {file_path}')
    else:
        print(f'ERROR: Path not found: {file_path}')


def main():
    
    for path in dirs_to_scan:
        scan_results = scan_directory(path)
        
        for bad_hash in bad_hashes:
            if bad_hash in scan_results:
                remove_file(path)
                
                
if __name__ == '__main__':
    main()
import os
import hashlib

known_hashes = [
    "4bc8448b818a983db84f44a4fafd60c4",
    "8e5d5629672fcf8664bc28f42f79453f",
    "d35482baeab98cd49621866021e9e6fa",
    "5d80aaea305d1cb46b2e987270a3aa95"
]

dirs_to_scan = [
    '/etc', '/home', '/var', '/dev', '/bin'
]

def check_file(filepath):
    
    filehash = hashlib.md5(filepath).hexdigest()
    with open(filepath, 'rb') as file:
        for 
    
    return 
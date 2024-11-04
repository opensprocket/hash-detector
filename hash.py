import hashlib
import sys

def md5(file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

def main():
    args = sys.argv
    print(f'args: {args}')
    
    # if len(args) < 2:
    #     del args[0] # remove the calling python script
    # else: 
    #     print(f'Invalid arguments! Must provide arguments!')
    #     return
    
    result = md5(args[1])
    print(result)

if __name__ == "__main__":
    main()
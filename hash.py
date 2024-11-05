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
    # print(f'args: {args}')
    
    result = md5(args[1])
    print(result)

if __name__ == "__main__":
    main()
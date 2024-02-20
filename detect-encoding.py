import chardet
import sys

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect_encoding.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    encoding = detect_encoding(file_path)
    print(f"The file is encoded in: {encoding}")

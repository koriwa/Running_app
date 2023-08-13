import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

file_path = "database.txt"
detected_encoding = detect_encoding(file_path)
print(f"The detected encoding of 'database.txt' is: {detected_encoding}")

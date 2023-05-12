import os
import os.path
import sys


keyword = "/include/"

def getFiles(path):
    files = os.listdir(path)
    return list(filter(lambda x: x[0] != '.', files))

def gen_all_file_strings(path, files, headers, output):
    for file in files:
        components = file.split("_")
        package = f"{components[0]}:" + components[2].replace(".list", "")
        with open(path + file) as f:
            for line in f:
                if line.strip()[-1] == "/":
                    continue
                filepath = line[line.find("/"):]
                output.write(f"{package}:{filepath}")
                if filepath.startswith(keyword):
                    headers.write(f"{package}:{filepath[len(keyword):]}")

def main(path):
    try:
        os.mkdir("scripts/list_files")
    except FileExistsError:
        print("Path already exists, continuing...")

    try:
        with open("scripts/list_files/VCPKGHeadersDatabase.txt", mode='w') as headers:
            output = open("scripts/list_files/VCPKGDatabase.txt", mode='w')
            gen_all_file_strings(path, getFiles(path), headers, output)
        output.close()
    except e:
        print("Failed to generate file lists")

if __name__ == "__main__":
    main(sys.argv[1])


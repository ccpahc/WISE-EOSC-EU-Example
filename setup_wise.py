import requests
import io
import tarfile
import subprocess
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="setup_wise.py",
        description="Script to download and extract project vectors and data for a WISE deployment to the EOSC EU Node",
    )

    #parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0", help="Show program version number and exit")
    
    parser.add_argument("vectors-url", type=str, help="URL pointing to the .tar.gz file containing the pre-processed vectors")
    parser.add_argument("data-url", type=str, help="URL pointing to the .tar.gz file containing the image/video data")
    parser.add_argument("project-name", type=str, help="Name of the project (also the name of the root folder inside the vectors .tar.gz file)")

    args = parser.parse_args()

    return args

if __name__ == "__main__":

    args = parse_args()

    print("Requesting tarfiles...")

    vectors_request = requests.get(args.vectors_url)
    data_request = requests.get(args.data_url)

    if vectors_request.status_code != 200:
        print(f"Error: Vectors failed to download with code {vectors_request.status_code}")
        exit(1)
    if data_request.status_code != 200:
        print(f"Error: Data failed to download with code {data_request.status_code}")
        exit(1)

    vectors_bytes = io.BytesIO(vectors_request.content)
    data_bytes = io.BytesIO(data_request.content)

    print("Opening tarfiles...")

    vectors_tarfile = tarfile.open(mode='r:gz', fileobj=vectors_bytes)
    data_tarfile = tarfile.open(mode='r:gz', fileobj=data_bytes)

    print("Extracting tarfiles...")

    vectors_tarfile.extractall(path='/wise/projects', filter='tar')
    data_tarfile.extractall(path='/wise/data', filter='tar')

    print(f"Successfully extracted. Launching WISE for project /wise/projects/{args.project_name}...")

    subprocess.run(["python3", "serve.py", "--project-dir", f"projects/{args.project_name}"], cwd="/wise")

'''

Copyright 2026 Towards a New CCP For The Arts And Humanities
Licensed under the MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
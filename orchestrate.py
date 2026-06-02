import requests
import io
import tarfile
import subprocess
import sys
import argparse

def serve(args):
    print("Requesting vectors tarfile...")

    vectors_request = requests.get(args.vectors_url)

    if vectors_request.status_code != 200:
        print(f"Error: Vectors failed to download with code {vectors_request.status_code}")
        exit(1)
    vectors_bytes = io.BytesIO(vectors_request.content)
    print("Opening vectors tarfile...")
    vectors_tarfile = tarfile.open(mode='r:gz', fileobj=vectors_bytes)
    print("Extracting vectors tarfile...")
    vectors_tarfile.extractall(path='/wise/projects', filter='tar')

    if args.iiif:
        print("Requesting data iiif collection...")
        subprocess.run(["python3", "iiif_downloader.py", args.data_url, "/wise/data"], cwd="/")
    else:
        print("Requesting data tarfile...")
        data_request = requests.get(args.data_url)
        if data_request.status_code != 200:
            print(f"Error: Data failed to download with code {data_request.status_code}")
            exit(1)
        data_bytes = io.BytesIO(data_request.content)
        print("Opening data tarfile...")
        data_tarfile = tarfile.open(mode='r:gz', fileobj=data_bytes)
        print("Extracting data tarfile...")
        data_tarfile.extractall(path='/wise/data', filter='tar')

    print(f"Successfully downloaded and extracted. Launching WISE for project /wise/projects/{args.project_name}...")

    subprocess.run(["python3", "serve.py", "--project-dir", f"projects/{args.project_name}"], cwd="/wise")

def process(args):
    print("Not implemented yet")
    exit(0)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="setup_wise.py",
        description="Script to download and extract project vectors and data for a WISE deployment to the EOSC EU Node",
    )

    #parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0", help="Show program version number and exit")

    serve_parse = parser.add_subparser("serve", help="Retrieve processed .tar.gz files and serve them")

    serve_parse.add_argument("-i", "--iiif", action="store_true", help="If set, the data_url will be interpreted as pointing to an iiif collection instead of a .tar.gz file")

    serve_parse.add_argument("vectors_url", type=str, help="URL pointing to the .tar.gz file containing the pre-processed vectors")
    serve_parse.add_argument("data_url", type=str, help="URL pointing to the .tar.gz file containing the image/video data")
    serve_parse.add_argument("project_name", type=str, help="Name of the project (also the name of the root folder inside the vectors .tar.gz file)")

    serve_parse.set_defaults(func=serve)

    process_parse = parser.add_subparser("process_iiif", help="Download data from iiif collection and process it")

    process_parse.add_argument("iiif_url", type=str, help="URL pointing to the iiif collection in which the data is stored")
    process_parse.add_argument("project_name", type=str, help="Name of the project (also the name of the root folder inside the resulting vectors .tar.gz file)")

    process_parse.set_defaults(func=process)

    args = parser.parse_args()

    return args

if __name__ == "__main__":

    args = parse_args()
    args.func(args)


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

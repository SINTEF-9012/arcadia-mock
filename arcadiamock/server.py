
from flask import Flask

from arcadiamock import __VERSION__, __SERVICE_NAME__


import argparse



app = Flask(__name__)


@app.route("/version")
def hello():
    return 


def show_version():
    print "%s v%s" % (__SERVICE_NAME__, __VERSION__)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--version', "-v",
                        action="store_true",
                        help='show the version')
    
    args = parser.parse_args()
    if args.version:
        show_version()

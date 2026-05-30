import os
import json
import sys


def main():
    base = "task-tracker"
    for d in [f"{base}/src", f"{base}/data"]:
        os.makedirs(d, exist_ok=True)
        print(f"dir/{d}")
    pkg = f"{base}/package.json"
    if not os.path.exists(pkg):
        with open(pkg, "w") as f:
            json.dump("name": "task-tracker", "version": "1.0.0", "main": "index.js", "description": "Simple task tracking CLI", "license": "MIT"}, f, indent=2)
            f.write("\n")
        print("file/package.json")
    idx = f"{base}/index.js"
    if not os.path.exists(idx):
        with open(idx, "w") as f:
            f.write("const fs = require('fs');")
            f.write("console.log('task-tracker running');")
        print("file/index.js")
    print("setup done")


if __name__ == "__main__":
    main()

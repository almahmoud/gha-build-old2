import json
from os.path import exists
from tabulate import tabulate
with open("original.json", "r") as f:
    pkgs = json.load(f)
import requests

table = []

for pkg in list(pkgs):
    name = pkg
    runid = ""
    runurl = ""
    status = "Unclaimed"
    tarname = ""
    plog = ""
    if exists(f"logs/run_ids/{pkg}"):
        with open(f"logs/run_ids/{pkg}", "r") as frun:
            runid = frun.read()
    if "https://github.com/" in runid:
        runurl = runid.strip().replace("null\n", "")
        r = requests.get(runurl)
        if r.status_code == 404:
            runurl = runurl.replace("gha-build", "gha-build-old")
            r = requests.get(runurl)
        if r.status_code == 200:
            name = f"[{pkg}]({runurl})"
    if exists(f"lists/failed/{pkg}"):
        status = "Failed"
    elif exists(f"lists/{pkg}"):
        with open(f"lists/{pkg}", "r") as pf:
            plog = pf.read()
    if plog.endswith("tar.gz\n"):
        status = "Succeeded"
        tarname = plog.strip()
    if tarname:
        tarname = f"https://js2.jetstream-cloud.org:8001/swift/v1/gha-build/{tarname}"
    table.append([name, status, tarname])


headers = ["Package", "Status", "Tarball"]
with open("README.md", "w") as f:
    f.write(tabulate(table, headers, tablefmt="github"))

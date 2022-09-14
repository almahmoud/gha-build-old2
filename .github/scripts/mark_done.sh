#!/bin/bash
set -e
# rclone ls js2:/gha-build | grep "tar" | awk '{print $2}' > /tmp/tars
# cat /tmp/tars | awk -F'_' '{print $1}' | xargs -i bash .github/scripts/mark_done.sh {}

#cat /tmp/tars | awk -F'_' '{print $1}' | xargs -i bash -c 'grep "^{}_" /tmp/tars | head -n1 > lists/{}'

PKGTOMARK=$1

sed -i "s/    \"$PKGTOMARK\": \[\],\?//g" packages.json
sed -i "s/        \"$PKGTOMARK\",\?//g" packages.json
sed -i -z 's/,\n\n\+}/}/g' packages.json
sed -i -z 's/,\n\n\+ *]/]/g' packages.json
python -c 'import json; f = open("packages.json", "r"); pkgs = json.load(f); f.close(); f = open("packages.json", "w"); f.write(json.dumps(pkgs, indent=4)); f.close()'

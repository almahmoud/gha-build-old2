#!/bin/bash
set -xe
git pull origin main || git reset --hard origin/main

PKG=$1
sed -i 's/claimed/built/g' "lists/$PKG"
git add lists
#cp /tmp/tars/*.tar.gz tars/
mkdir -p logs/
cp /tmp/logs/*.out logs/
#git add tars
git add logs
#git add built
git commit -m "Built $PKG"
git push

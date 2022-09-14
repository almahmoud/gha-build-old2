#!/bin/bash
set -xe
git pull origin main || git reset --hard origin/main
LIBRARY=$1
PKG=$2
mkdir -p $LIBRARY
mkdir -p /tmp/tars/
mkdir -p /tmp/logs/
sed -n "/^    \"$PKG\"/,/^    \"/p" original.json | grep '^        "' | awk -F'"' '{print $2}' | xargs -i cat lists/{} | xargs -i bash -c "curl -o $LIBRARY/{} https://js2.jetstream-cloud.org:8001/swift/v1/gha-build/{}"
( cd $LIBRARY && ls | grep ".tar.gz" | xargs -i tar -xvf {} )
if git clone git@git.bioconductor.org:packages/$PKG
then
	Rscript -e "p <- .libPaths(); p <- c('$LIBRARY', p); .libPaths(p); if(BiocManager::install('./$PKG', INSTALL_opts = '--build', update = TRUE, quiet = FALSE, force = TRUE, keep_outputs = TRUE) %in% rownames(installed.packages())) q(status = 0) else q(status = 1)"
else
	Rscript -e "Sys.setenv(BIOCONDUCTOR_USE_CONTAINER_REPOSITORY=FALSE); p <- .libPaths(); p <- c('$LIBRARY', p); .libPaths(p); if(BiocManager::install('$PKG', INSTALL_opts = '--build', update = TRUE, quiet = FALSE, force = TRUE, keep_outputs = TRUE) %in% rownames(installed.packages())) q(status = 0) else q(status = 1)"
fi
cp *.tar.gz /tmp/tars/
cp *.out /tmp/logs/

#!/bin/bash

#https://github.com/Microsoft/PowerBI-Cli/issues/5
pushd /usr/lib/node_modules/powerbi-cli/bin/
for f in cli-*; do mv "$f" "`echo $f | sed s/cli-/powerbi-/`"; done
chmod +x powerbi-*
popd

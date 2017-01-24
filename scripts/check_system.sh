#!/bin/bash

set -e

# Confirm that the pcp mapping file is correct
echo 'f3616ce9450408c9458e8b0292402a6e  /usr/share/xdmod/etl/js/config/supremm/dataset_maps/pcp.js' | md5sum --check

# Check the etl version number
grep 'var *version' /usr/share/xdmod/etl/js/config/supremm/etl.profile.js

# output the contents of the supremm configuration file
cat /etc/xdmod/supremm_resources.json

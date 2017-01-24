#!/bin/bash

set -e

# Edit the supremm resources file and reset dataset mapping
sed -i 's/"datasetmap": "pcp"/"datasetmap": "ganglia-pcp"/' /etc/xdmod/supremm_resources.json

# Switch the schema file
cd /usr/share/xdmod/etl/js/config/supremm
mv etl.schema.js etl.schema.js.orig
cp etl.schema.ncar.js etl.schema.js

# Update the instance
cd /usr/share/xdmod/etl/js
node etl.cli.js -a

# Output the various files
md5sum /usr/share/xdmod/etl/js/config/supremm/etl.schema*
md5sum /etc/xdmod/aggregation_meta/modw_aggregates.supremmfact_aggregation_meta.json
cat /etc/xdmod/supremm_resources.json

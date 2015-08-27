#!/usr/bin/env bash

set -xe

chmod 600 filea.txt

export creator=$(git --no-pager show -s --format='%ae' ${TRAVIS_COMMIT})
export creation_time=`date +"%Y%m%d%H%M%S"`
export appversion="0.0.${TRAVIS_BUILD_ID}"
export ec2_source_ami=ami-a10897d6

ssh -i filea.txt -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no packer@52.19.153.94 \
"packer build packer/build.json"
 
#packer -machine-readable build    packer/build.json | tee output.txt
#tail -2 output.txt | head -2 | awk 'match($0, /ami-.*/) { print substr($0, RSTART, RLENGTH) }' >  ami.txt

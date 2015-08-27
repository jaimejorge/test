#!/bin/bash

set -e
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
app="bank_${TRAVIS_BRANCH//./_}"
app="bank_master"


. ${DIR}/functions.sh
. ${DIR}/params.sh

echo creating app in $domain

exist  application ${app} && echo app ${app} already exist || create application ${appParams}
getNextVersion ${app} && deploy ${app} || create autoScaling ${autoScalingParams}

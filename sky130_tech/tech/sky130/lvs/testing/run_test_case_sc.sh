#!/bin/bash -f

export CASE_NAME=$1
export PDK_ROOT=`readlink -f $2`
export PDK=$3
export TESTCASES_DIR=`readlink -f $4`
export RUN_FOLDER=`readlink -f $5`

echo "## Running test case for $CASE_NAME"
echo "PDK_ROOT = $PDK_ROOT and PDK = $PDK"

## hd cells
hd_gds=$TESTCASES_DIR/hd/${CASE_NAME}.gds
hd_cdl=$TESTCASES_DIR/hd/${CASE_NAME}.cdl

if [ -f $hd_gds ]
then
    if [ -f $hd_cdl ]
    then
        python3 $PDK_ROOT/$PDK/run_lvs.py --design=$hd_gds --net=$hd_cdl --output_netlist=$RUN_FOLDER/${CASE_NAME}_pass_ext.cir --report=$RUN_FOLDER/${CASE_NAME}_pass > $RUN_FOLDER/${CASE_NAME}_pass_lvs.log 2>&1
        return_code=$?
        if [ "$return_code" != "0" ]
        then
            echo "## Pass test case $CASE_NAME didn't pass as expected."
            echo "## $CASE_NAME XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX."
            # exit 1
        else
            echo "## Pass test case $CASE_NAME passed successfully."
        fi
    else
        echo "## Can't find pass CDL for case: $hd_cdl"
        exit 1
    fi
else
    echo "## Can't find pass GDS for case: $hd_gds"
    exit 1
fi
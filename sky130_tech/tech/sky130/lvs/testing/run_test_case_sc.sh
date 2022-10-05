#!/bin/bash -f

export CASE_NAME=$1
export PDK_ROOT=`readlink -f $2`
export PDK=$3
export TESTCASES_DIR=`readlink -f $4`
export RUN_FOLDER=`readlink -f $5`
export LIB=$6
export GND=$7

echo "## Running test case for $CASE_NAME"
echo "PDK_ROOT = $PDK_ROOT and PDK = $PDK"

## Lib cells
gds_file=${TESTCASES_DIR}/${LIB}/${CASE_NAME}.gds
cdl_file=${TESTCASES_DIR}/${LIB}/${CASE_NAME}.cdl

if [ -f $gds_file ]
then
    if [ -f $cdl_file ]
    then
        python3 $PDK_ROOT/$PDK/run_lvs.py --design=$gds_file --net=$cdl_file --output_netlist=$RUN_FOLDER/${CASE_NAME}_pass_ext.cir --report=$RUN_FOLDER/${CASE_NAME}_pass --lvs_sub=${GND-sky130_gnd} > $RUN_FOLDER/${CASE_NAME}_pass_lvs.log 2>&1
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
        echo "## Can't find pass CDL for case: $cdl_file"
        exit 1
    fi
else
    echo "## Can't find pass GDS for case: $gds_file"
    exit 1
fi
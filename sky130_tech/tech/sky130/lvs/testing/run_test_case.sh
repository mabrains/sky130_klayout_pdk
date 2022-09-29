#!/bin/bash -f

export CASE_NAME=$1
export PDK_ROOT=`readlink -f $2`
export PDK=$3
export TESTCASES_DIR=`readlink -f $4`
export RUN_FOLDER=`readlink -f $5`

echo "## Running test case for $CASE_NAME"
echo "PDK_ROOT = $PDK_ROOT and PDK = $PDK"

pass_gds=$TESTCASES_DIR/pass_cases/${CASE_NAME}.gds
pass_cdl=$TESTCASES_DIR/pass_cases/${CASE_NAME}.cdl

fail_dim_gds=$TESTCASES_DIR/fail_cases/${CASE_NAME}_dim_fail.gds
fail_dim_cdl=$TESTCASES_DIR/fail_cases/${CASE_NAME}_dim_fail.cdl

fail_lay_gds=$TESTCASES_DIR/fail_cases/${CASE_NAME}_lyr_fail.gds
fail_lay_cdl=$TESTCASES_DIR/fail_cases/${CASE_NAME}_lyr_fail.cdl

fail_net_gds=$TESTCASES_DIR/fail_cases/${CASE_NAME}_net_fail.gds
fail_net_cdl=$TESTCASES_DIR/fail_cases/${CASE_NAME}_net_fail.cdl


if [ -f $pass_gds ]
then
    if [ -f $pass_cdl ]
    then
        python3 $PDK_ROOT/$PDK/run_lvs.py --design=$pass_gds --net=$pass_cdl --output_netlist=$RUN_FOLDER/${CASE_NAME}_pass_ext.cir --report=$RUN_FOLDER/${CASE_NAME}_pass > $RUN_FOLDER/${CASE_NAME}_pass_lvs.log 2>&1
        return_code=$?
        if [ "$return_code" != "0" ]
        then
            echo "## Pass test case $CASE_NAME didn't pass as expected."
            exit 1
        else
            echo "## Pass test case $CASE_NAME passed successfully."
        fi
    else
        echo "## Can't find pass CDL for case: $pass_cdl"
        exit 1
    fi
else
    echo "## Can't find pass GDS for case: $pass_gds"
    exit 1
fi


if [ -f $fail_dim_gds ]
then
    if [ -f $fail_dim_cdl ]
    then
        python3 $PDK_ROOT/$PDK/run_lvs.py --design=$fail_dim_gds --net=$fail_dim_cdl --output_netlist=$RUN_FOLDER/${CASE_NAME}_fail_dim_ext.cir --report=$RUN_FOLDER/${CASE_NAME}_fail_dim > $RUN_FOLDER/${CASE_NAME}_fail_dim_lvs.log 2>&1
        return_code=$?
        if [ "$return_code" != "1" ]
        then
            echo "## Fail dimension test case $CASE_NAME didn't fail as expected."
            exit 1
        else
            echo "## Fail dimension test case $CASE_NAME failed as expected."
        fi
    else
        echo "## Can't find fail dimension CDL for case: $fail_dim_cdl"
        exit 1
    fi
else
    echo "## Can't find fail dimension GDS for case: $fail_dim_gds"
    exit 1
fi

if [ -f $fail_lay_gds ]
then
    if [ -f $fail_lay_cdl ]
    then
        python3 $PDK_ROOT/$PDK/run_lvs.py --design=$fail_lay_gds --net=$fail_lay_cdl --output_netlist=$RUN_FOLDER/${CASE_NAME}_fail_lay_ext.cir --report=$RUN_FOLDER/${CASE_NAME}_fail_lay > $RUN_FOLDER/${CASE_NAME}_fail_lay_lvs.log 2>&1
        return_code=$?
        if [ "$return_code" != "1" ]
        then
            echo "## Fail layer test case $CASE_NAME didn't fail as expected."
            exit 1
        else
            echo "## Fail layer test case $CASE_NAME failed as expected."
        fi
    else
        echo "## Can't find fail layer for case: $fail_lay_cdl"
        exit 1
    fi
else
    echo "## Can't find fail layer GDS for case: $fail_lay_gds"
    exit 1
fi

if [ -f $fail_net_gds ]
then
    if [ -f $fail_net_cdl ]
    then
        python3 $PDK_ROOT/$PDK/run_lvs.py --design=$fail_net_gds --net=$fail_net_cdl --output_netlist=$RUN_FOLDER/${CASE_NAME}_fail_net_ext.cir --report=$RUN_FOLDER/${CASE_NAME}_fail_net > $RUN_FOLDER/${CASE_NAME}_fail_net_lvs.log 2>&1
        return_code=$?
        if [ "$return_code" != "1" ]
        then
            echo "## Fail netlist test case $CASE_NAME didn't fail as expected."
            exit 1
        else
            echo "## Fail netlist test case $CASE_NAME failed as expected."
        fi
    else
        echo "## Can't find fail netlist CDL for case: $fail_net_cdl"
        exit 1
    fi
else
    echo "## Can't find fail netlist GDS for case: $fail_net_gds"
    exit 1
fi


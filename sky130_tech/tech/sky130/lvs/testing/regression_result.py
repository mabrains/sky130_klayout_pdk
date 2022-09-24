# Copyright 2022 Mabrains
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Run Skywater 130nm LVS regression results.

Usage: 
    regression_result.py (--help| -h)
    regression_result.py (--db=<db_path>) 

Options:
    --help -h                   Print this help message.
    --db=<db_path>              The result database path.
"""
import logging
from docopt import docopt
import os

def Sort(sub_li):
    sub_li.sort(key = lambda x: x[0])
    return sub_li

def main():

    results_table   = []
    circuits_table  = []

    netlist         = False
    compare         = False

    with open(args["--db"], 'r') as f:
        for line in f:
            if "H(" in line:
                netlist = True
            if "Z(" in line:
                compare = True
                netlist = False
            if netlist:
                if "D(" in line:
                    device_num = line.replace("  D(", "").strip("\n").split(" ")[0]
                if "   I(" in line:
                    if "FAIL" not in line:
                        circuits_table.append([device_num,"1"])
                    else:
                        circuits_table.append([device_num,"0"])
            if compare:
                if "D(" in line:
                    results_table.append(line.replace("   D(", "").strip(")\n").split(" ")[1:])

    results_table = [[int(x) for x in lst if x != '()'] for lst in results_table]
    circuits_table = [[int(x) for x in lst if x != '()'] for lst in circuits_table]

    results_table = Sort([subl for subl in results_table if subl[0] != 0])

    if (results_table == circuits_table) or ( results_table == [] and "fail" in args["--db"] ):
        logging.info("===================================================")
        logging.info("Congratualtions! All cases have passed successfully")
        logging.info("===================================================")
    else:
        for i, check in enumerate(results_table):
            if int(circuits_table[i][1]) > int(check[1]):
                logging.error('Error: Found false postive case')
            elif int(circuits_table[i][1]) < int(check[1]):
                logging.error('Error: Found false negative case')
            else:
                logging.error(f"Device number {check[0]} has matched")

        raise ValueError('Error: Found cases did not behave as expected')


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s | %(levelname)-7s | %(message)s", datefmt='%d-%b-%Y %H:%M:%S')

    # Args 
    args          = docopt(__doc__, version='LVS Checker: 0.1')
    
    # Env. variables
    if os.environ.get('PDK_ROOT') is not None:
        ## if PDK_ROOT is defined, we assume that PDK is defined as well. Will error out if PDK_ROOT only is defined.
        pdk_root = os.environ['PDK_ROOT']
        pdk      = os.environ['PDK']
    else:
        pdk_full_path = os.path.dirname(os.path.abspath(__file__))
        pdk_root = os.path.dirname(pdk_full_path) 
        pdk      = os.path.basename(pdk_full_path)

    # ========= Checking Klayout version =========
    klayout_v_ = os.popen("klayout -v").read()
    klayout_v_ = klayout_v_.split("\n")[0]
    klayout_v  = int (klayout_v_.split(".") [-1])
        
    if klayout_v < 8:
        logging.warning("Using this klayout version has not been assesed in this development. Limits are unknown")    
        logging.info(f"Your version is: {klayout_v_}"  )
        logging.info(f"Prerequisites at a minimum: KLayout 0.27.8")

    # Calling main function 
    main()

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


"""Run Skywater 130nm LVS.

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
            if "lyr_fail" in line:
                raise ValueError('Error: Found false negative case')
            if "H(" in line:
                netlist = True
            if "Z(" in line:
                compare = True
                netlist = False
            if netlist:
                if "D(" in line:
                    device_num = line.replace("  D(", "").strip("\n").split(" ")[0]
                if "   I(" in line:
                    if "fail" not in line:
                        circuits_table.append([device_num,"1"])
                    else:
                        circuits_table.append([device_num,"0"])
            if compare:
                if "D(" in line:
                    results_table.append(line.replace("   D(", "").strip(")\n").split(" ")[1:])

    results_table = Sort([subl for subl in results_table if subl[0] != '()'])

    if results_table == circuits_table:
        logging.info("Congratualtions! All cases have passed successfully")
    else:
        for i, check in enumerate(results_table):
            if int(circuits_table[i][1]) > int(check[1]):
                logging.error('Error: Found false postive case')
                raise ValueError('Error: Found false postive case')
            elif int(circuits_table[i][1]) < int(check[1]):
                logging.error('Error: Found false negative case')
                raise ValueError('Error: Found false negative case')
            else:
                logging.info(f"Device number {check[0]} has passed")


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s | %(levelname)-7s | %(message)s", datefmt='%d-%b-%Y %H:%M:%S')

    # Args 
    args          = docopt(__doc__, version='LVS Checker: 0.1')
    
    # Env. variables
    pdk_root = os.environ['PDK_ROOT']
    pdk      = os.environ['PDK']

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

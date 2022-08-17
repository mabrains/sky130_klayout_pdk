########################################################################################################################
##
# Mabrains Company LLC ("Mabrains Company LLC") CONFIDENTIAL
##
# Copyright (C) 2018-2022 Mabrains Company LLC <contact@mabrains.com>
##
# This file is authored by:
#           - <Mohanad Mohamed> <mohanad_mohamed@mabrains.com>
##
# This code is provided solely for Mabrains use and can not be sold or reused for any other purpose by
# any person or entity without prior authorization from Mabrains.
##
# NOTICE:  All information contained herein is, and remains the property of Mabrains Company LLC.
# The intellectual and technical concepts contained herein are proprietary to Mabrains Company LLC
# and may be covered by U.S. and Foreign Patents, patents in process, and are protected by
# trade secret or copyright law.
# Dissemination of this information or reproduction of this material is strictly forbidden
# unless prior written permission is obtained
# from Mabrains Company LLC.  Access to the source code contained herein is hereby forbidden to anyone except current
# Mabrains Company LLC employees, managers or contractors who have executed Confidentiality and Non-disclosure
# agreements explicitly covering such access.
#
##
# The copyright notice above does not evidence any actual or intended publication or disclosure
# of  this source code, which includes
# information that is confidential and/or proprietary, and is a trade secret, of  Mabrains Company LLC.
# ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC  PERFORMANCE, OR PUBLIC DISPLAY OF OR THROUGH USE
# OF THIS  SOURCE CODE  WITHOUT THE EXPRESS WRITTEN CONSENT OF Mabrains Company LLC IS STRICTLY PROHIBITED,
# AND IN VIOLATION OF APPLICABLE LAWS AND INTERNATIONAL TREATIES.  THE RECEIPT OR POSSESSION OF  THIS SOURCE CODE
# AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS,
# OR TO MANUFACTURE, USE, OR SELL ANYTHING THAT IT  MAY DESCRIBE, IN WHOLE OR IN PART.
##
# Mabrains retains the full rights for the software which includes the following but not limited to: right to sell,
# resell, repackage, distribute, creating a Mabrains Company LLC using that code, use, reuse or modify the code created.
##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL
# MABRAINS COMPANY LLC OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT,TORT OR OTHERWISE, ARISING FROM
# , OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# MABRAINS COMPANY LLC DOES NOT HOLD ANY RESPONSIBILITIES THAT MIGHT RISE DUE TO LOSE OF MONEY OR DIGITAL ASSETS USING
# THIS SOFTWARE AND IT IS SOLELY THE RESPONSIBILITY OF THE SOFTWARE USER.
#
# This banner can not be removed by anyone other than Mabrains Company LLC.
##
########################################################################################################################

########################################################################################################################
## Mabrains Company LLC
##
## Mabrains LVS Rule Deck runner script for Skywater 130nm
########################################################################################################################


"""Run Skywater 130nm LVS.

Usage:
    run_lvs.py (--help| -h)
    run_lvs.py (--design=<layout_path>) (--net=<netlist_path>) [--thr=<thr>] [--run_mode=<run_mode>] [--lvs_sub=<sub_name>] [--no_net_names] [--set_spice_comments] [--set_scale] [--set_verbose] [--set_schematic_simplify] [--set_net_only] [--set_top_lvl_pins] [--set_combine] [--set_purge] [--set_purge_nets]

Options:
    --help -h                           Print this help message.
    --design=<layout_path>              The input GDS file path.
    --net=<netlist_path>                The input netlist file path.
    --thr=<thr>                         Number of cores to be used by LVS checker
    --run_mode=<run_mode>               Select klayout mode Allowed modes (flat , deep, tiling). [default: deep]
    --lvs_sub=<sub_name>                Assign the substrate name used in design.
    --no_net_names                      Discard net names in extracted netlist.
    --set_spice_comments                Set netlist comments in extracted netlist.
    --set_scale                         Set scale of 1e6 in extracted netlist.
    --set_verbose                       Set verbose mode.
    --set_schematic_simplify            Set schematic simplification in input netlist.
    --set_net_only                      Set netlist object creation only in extracted netlist.
    --set_top_lvl_pins                  Set top level pins only in extracted netlist.
    --set_combine                       Set netlist combine only in extracted netlist.
    --set_purge                         Set netlist purge all only in extracted netlist.
    --set_purge_nets                    Set netlist purge nets only in extracted netlist.
"""

from docopt import docopt
import os
import logging

def main():

    # Switches used in run
    switches = ''

    if args["--run_mode"] in ["flat" , "deep", "tiling"]:
        switches = switches + f'-rd run_mode={args["--run_mode"]} '
    else:
        logging.error("Allowed klayout modes are (flat , deep , tiling) only")
        exit()

    switches = switches + '-rd spice_net_names=false ' if args["--no_net_names"] else switches + '-rd spice_net_names=true '

    switches = switches + '-rd spice_comments=true ' if args["--set_spice_comments"] else switches + '-rd spice_comments=false '

    switches = switches + '-rd scale=true ' if args["--set_scale"] else switches + '-rd scale=false '

    switches = switches + '-rd verbose=true ' if args["--set_verbose"] else switches + '-rd verbose=false '

    switches = switches + '-rd schematic_simplify=true ' if args["--set_schematic_simplify"] else switches + '-rd schematic_simplify=false '

    switches = switches + '-rd net_only=true ' if args["--set_net_only"] else switches + '-rd net_only=false '

    switches = switches + '-rd top_lvl_pins=true ' if args["--set_top_lvl_pins"] else switches + '-rd top_lvl_pins=false '

    switches = switches + '-rd combine=true ' if args["--set_combine"] else switches + '-rd combine=false '

    switches = switches + '-rd purge=true ' if args["--set_purge"] else switches + '-rd purge=false '

    switches = switches + '-rd purge_nets=true ' if args["--set_purge_nets"] else switches + '-rd purge_nets=false '

    switches = switches + f'-rd lvs_sub={args["--lvs_sub"]} ' if args["--lvs_sub"] else switches


    # Generate databases
    if args["--design"]:
        path = args["--design"]
        if args["--design"]:
            file_name = args["--net"].split('.')
        else:
            print("The script must be given a netlist file or a path to be able to run LVS")
            exit()

        os.system(f"klayout -b -r sky130.lvs -rd input={path} -rd report={file_name[0]}.lyrdb -rd schematic={args['--net']} -rd target_netlist=extracted_netlist_{file_name[0]}.cir -rd thr={workers_count} {switches}")

    else:
        print("The script must be given a layout file or a path to be able to run LVS")
        exit()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s | %(levelname)-7s | %(message)s", datefmt='%d-%b-%Y %H:%M:%S')

    # Args
    args          = docopt(__doc__, version='LVS Checker: 0.1')
    workers_count = os.cpu_count()*2 if args["--thr"] == None else int(args["--thr"])

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

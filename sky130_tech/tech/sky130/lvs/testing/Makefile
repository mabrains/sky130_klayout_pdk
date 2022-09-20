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

#=========================================================================
# ---------------------------------- LVS ---------------------------------
#=========================================================================

SHELL        := /bin/bash
Testing_DIR  ?= $(shell pwd)
run_folder    = $(shell date +'run_%Y_%m_%d_%H_%M')

.DEFAULT_GOAL := all

all: test_lvs_main test_lvs_collective test_lvs_connectivity

#=================================
# -------- TEST MAIN LVS ---------
#=================================

.ONESHELL:
test_lvs_main_gha_%:
	@cd $(Testing_DIR)
	@file=`find . -iname $*.gds`
	@net="$${file//'./testcases/'/}"; net="$${net//fixed_devices/}";
	@if python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=$$file --net=$${net//.gds/.cdl} ; then exit 0; \
		else python3 regression_result.py --db=$${file//.gds/.lvsdb} ; fi
#	@if python3 run_lvs.py --design=$${file//.gds/_dim_fail.gds} --net=$${net//.gds/_dim_fail.cdl} ; then exit 1; \
#		else python3 regression_result.py --db=$${file//.gds/_dim_fail.lvsdb} ; fi
#	@if python3 run_lvs.py --design=$${file//.gds/_lyr_fail.gds} --net=$${net//.gds/_lyr_fail.cdl} ; then exit 1; \
#		else python3 regression_result.py --db=$${file//.gds/_lyr_fail.lvsdb} ; fi
#	@if python3 run_lvs.py --design=$${file//.gds/_net_fail.gds} --net=$${net//.gds/_net_fail.cdl} ; then exit 1; \
#		else python3 regression_result.py --db=$${file//.gds/_net_fail.lvsdb} ; fi

.ONESHELL:
test_lvs_main: 
	@cd $(Testing_DIR)/..
	@mkdir -p testing/$(run_folder)
	@search_dir=`ls testing/testcases/*.gds testing/testcases/fixed_devices/*.gds`
	@for file in $$search_dir ; do cdl="$${file//'testing/testcases/'/}"; cdl="$${cdl//'fixed_devices/'/}"; \
	if python3 run_lvs.py --design=$$file --net=$${cdl//.gds/.cdl}  |& tee -a testing/$(run_folder)/main_results.log ; then continue; \
		else python3 regression_result.py --db=$${file//.gds/.lvsdb} ; fi; done
	@echo "Congratulations! Testing main lvs is finished successfully"

#=================================
# ----- TEST COLLECTIVE LVS ------
#=================================

.ONESHELL:
test_lvs_collective: 
	@cd $(Testing_DIR)
	@mkdir -p $(run_folder)
	@search_dir=`ls collective_test/*.gds`
	@for file in $$search_dir ; do cdl="$${file//collective_test/}"; \
	python3 ../run_lvs.py --design=$$file --net=$${cdl//.gds/.cdl}  |& tee -a $(run_folder)/collective_results.log  ; done
	@echo "Congratulations! Testing collective lvs is finished successfully"

#=================================
# ---- TEST CONNECTIVITY LVS -----
#=================================

.ONESHELL:
test_lvs_connectivity: 
	@cd $(Testing_DIR)
	@mkdir -p $(run_folder)
	@search_dir=`ls connectivity_test/*.gds`
	@for file in $$search_dir ; do cdl="$${file//connectivity_test/}"; \
	python3 ../run_lvs.py --design=$$file --net=$${cdl//.gds/.cdl}  |& tee -a $(run_folder)/connectivity_results.log  ; done
	@echo "Congratulations! Testing connectivity lvs is finished successfully"

#==========================
# --------- HELP ----------
#==========================

# Help Target
help:
	@echo "\n ==== The following are some of the valid targets for this Makefile ====\n"
	@echo "... all                  	(the default if no target is provided          		)"
	@echo "... test_lvs_main        	(To run main lvs regression for all devices    		)"
	@echo "... test_lvs_collective  	(To run collective lvs regression for all devices	)"
	@echo "... test_lvs_connectivity    (To run connectivity lvs regression for all devices	)"
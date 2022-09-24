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
Testing_DIR  ?= $(shell realpath .)
PDK_ROOT     ?= $(shell realpath ../..)
PDK          ?= $(shell basename `realpath ..`)
run_folder   := $(shell realpath $$(date +'run_%Y_%m_%d_%H_%M'))
CASES 		 := $(wildcard testcases/*pfet*.cdl)
CASES		 += $(wildcard testcases/fixed_devices/*.cdl)
MAIN		 := $(CASES:testcases/%=%)
MID_CASES	 := $(MAIN:fixed_devices/%.cdl=test_lvs_main_gha_%)
CASES	 	 := $(MID_CASES:%.cdl=test_lvs_main_gha_%)
CONN_CASES	 := $(wildcard connectivity_test/*.gds)

.DEFAULT_GOAL := all

all: test_lvs_main test_lvs_collective test_lvs_connectivity

#=================================
# -------- TEST MAIN LVS ---------
#=================================
.ONESHELL:
$(run_folder):
	@echo "## Our current Run folder: $(run_folder)"
	@mkdir -p $(run_folder)

.ONESHELL:
test_lvs_main_gha_%:
	@echo "## Running test case for $*"
	@echo "PDK_ROOT = $(PDK_ROOT) and PDK = $(PDK)"
	@cd $(Testing_DIR)
	@file=`find . -iname $*.gds`
	@net="$${file//'./testcases/'/}"; net="$${net//'fixed_devices/'/}";
	@if python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=$$file --net=$${net//.gds/.cdl} --report=$(run_folder)/$* > $(run_folder)/$*_pass_lvs.log 2>&1 ; then echo PASS CASE MATCHED; \
		else python3 regression_result.py --db=$${file//.gds/.lvsdb} ; exit 1; fi;
	@file="$${file//'./testcases/'/'./fail_cases/'}";
	@if python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=$${file//.gds/_dim_fail.gds} --net=$${net//.gds/_dim_fail.cdl} --report=$(run_folder)/$* > $(run_folder)/$*_fail_dim_lvs.log 2>&1 ; then exit 1; \
		else python3 regression_result.py --db=$${file//.gds/_dim_fail.lvsdb} ; fi
	@if python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=$${file//.gds/_lyr_fail.gds} --net=$${net//.gds/_lyr_fail.cdl} --report=$(run_folder)/$* > $(run_folder)/$*_fail_layer_lvs.log 2>&1 ; then exit 1; \
		else python3 regression_result.py --db=$${file//.gds/_lyr_fail.lvsdb} ; fi
	@if python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=$${file//.gds/_net_fail.gds} --net=$${net//.gds/_net_fail.cdl} --report=$(run_folder)/$* > $(run_folder)/$*_fail_layer_lvs.log 2>&1 ; then exit 1; \
		else python3 regression_result.py --db=$${file//.gds/_net_fail.lvsdb} ; fi

.ONESHELL:
test_lvs_main: $(run_folder)
	@$(MAKE) run_all_test_cases

.ONESHELL:
run_all_test_cases: $(CASES)
	@echo "Congratulations! Testing main LVS is finished successfully"

#=================================
# ----- TEST COLLECTIVE LVS ------
#=================================

.ONESHELL:
test_lvs_collective: 
	@cd $(Testing_DIR)
	@python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=collective_test/collective.gds --net=collective.cdl |& tee -a $(run_folder)/collective_results.log
	@echo "Congratulations! Testing collective LVS is finished successfully"

#=================================
# ---- TEST CONNECTIVITY LVS -----
#=================================

.ONESHELL:
connectivity_test/% : $(PDK_ROOT)/$(PDK)/run_lvs.py
	@cd $(Testing_DIR)
	@mkdir -p $(run_folder)/connectivity_test
	@file="$@"
	@cdl="$${file//'connectivity_test/'/}";
	@python3 $< --design=$$file --net=$${cdl//.gds/.cdl}  |& tee $(run_folder)/connectivity_test/$${cdl//.gds/.log}

.ONESHELL:
test_lvs_connectivity: $(CONN_CASES)
	@echo "Congratulations! Testing connectivity LVS is finished successfully"

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

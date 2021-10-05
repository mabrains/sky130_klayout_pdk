########################################################################################################################
##
# Mabrains Company LLC ("Mabrains Company LLC") CONFIDENTIAL
##
# Copyright (C) 2018-2021 Mabrains Company LLC <contact@mabrains.com>
##
# This file is authored by:
#           - <Mina Maksimous> <mina_maksimous@mabrains.com>
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


import pya
import generators.klayout.nmos18 as nmos
from generators.klayout.layers_definiations import *
import os
repo_path = os.environ['automation_repo']
gds_path = repo_path+"/generators/klayout/"
class bjt(nmos.nmos18_device):
    
    n_well_diffusion_spacing = 0.34
    tap_width = 0.26

    def __init__(self, layout, device_name,guard_ring = 1):
        self.layout = layout
        self.device_name = device_name
        self.percision = 1/layout.dbu
        self.l_guard = self.layout.layer(
            psdm_lay_num, psdm_lay_dt)

        self.gr = guard_ring

    def add_labels (self):
        pass

    

    def draw_bjt(self):
        if self.device_name == "npn_w1_l1":
            self.layout.read(gds_path+self.device_name+".gds")
            self.cell_name = "sky130_fd_pr__rf_npn_05v5_W1p00L1p00"
        elif self.device_name == "npn_w1_l2":
            self.layout.read(gds_path+self.device_name+".gds")
            self.cell_name = "sky130_fd_pr__rf_npn_05v5_W1p00L2p00"

        enlarge_value = int((bjt.n_well_diffusion_spacing +
                         bjt.tap_width/2)*self.percision)
        self.bjt_bbox = self.layout.cell(self.cell_name).bbox().enlarge(enlarge_value,enlarge_value)
        # print('--->',(self.bjt_bbox.p1.x-1000*enlarge_value)/self.percision)
        # print('--->',self.bjt_bbox.p1.x-1*enlarge_value)
        if self.gr:
            self.draw_guard_ring(layout=self.layout,
                                x=(self.bjt_bbox.p1.x),
                                y=(self.bjt_bbox.p1.y),
                                guard_width=self.bjt_bbox.width()/self.percision,
                                guard_height=self.bjt_bbox.height()/self.percision,
                                tap_width=bjt.tap_width, cell=self.layout.cell(self.cell_name),
                                precision=self.percision)

        return self.layout.cell(self.cell_name)



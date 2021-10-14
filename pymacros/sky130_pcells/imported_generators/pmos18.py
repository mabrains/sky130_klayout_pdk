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

########################################################################################################################
# Mabrains Company LLC
##
# Mabrains PMOS 1.8V Generator for Skywaters 130nm
########################################################################################################################

from .nmos18 import *


class pmos18_device(nmos18_device):
    

    def __init__(self, w=0.42, l=0, nf=1, gr=1,
                 dsa=2,
                 connection=0,
                 n=1,
                 x_offest=0,
                 y_offest=0,
                 conn_num=0,
                 gate_connection="gate_connection_",
                 gate_connection_up="gate_connection_up_",
                 gate_connection_down="gate_connection_down_",
                 drain_connection="drain_connection_",
                 source_connection="source_connection_",
                 connection_labels=1,
                 connected_gates=1,
                 layout=None):
        super().__init__(w=w, l=l, nf=nf, gr=gr, dsa=dsa, connection=connection, 
                        n=n, x_offest=x_offest, y_offest=y_offest, conn_num=conn_num, 
                        gate_connection=gate_connection,
                        gate_connection_up=gate_connection_up, gate_connection_down=gate_connection_down, drain_connection=drain_connection, 
                        source_connection=source_connection, layout=layout,connection_labels=connection_labels,connected_gates=connected_gates)

        self.layout = layout
        self.percision = 1/self.layout.dbu
        self.l_diff_implant = self.layout.layer(psdm_lay_num, psdm_lay_dt)
        self.l_guard = self.layout.layer(
            nsdm_lay_num, nsdm_lay_dt)  # guard ring implant layer
        self.cell_str = "pmos18_w" + str(self.w).replace(".", "p") + "u_l" + str(self.l).replace(".", "p") + "u_nf" + str(
            self.nf) + "_drain_area" + str(self.dsa) + "_gate_connection" + str(self.connection) + "alt" + str(self.n)
        self.l_nwell = self.layout.layer(nwell_lay_num, nwell_lay_dt)
        self.nwell_extension = 0.18 * self.percision
    # def draw_guard_ring(self, layout, x, y, guard_width, guard_height, precision, tap_width=0.26, cell=None, type='n'):
    #     return super().draw_guard_ring(layout, x, y, guard_width, guard_height, precision, tap_width=tap_width, cell=cell, type=type)

    def draw_nmos(self):
        self.pmos_cell = super().draw_nmos()
        self.pmos_cell.shapes(self.l_nwell).insert(
            self.pmos_cell.bbox().enlarge(self.nwell_extension, self.nwell_extension))
        return self.pmos_cell

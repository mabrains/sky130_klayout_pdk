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
from .layers_definiations import *
import pya


class mimcap():
    mimcap_drawing_offest = 0.5
    metal3_margin_right = 0.995
    mimcap_enc_metal4 = 0.195
    met4_side_overlap = 0.005
    met4_side_width = 0.48

    def number_spc_contacts(self, box_width, min_enc, cont_spc, cont_width):
        """ Calculate number of cantacts in a given dimensions and the free space for symmetry.

            By getting the min enclosure,the width of the box,the width of the cont. or via
            and the spacing between cont. or via

            Parameters
            ----------
            box_width : double
                The length you place the via or cont. in

            min_enc : double
                the spacing between the edge of the box and the first via or cont.

            cont_spc : double
                the spacing between different via's or cont

            cont_width: double
                the cont. or via width in the same direction

        """

        spc_cont = box_width - 2 * min_enc
        num_cont = int((spc_cont + cont_spc) / (cont_width + cont_spc))
        free_spc = box_width - (num_cont * cont_width +
                                (num_cont - 1) * cont_spc)
        return num_cont, free_spc

    def __init__(self, layout, w, l, pin0='p0', pin1='n0',connection_labels=1):
        self.layout = layout
        self.l_capm = self.layout.layer(capm_lay_num, capm_lay_dt)
        self.l_met3 = self.layout.layer(met3_lay_num, met3_lay_dt)
        self.l_met4 = self.layout.layer(met4_lay_num, met4_lay_dt)
        self.l_met4_label = self.layout.layer(
            met4_label_lay_num, met4_label_lay_dt)
        self.l_via3 = self.layout.layer(via3_lay_num, via3_lay_dt)
        self.l_prbndry = self.layout.layer(prbndry_lay_num, prbndry_lay_dt)
        self.percision = 1/self.layout.dbu
        self.cell = self.layout.create_cell(
            "sky130_fd_pr__cap_mim_m3_1_w"+str(w)+"_l"+str(l))
        self.w = w * self.percision
        self.l = l * self .percision
        self.pin0 = pin0
        self.pin1 = pin1
        self.connection_labels=connection_labels

    def draw_vias(self, box, via3_cell):
        via3_size = 0.2*self.percision
        met_via3_enc_1 = 0.065*self.percision
        met_via3_enc_2 = 0.09*self.percision
        via3_spc = 0.2*self.percision
        AL_via3 = pya.Box(0, 0, via3_size, via3_size)
        # via3_cell = self.layout.create_cell("via3")
        via3_cell.shapes(self.l_via3).insert(AL_via3)
        num_via3_1, via3_free_spc_1 = self.number_spc_contacts(
            box.width(), met_via3_enc_1, via3_spc, via3_size)
        num_via3_2, via3_free_spc_2 = self.number_spc_contacts(
            box.height(), met_via3_enc_2, via3_spc, via3_size)
        via3_arr = pya.CellInstArray(via3_cell.cell_index(), pya.Trans(
            pya.Point(box.p1.x+via3_free_spc_1 / 2, box.p1.y + via3_free_spc_2 / 2)),
            pya.Vector(via3_spc + via3_size, 0),
            pya.Vector(0, via3_spc + via3_size),
            num_via3_1, num_via3_2)

        return via3_arr

    def draw_cap(self):

        mimcap_box = pya.Box(mimcap.mimcap_drawing_offest*self.percision,
                             mimcap.mimcap_drawing_offest*self.percision,
                             mimcap.mimcap_drawing_offest*self.percision+self.w,
                             mimcap.mimcap_drawing_offest*self.percision+self.l)

        self.cell.shapes(self.l_capm).insert(mimcap_box)
        self.met4_center_box = mimcap_box.enlarge(-1*mimcap.mimcap_enc_metal4*self.percision,

                                                  -1*mimcap.mimcap_enc_metal4*self.percision)
        self.cell.shapes(self.l_met4).insert(self.met4_center_box)
        met3_box = pya.Box(0, 0,
                           mimcap.mimcap_drawing_offest*self.percision +
                           self.w+mimcap.metal3_margin_right*self.percision,
                           2*mimcap.mimcap_drawing_offest*self.percision+self.l)

        self.cell.shapes(self.l_met3).insert(met3_box)
        pin0_text = pya.Text(self.pin0, self.met4_center_box.center().x,
                             self.met4_center_box.center().y)
        prbndry_box = pya.Box(0, 0,
                              2*mimcap.mimcap_drawing_offest*self.percision+self.w,
                              2*mimcap.mimcap_drawing_offest*self.percision+self.l)

        self.cell.shapes(self.l_prbndry).insert(prbndry_box)

        self.met4_side_box = pya.Box(prbndry_box.p2.x-mimcap.met4_side_overlap*self.percision,
                                     prbndry_box.p1.y + 0.06*self.percision,
                                     prbndry_box.p2.x-mimcap.met4_side_overlap *
                                     self.percision+mimcap.met4_side_width*self.percision,
                                     prbndry_box.p2.y - 0.06*self.percision)
        pin1_text = pya.Text(self.pin1, self.met4_side_box.center().x,
                             self.met4_side_box.center().y)
        if self.connection_labels:
            self.cell.shapes(self.l_met4_label).insert(pin0_text)
            self.cell.shapes(self.l_met4_label).insert(pin1_text)

        self.cell.shapes(self.l_met4).insert(self.met4_side_box)

        # print('--->', self.layout.cell("via3"))
        if self.layout.cell("via3") == None:
            via3_cell = self.layout.create_cell("via3")
            # print('--->', self.layout.cell("via3"))
        else:
            via3_cell = self.layout.cell("via3")

        via3_arr = self.draw_vias(self.met4_center_box, via3_cell)

        self.cell.insert(via3_arr)

        via3_arr = self.draw_vias(self.met4_side_box, via3_cell)
        self.cell.insert(via3_arr)
        # For correct drc on magic 
        self.cell.flatten(1)
        return self.cell

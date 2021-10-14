
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
import math
from .imported_generators.mimcap import *




class mimcap_1_gen(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the mimcap_1
    """

    def __init__(self):

        # Important: initialize the super class
        super(mimcap_1_gen, self).__init__()

        # declare the parameters
        self.param("l", self.TypeDouble, "Length", default=1,unit="um")
        self.param("w", self.TypeDouble, "Width", default=1,unit="um")
        self.param("array_x", self.TypeInt, "elements in x_direction", default=1)
        self.param("array_y", self.TypeInt, "elements in y_direction", default=1)
        self.param("x_spacing", self.TypeDouble, "spacing in x_direction", default=1,unit="um")
        self.param("y_spacing", self.TypeDouble, "spacing in y_direction", default=1,unit="um")
        self.param("totalcap", self.TypeDouble, "Total Capcitance",unit="fF",readonly=True)
        # self.set_totalcap(4)
        


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "sky130_fd_pr__cap_mim_m3_1_w"+str(self.w)+"_l"+str(self.l)

    def coerce_parameters_impl(self):

        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        # rs = None
        # if isinstance(self.s, pya.DPoint):
        #     # compute distance in micron
        #     rs = self.s.distance(pya.DPoint(0, 0))
        # if rs != None and abs(self.r - self.ru) < 1e-6:
        #     self.ru = rs
        #     self.r = rs
        # else:
        #     self.ru = self.r
        #     self.s = pya.DPoint(-self.r, 0)

        # self.rd = 2 * self.r

        # # n must be larger or equal than 4
        # if self.n <= 4:
        #     self.n = 4
        self.totalcap = self.w * self.l * self.array_x * self.array_y * 2

    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        # return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
        pass

    def parameters_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        # bounding box width and layer
        # self.r = self.shape.bbox().width() * self.layout.dbu / 2
        # self.l = self.layout.get_info(self.layer)
        pass

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        pass

    def produce_impl(self):
       
        self.percision = 1/self.layout.dbu
        mimcap_instance = mimcap(layout=self.layout,w=self.w,l=self.l,connection_labels=0)
        mimcap_cell = mimcap_instance.draw_cap()
        write_cells = pya.CellInstArray(mimcap_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                              pya.Vector(self.x_spacing*self.percision, 0), pya.Vector(0, self.y_spacing*self.percision),self.array_x , self.array_y)
        
        self.cell.flatten(1)
        self.cell.insert(write_cells)
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
## Mabrains Company LLC
##
## Mabrains Pcells Generators for Klayout for Skywaters 130nm
########################################################################################################################

import pya

# from .via import ViaGenerator
from .via_new import Via_newGenerator
from .nmos18 import NMOS18
from .pmos18 import PMOS18
from .circle import Circle
from .polyres import PolyRes
from .inductor import IndGenerator
from .rectangular_shielding import rectangular_shielding_Generator
from .triangular_shielding import triangular_shielding_Generator
from .diff_square_inductor import diff_squar_ind_Generator
from .single_octagon_ind import single_octagon_ind_Generator
from .new_single_octagon_ind import new_single_octagon_Generator
from .diff_octagon import diff_octagon_ind_Generator
from .nmos5d10 import nmos5d10_gen
from .pmos5d10 import pmos5d10_gen
from .mimcap_1 import mimcap_1_gen
from .mimcap_2 import mimcap_2_gen
from .pnp_gen import pnp_bjt


from .layers_definiations import *

class Sky130(pya.Library):
    """
    The library where we will put the PCell into
    """

    def __init__(self):
        # Set the description
        self.description = "Skywaters 130nm Pcells"

        # Create the PCell declarations
        # self.layout().register_pcell("via", ViaGenerator())
        self.layout().register_pcell("via_new", Via_newGenerator())
        self.layout().register_pcell("nmos18", NMOS18())
        self.layout().register_pcell("Circle", Circle())
        self.layout().register_pcell("pmos18", PMOS18())
        self.layout().register_pcell("poly_res", PolyRes())
        self.layout().register_pcell("inductor", IndGenerator())
        self.layout().register_pcell("rectangular_shielding", rectangular_shielding_Generator())
        self.layout().register_pcell("triangular_shielding", triangular_shielding_Generator())
        self.layout().register_pcell("diff_square_inductor", diff_squar_ind_Generator())
        self.layout().register_pcell("diff_octagon_inductor", diff_octagon_ind_Generator())
        self.layout().register_pcell("single_octagon_ind", single_octagon_ind_Generator())
        self.layout().register_pcell("new_single_octagon_ind", new_single_octagon_Generator())
        self.layout().register_pcell("nmos5d10", nmos5d10_gen())
        self.layout().register_pcell("pmos5d10", pmos5d10_gen())
        self.layout().register_pcell("mimcap_1", mimcap_1_gen())
        self.layout().register_pcell("mimcap_2", mimcap_2_gen())
        self.layout().register_pcell("BNB BJT", pnp_bjt())










        # Register us with the name "MyLib".
        self.register("SKY130")

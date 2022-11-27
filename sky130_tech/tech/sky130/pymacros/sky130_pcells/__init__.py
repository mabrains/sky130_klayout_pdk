########################################################################################################################
##
# Mabrains Company LLC ("Mabrains Company LLC") CONFIDENTIAL
##
# Copyright (C) 2018-2021 Mabrains Company LLC <contact@mabrains.com>
##
# This file is authored by:
#           - <Mina Maksimous> <mina_maksimous@mabrains.com>
##
########################################################################################################################

########################################################################################################################
## Mabrains Company LLC
##
## Mabrains Pcells Generators for Klayout for Skywaters 130nm
########################################################################################################################

import pya

# from .via import ViaGenerator
from sky130_pcells.PcViaStack import pcViaStackGenerator
from sky130_pcells.PcGRing import pcGRingGenerator
from sky130_pcells.PcMos18Finger import pcMos18FingerGenerator
from sky130_pcells.PclvtNmos18 import pclvtNmos18Generator
from sky130_pcells.PclvtPmos18 import pclvtPmos18Generator
from sky130_pcells.PcNmos18 import pcNmos18Generator
from sky130_pcells.PcPmos18 import pcPmos18Generator
from sky130_pcells.PchvtPmos18 import pchvtPmos18Generator
from sky130_pcells.PcNmos5d10 import pcNmos5d10Generator
from sky130_pcells.nmos18 import NMOS18
from sky130_pcells.pmos18 import PMOS18
from sky130_pcells.polyres import PolyRes_gen
from sky130_pcells.inductor import IndGenerator
from sky130_pcells.rectangular_shielding import rectangular_shielding_Generator
from sky130_pcells.triangular_shielding import triangular_shielding_Generator
from sky130_pcells.diff_square_inductor import diff_squar_ind_Generator
from sky130_pcells.single_octagon_ind import single_octagon_ind_Generator
from sky130_pcells.new_single_octagon_ind import new_single_octagon_Generator
from sky130_pcells.diff_octagon import diff_octagon_ind_Generator
from sky130_pcells.nmos5d10 import nmos5d10_gen
from sky130_pcells.pmos5d10 import pmos5d10_gen
from sky130_pcells.mimcap_1 import mimcap_1_gen
from sky130_pcells.mimcap_2 import mimcap_2_gen
from sky130_pcells.pnp_gen import pnp_bjt


from sky130_pcells.layers_definiations import *

class Sky130(pya.Library):
    """
    The library where we will put the PCell into
    """

    def __init__(self):
        # Set the description
        self.description = "Skywaters 130nm Pcells"

        # Create the PCell declarations
        self.layout().register_pcell("PcViaStack", pcViaStackGenerator())
        self.layout().register_pcell("PcGRing", pcGRingGenerator())
        self.layout().register_pcell("PclvtNmos18", pclvtNmos18Generator())
        self.layout().register_pcell("PclvtPmos18", pclvtPmos18Generator())
        self.layout().register_pcell("PcNmos18", pcNmos18Generator())
        self.layout().register_pcell("PcPmos18", pcPmos18Generator())
        self.layout().register_pcell("PchvtPmos18", pchvtPmos18Generator())
        self.layout().register_pcell("PcNmos5d10", pcNmos5d10Generator())
        self.layout().register_pcell("nmos18", NMOS18())
        self.layout().register_pcell("pmos18", PMOS18())
        self.layout().register_pcell("poly_res", PolyRes_gen())
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

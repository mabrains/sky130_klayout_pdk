########################################################################################################################
## Mabrains Company LLC
##
## Mabrains Pcells Generators for Klayout for Skywaters 130nm
########################################################################################################################

import pya

from .via import ViaGenerator
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

from .layers_definiations import *

class Sky130(pya.Library):
    """
    The library where we will put the PCell into
    """

    def __init__(self):
        # Set the description
        self.description = "Skywaters 130nm Pcells"

        # Create the PCell declarations
        self.layout().register_pcell("via", ViaGenerator())
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










        # Register us with the name "MyLib".
        self.register("SKY130")

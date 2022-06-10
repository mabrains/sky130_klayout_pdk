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
# Mabrains Company LLC
##
# Mabrains NMOS 1.8V Generator for Skywaters 130nm
########################################################################################################################
import pya
import math
from .layers_definiations import *
from .imported_generators.nmos18 import *


class NMOS18(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """

    def __init__(self):
        # Initialize super class.
        super(NMOS18, self).__init__()

        # declare the parameters

        self.param("w", self.TypeDouble, "Width", default=0.42)
        self.param("l", self.TypeDouble, "Length", default=0.15)
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("gr", self.TypeBoolean, "guard ring", default=1)
        self.param("dsa", self.TypeInt,
                   "drain and source number of contacts", default=1)
        connection_option = self.param(
            "connection", self.TypeString, "Connection Option", default=0)
        connection_option.add_choice("Connection Up", 0)
        connection_option.add_choice("Connection Down", 1)
        connection_option.add_choice("Alternate connection", 2)
        self.param("connected_gates", self.TypeBoolean, "Connected Gates", default=1)

        self.param("n", self.TypeInt,
                   "Alternate Factor(for Alternate Connection)", default=1)

        #self.param("down_connection", self.TypeBoolean, "Gate connection down", default=1)
        #self.param("up_connection", self.TypeBoolean, "Gate connection up", default=0)
        #self.param("alternate_connection",self.TypeBoolean, "Alternate gate connection",default=0)

        # Below shows how to create hidden parameter is used to determine whether the radius has changed
        # or the "s" handle has been moved
        ## self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
        ## self.param("rd", self.TypeDouble, "Double radius", readonly = True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "NMOS18(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        pass

    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def parameters_from_shape_impl(self):
        #     # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        #     # bounding box width and layer
        self.r = self.shape.bbox().width() * self.layout.dbu / 2
        self.l = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().center())

    def produce_impl(self):
        nmos18_instance = nmos18_device(w=self.w, l=self.l, nf=self.nf, connection=int(self.connection),
                                        layout=self.layout, gr=self.gr, connection_labels=0, dsa=self.dsa,connected_gates=self.connected_gates)
        nmos_cell = nmos18_instance.draw_nmos()

        write_cells = pya.CellInstArray(nmos_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                                        pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
        self.cell.flatten(1)
        self.cell.insert(write_cells)

########################################################################################################################
##
# Mabrains Company LLC ("Mabrains Company LLC") CONFIDENTIAL
##
# Copyright (C) 2018-2021 Mabrains Company LLC <contact@mabrains.com>
##
# This file is authored by:
#           - <Mina Maksimous> <mina_maksimous@mabrains.com>
#
# File Edited by Taher Kourany
##
########################################################################################################################

########################################################################################################################
## Mabrains Company LLC
##
## Mabrains Via Generator for Skywaters 130nm
########################################################################################################################

from sky130_pcells.imported_generators.layers_definiations import *
import pya
import math
import pandas as pd


"""
Mabrains Via Generator for Skywaters 130nm
"""

class pcViaStackGenerator(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """

    def __init__(self):

        ## Initialize super class.
        super(pcViaStackGenerator, self).__init__()
        # declare the parameters

        self.param("des_param", self.TypeString, "Description", default= "SkyWater 130nm Contact/Via Pcell", readonly = True)

        self.param("starting_metal", self.TypeInt, "Lower Metal",default=-5,
        choices= (["Poly",-5], ["Diff Ptap",-4], ["Diff Ntap",-3], ["Diff pdsm",-2], ["Diff ndsm",-1], 
        ["metal1",0], ["metal2",1], ["metal3", 2], ["metal4", 3], ["metal5", 4]))

        self.param("ending_metal",self.TypeInt,"Upper Metal",default=1, 
        choices= (["Metal1",1], ["Metal2",2], ["Metal3",3], ["Metal4",4], ["Metal5",5], ["TOP Metal",6]))

        self.param("width", self.TypeDouble, "width", default=1)
        self.param("length", self.TypeDouble, "length", default=1)
        self.param("hv",self.TypeBoolean,"HV Well",default=False)
        
        top_layer = self.param("top_metal", self.TypeInt, "Top Metal", default=0, hidden=False) 
        top_layer.add_choice("AL",0)
        top_layer.add_choice("CU",1)
        
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pcViaStack (w=%.4gum,l=%.4gum)" % (self.width,self.length)
       
    def coerce_parameters_impl(self):
      """
      parametrization is a two-stage process: the parameters are edited and then transferred to the PCell by
      "Apply". Only then the layout is modified. While editing, "coerce_parameters" is called to "fix" the 
      parameter configuration - e.g. to ensure parameters to be compatible or within a certain range. 
      Only the parameter values can be modified. 
      Parameter  attributes such as name, description, type and hidden flag are static.
      """
      if self.ending_metal == 6:
        self.top_metal = 1
        raise AttributeError("Wait!! No Top Metal Exists")
    
    def rectArrayBoundBox(self,lay, x, y, encX, encY, spcX, spcY, width, length, shapetrans = "0,0"):

        """ Calculate number of rect within a given dimensions and the overlap at both ends
            Parameters:
            x,y: length(x-dir) & width(y-direction) of the bounding box
            encX: min enclosure required in x-dir
            ency: min enclosure required in y-dir
            spcX: allowed space between rects in x-dir
            spcY: allowed space between rects in y-dir
            width: given width (y-dir) of rect
            length: given length(x-dir) of rect      
        """
        
        _y = y - 2 * encY
        pitchY = width + spcY
        numY = int((_y + spcY) / pitchY)
        ovlY = y - (numY * width + (numY - 1) * spcY)
         
        _x = x - 2 * encX
        pitchX = length + spcX
        numX = int((_x + spcX) / pitchX)
        ovlX = x - (numX * length + (numX - 1) * spcX)
        
        for indY in range(0,numY):
          for indX in range(0, numX):
            l_Shape = self.cell.shapes(lay).insert(pya.Box(ovlX/2.0+indX*pitchX, -y/2.0+ovlY/2.0+indY*pitchY, ovlX/2.0+indX*pitchX+length , -y/2.0+ovlY/2.0+indY*pitchY+width ))
            l_Shape.transform(pya.Trans(eval(shapetrans)[0],eval(shapetrans)[1])) 
             
    def draw_metals(self,layout, cell, width,length,starting_metal,ending_metal,shapetrans = "0,0"):
        
        precision = 1000
        width = width * precision
        length = length * precision
        
        self.layout = layout
        self.cell = cell
        
        #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
        #Enclosure of diff by nsdm(psdm), except for butting edge 0.125
        #Enclosure of tap by nsdm(psdm), except for butting edge 0.125
        #Enclosure of (n+) tap by N-well. Rule exempted inside UHVI = 0.18
        #N+ Htap must be enclosed by Hv_nwell by at least …Rule exempted inside UHVI. = 0.33
        #Min enclosure of Hdiff or Htap by Hvi. Rule exempted inside UHVI. = 0.18
        #(Nwell overlapping hvi) must be enclosed by hvi
        
        npsdm_enc_diff = 0.125*precision
        npsdm_enc_tap = 0.125*precision # ok
        nwell_enc_ntap = 0.180*precision 
        
        hvnwell_enc_tap = 0.33*precision 
        hvi_enc_tap = max(hvnwell_enc_tap, 0.18*precision) 
        
        #Assign lay gdsnumber,datatype to variables
        l_diff = self.layout.layer(diff_lay_num,diff_lay_dt)
        l_nsdm = self.layout.layer(nsdm_lay_num,nsdm_lay_dt)
        l_psdm = self.layout.layer(psdm_lay_num,psdm_lay_dt)
        l_li = self.layout.layer(li_lay_num,li_lay_dt)
        
        l_tap = self.layout.layer(tap_lay_num,tap_lay_dt)
        l_nwell = self.layout.layer(nwell_lay_num,nwell_lay_dt)
        
        l_poly = self.layout.layer(poly_lay_num,poly_lay_dt)
        l_npc = self.layout.layer(npc_lay_num,npc_lay_dt)
       
        l_hvi =  self.layout.layer(hvi_lay_num,hvi_lay_dt)
        
        #define transformation list
        l_Shapes = [];
        
        if starting_metal == -5:
          l_Shapes.append(self.cell.shapes(l_li).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_poly).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_npc).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          
        if starting_metal == -4:
          l_Shapes.append(self.cell.shapes(l_li).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_tap).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_psdm).insert(pya.Box(-npsdm_enc_tap, -width/2.0-npsdm_enc_tap, length+npsdm_enc_tap , width/2.0+npsdm_enc_tap )))
          
          if self.hv :
            l_Shapes.append(self.cell.shapes(l_hvi).insert(pya.Box(-hvi_enc_tap, -width/2.0-hvi_enc_tap, length+hvi_enc_tap , width/2.0+hvi_enc_tap )))
            
        if starting_metal == -3:
          l_Shapes.append(self.cell.shapes(l_li).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_tap).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_nsdm).insert(pya.Box(-npsdm_enc_tap, -width/2.0-npsdm_enc_tap, length+npsdm_enc_tap , width/2.0+npsdm_enc_tap )))
          
          if self.hv :
            l_Shapes.append(self.cell.shapes(l_hvi).insert(pya.Box(-hvi_enc_tap, -width/2.0-hvi_enc_tap, length+hvi_enc_tap , width/2.0+hvi_enc_tap )))
            l_Shapes.append(self.cell.shapes(l_nwell).insert(pya.Box(-hvnwell_enc_tap, -width/2.0-hvnwell_enc_tap, length+hvnwell_enc_tap , width/2.0+hvnwell_enc_tap )))
          else:
            l_Shapes.append(self.cell.shapes(l_nwell).insert(pya.Box(-nwell_enc_ntap, -width/2.0-nwell_enc_ntap, length+nwell_enc_ntap , width/2.0+nwell_enc_ntap )))
        
        if starting_metal == -2:
          l_Shapes.append(self.cell.shapes(l_diff).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_li).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_psdm).insert(pya.Box(-npsdm_enc_diff, -width/2.0-npsdm_enc_diff, length+npsdm_enc_diff , width/2.0+npsdm_enc_diff )))
         
        if starting_metal == -1:
          l_Shapes.append(self.cell.shapes(l_diff).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_li).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
          l_Shapes.append(self.cell.shapes(l_nsdm).insert(pya.Box(-npsdm_enc_diff, -width/2.0-npsdm_enc_diff, length+npsdm_enc_diff , width/2.0+npsdm_enc_diff )))
        
        for i in range(0,ending_metal):
            
            #strcat via index to via string
            metStr = "met"+str(i+1)

            #Assign metStr to layout.layer() Argument. output is gdsnumber,datetype
            if metStr != "met6":
              l_met = self.layout.layer(eval(metStr+"_lay_num"), eval(metStr+"_lay_dt"))
            
            l_Shapes.append(self.cell.shapes(l_met).insert(pya.Box(0, -width/2.0, length , width/2.0 )))
        
        # transforming shapes
        for shape in l_Shapes:
            shape.transform(pya.Trans(eval(shapetrans)[0],eval(shapetrans)[1])) 
      
    def draw_vias(self,layout, cell, width,length,starting_metal,ending_metal,shapetrans = "0,0"):
            
        precision = 1000
        width = width * precision
        length = length * precision
        
        self.layout = layout
        self.cell = cell
        
        if starting_metal < 0: 
          #FEOL contact layers 
          l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)
          
          licon_size = 0.17*precision
          licon_spc = 0.17*precision
        
          #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
          #Enclosure of licon by diff = 0.04um
          #Enclosure of licon by diff on one of two adjacent sides = 0.06um
          #Enclosure of poly_licon by poly = 0.05um
          #Enclosure of poly_licon by poly on one of two adjacent sides = 0.08um
          #Enclosure of licon by one of two adjacent LI sides = 0.08um
          #Enclosure of licon by one of two adjacent edges of isolated tap = 0.12um
          #poly_licon must be enclosed by npc by 0.1um
          #Diff and tap are not allowed to extend beyond their abutting edge
          
          if starting_metal == -5:
              poly_licon_enc_1 = 0.05*precision # ok poly
              poly_licon_enc_2 = 0.08*precision # ok poly
              li_enc_licon_2 = 0.08*precision
              npc_enc_pc_licon = 0.10*precision
              
              met_licon_enc_1 = max(poly_licon_enc_1, npc_enc_pc_licon)
              met_licon_enc_2 = max(poly_licon_enc_2, npc_enc_pc_licon, li_enc_licon_2)
              
          if starting_metal == -4 or starting_metal == -3:
            
            li_enc_licon_2 = 0.08*precision
            tap_enc_licon_2 = 0.12*precision # exclusive for well diff 
            
            met_licon_enc_1 = 0.0
            met_licon_enc_2 = max(li_enc_licon_2, tap_enc_licon_2)
            
          if starting_metal == -2 or starting_metal == -1:
            diff_licon_enc_1 = 0.04*precision # ok diff
            diff_licon_enc_2 = 0.06*precision # diff
            li_enc_licon_2 = 0.08*precision
            
            met_licon_enc_1 = diff_licon_enc_1
            met_licon_enc_2 = max(diff_licon_enc_2, li_enc_licon_2) 
          
          l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
          
          mcon_size = 0.17*precision
          mcon_spc = 0.19*precision
          
          met_mcon_enc_1 = 0.03*precision # ok Met1
          met_mcon_enc_2 = 0.06*precision # ok Met1
        
          #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
          #Mcon must be enclosed by LI by at least 0.0
          #Mcon must be enclosed by Met1 by at least 0.3
          #Mcon must be enclosed by Met1 on one of two adjacent sides by at least 0.06
        
        
          self.rectArrayBoundBox(l_licon,length,width, met_licon_enc_1, met_licon_enc_2, licon_spc, licon_spc, licon_size, licon_size,shapetrans)
          self.rectArrayBoundBox(l_mcon,length,width, met_mcon_enc_1, met_mcon_enc_2, mcon_spc, mcon_spc, mcon_size, mcon_size,shapetrans)
        
        #BEOL contact layers
        #Rules applicable only to Al BE flows
        
        via_size = 0.15*precision
        via_spc = 0.17*precision
        
        #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
        #0.150 µm Via must be enclosed by Met1 by at least …0.55um
        #0.150 µm Via must be enclosed by Met1 on one of two adjacent sides by at least … 0.085um
        #Via must be enclosed by Met2 by at least … 0.55um
        #Via must be enclosed by Met2 on one of two adjacent sides by at least … 0.085um
        
        met1_via_enc_1 = 0.055*precision # ok
        met1_via_enc_2 = 0.085*precision #ok
        met2_via_enc_1 = 0.055*precision 
        met2_via_enc_2 = 0.085*precision
        
        met_via_enc_1 = max(met1_via_enc_1, met2_via_enc_1)
        met_via_enc_2 = max(met2_via_enc_2, met2_via_enc_2) 
        
        via2_size = 0.2*precision
        via2_spc = 0.2*precision
        
        #Via2 must be enclosed by Met2 by at least … 0.04um
        #Via2 must be enclosed by Met2 on one of two adjacent sides by at least … 0.085um
        #Via2 must be enclosed by Met3 by at least … 0.065um
        #Via2 must be enclosed by Met3 on one of two adjacent sides by at least … N/A ???
        
        met2_via2_enc_1 = 0.040 * precision
        met2_via2_enc_2 = 0.085 * precision # ok
        met3_via2_enc = 0.065 * precision # ok
        
        met_via2_enc_1 = max(met2_via2_enc_1, met3_via2_enc)
        met_via2_enc_2 = max(met2_via2_enc_2, met3_via2_enc)
        
        via3_size = 0.2*precision
        via3_spc = 0.2*precision
        
        #Via3 must be enclosed by Met3 by at least … 0.06um
        #Via3 must be enclosed by Met3 on one of two adjacent sides by at least … 0.09um
        #via3 must be enclosed by met4 by atleast 0.065um
        
        met3_via3_enc_1 = 0.06*precision 
        met3_via3_enc_2 = 0.09*precision # ok
        met4_via3_enc = 0.065*precision # ok
        
        met_via3_enc_1 = max(met3_via3_enc_1, met4_via3_enc)
        met_via3_enc_2 = max(met3_via3_enc_2, met4_via3_enc)
        
        via4_size = 0.8*precision
        via4_spc = 0.8*precision
        
        #Via4 must be enclosed by Met4 by at least … 0.19um
        #via4 must be enclosed by met5 by atleast 0.310um
        
        met4_via4_enc = 0.190*precision
        met5_via4_enc = 0.310*precision
        
        met_via4_enc_1 = max(met4_via4_enc, met5_via4_enc)
        met_via4_enc_2 = max(met4_via4_enc, met5_via4_enc)
        
        for i in range(max(1, starting_metal+1), ending_metal):
            
            # Erraitc via layers numebering
            if i == 1: 
              viaInd = "" 
              
            else: 
              viaInd = str(i)
            
            #strcat via index to via string
            viaStr = "via"+viaInd
            
            #Assign viaStr to layout.layer() Argument. output is gdsnumber,datetype
            if viaStr != "via5":
              l_via = self.layout.layer(eval(viaStr+"_lay_num"), eval(viaStr+"_lay_dt"))
            
              #Assign viaStr to via enclosures respectively
              met_via_enc_1 = eval("met_"+viaStr+"_enc_1")
              met_via_enc_2 = eval("met_"+viaStr+"_enc_2")
              
              #Assign viaStr to via sizes respectively
              via_size = eval(viaStr+"_size")
              
              #Assign viaStr to via sizes respectively
              via_spc = eval(viaStr+"_spc")
              
              self.rectArrayBoundBox(l_via,length,width, met_via_enc_1, met_via_enc_2, via_spc, via_spc, via_size, via_size,shapetrans)
              
    def _PcViaStack(self,layout, cell, width,length,starting_metal,ending_metal,shapetrans = "0,0"):
      self.draw_metals(layout,cell,width,length,starting_metal,ending_metal,shapetrans)
      self.draw_vias(layout,cell,width,length,starting_metal,ending_metal,shapetrans)
    
    def produce_impl(self):

        # generate the layout of pcViaStack subpcell (_PcViaStack)  
        self._PcViaStack(self.layout, self.cell,self.width,self.length,self.starting_metal,self.ending_metal,shapetrans = "0,0")
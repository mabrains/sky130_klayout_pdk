
# Taher Kourany, 13.08.22 -- Initial version of MOS18 finger tran

from sky130_pcells.imported_generators.layers_definiations import *
from sky130_pcells.PcViaStack import *
import pya
import math

class pcMos18FingerGenerator:

    """
    Description: MOSFET Finger Transistor Pcell for Skywaters 130nm
    """

    def __init__(self):
    
      ## Initialize super class.
        super(pcMos18FingerGenerator, self).__init__()
      
      
    def _MOS18Finger(self,layout, cell, well, w, l, gate_contact,gate_contact_num):
    
      #----------------------------
      #         Parameters 
      #----------------------------
      # well      : Diffusion Well type (N+S/D, P+S/D) 
      # w         : Gate width (um)
      # l         : Gate length (um)
      
      prcn = 1000
      grid = 0.005*prcn
      
      self.layout = layout
      self.cell = cell
      self.well = well
      self.w = w
      self.l = l
    
      #---------------------
      #     sizes
      #---------------------
      licon_size = 0.17*prcn
      mcon_size = 0.17*prcn
      via_size = 0.15*prcn
      
      #---------------------
      #     spaces
      #---------------------
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #Spacing of licon on diff or tap to poly on diff (for all FETs inside :drc_tag:`areaid.sc` except 0.15um phighvt) = 0.05um
      #Spacing of metal1 to metal1 = 0.14um
      #Spacing of metal 2 to metal 2 = 0.14um
      #spacing of li to li = 0.17um
      licon_poly_spc = 0.05*prcn
      met1_spc = 0.14*prcn
      met2_spc = 0.14*prcn
      li_spc = 0.17*prcn
      via_spc = 0.17*prcn
      mcon_spc = 0.19*prcn
      licon_spc = 0.17*prcn
      
      #---------------------
      #     enclosures
      #---------------------
      diff_licon_enc_1 = 0.04*prcn # diff LICON
      diff_licon_enc_2 = 0.06*prcn
      met_mcon_enc_1 = 0.03*prcn # Met1 MCONT
      met_mcon_enc_2 = 0.06*prcn
      
      poly_licon_enc_2 = 0.08*prcn # ok poly
      li_enc_licon_2 = 0.08*prcn
      npc_enc_pc_licon = 0.10*prcn
      
      met1_via_enc_1 = 0.055*prcn #Met1 Via
      met2_via_enc_1 = 0.055*prcn #Met2 Via
      
      met1_via_enc_2 = 0.085*prcn
      met2_via_enc_2 = 0.085*prcn
      
      #---------------------
      #     draw diff 
      #---------------------  
      #Extension of diff beyond poly (min drain) = 0.25um
      diff_poly_ext = 0.25
      l_diff = self.layout.layer(diff_lay_num, diff_lay_dt)
      
      sa = max(diff_poly_ext,max(mcon_size+2*met_mcon_enc_1, licon_size+2*max(diff_licon_enc_1,li_enc_licon_2,licon_poly_spc)))
      sb = sa
      lenRx = self.l*prcn+sa+sb
      widRx = self.w*prcn
      self.cell.shapes(l_diff).insert(pya.Box(-lenRx/2.0, -widRx/2.0, lenRx/2.0, widRx/2.0))
      
      #------------------------------------
      # draw poly on diff & poly extension
      #------------------------------------
      l_poly = self.layout.layer(poly_lay_num, poly_lay_dt) 
      
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #calculate min poly_metal to diff_metal space
      #Extension of poly beyond diffusion (endcap) = 0.13um
      poly_diff_ext = 0.13*prcn
      lenPC = self.l*prcn
      widPC = self.w*prcn
      extPC = 2*max(met1_spc,met2_spc,poly_diff_ext,li_spc)
      totPC = widPC+extPC
      
      if gate_contact == "Bottom":
        self.cell.shapes(l_poly).insert(pya.Box(-lenPC/2.0, -totPC/2.0, lenPC/2.0, widPC/2.0+poly_diff_ext))
      if gate_contact == "Top":
        self.cell.shapes(l_poly).insert(pya.Box(-lenPC/2.0, -widPC/2.0-poly_diff_ext, lenPC/2.0, totPC/2.0))
      if gate_contact == "Both":
        self.cell.shapes(l_poly).insert(pya.Box(-lenPC/2.0, -totPC/2.0, lenPC/2.0, totPC/2.0))
      
      #---------------------
      #   draw Tran well
      #---------------------
      npsdm_enc_diff = 0.125*prcn
      if self.well == "N+S/D":
        lay_well = "nsdm"
      if self.well == "P+S/D":
        lay_well =  "psdm"
      l_well = self.layout.layer(eval(lay_well+"_lay_num"), eval(lay_well+"_lay_dt")) 
      self.cell.shapes(l_well).insert(pya.Box(-lenRx/2.0-npsdm_enc_diff, -widPC/2.0-npsdm_enc_diff, lenRx/2.0+npsdm_enc_diff, widPC/2.0+npsdm_enc_diff))

      # call pcViaStack Class
      instViaStack = pcViaStackGenerator()
      
      #---------------------
      #  draw Diff contacts
      #---------------------
      # generate stack from Diff to Metal1
      
      widStack_licon = (licon_size+2*max(diff_licon_enc_2,li_enc_licon_2))/prcn
      widStack_mcon = (mcon_size+2*met_mcon_enc_2)/prcn
      widStack = max(self.w, widStack_licon, widStack_mcon) 
      instViaStack._PcViaStack(self.layout, self.cell, widStack, sa/prcn, -1, 1,pya.Point(-lenRx/2.0,0))
      instViaStack._PcViaStack(self.layout, self.cell, widStack, sa/prcn, -1, 1,pya.Point(lenRx/2.0-sb,0))
      
      #generate stack from Metal1 to Metal2
      
      lenStack = via_size+2*max(met1_via_enc_1,met2_via_enc_1)
      widStack_via = (via_size+2*max(met1_via_enc_2,met2_via_enc_2))/prcn
      widStack = max(self.w, widStack_via)
      instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack/prcn, 0, 2,pya.Point(-lenRx/2.0-(lenStack-sa)/2.0,0))
      instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack/prcn, 0, 2,pya.Point(lenRx/2.0-sb-(lenStack-sa)/2.0,0))
      
      #---------------------
      #  draw poly contacts
      #---------------------
      
      #calulate contacts cell width. See PcViaStack.py
      
      # generate stack from Poly1 to Metal1
    
      widStack_licon = gate_contact_num*licon_size+(gate_contact_num-1)*licon_spc+2*max(poly_licon_enc_2, npc_enc_pc_licon, li_enc_licon_2)
      widStack_mcon = gate_contact_num*mcon_size+(gate_contact_num-1)*mcon_spc+2*met_mcon_enc_2 
      widStack = max(widStack_licon, widStack_mcon)
      lenStack_licon = (licon_size+2*max(diff_licon_enc_1,li_enc_licon_2,licon_poly_spc))/prcn
      lenStack_mcon = (mcon_size+2*met_mcon_enc_1)/prcn
      lenStack = max(self.l, lenStack_licon, lenStack_mcon)
      if gate_contact == "Bottom" or gate_contact == "Both":   
        instViaStack._PcViaStack(self.layout, self.cell, widStack/prcn, lenStack, -5, 1,pya.Point(-lenStack/2.0*prcn,-(totPC+widStack)/2.0))
      if gate_contact == "Top" or gate_contact == "Both":   
        instViaStack._PcViaStack(self.layout, self.cell, widStack/prcn, lenStack, -5, 1,pya.Point(-lenStack/2.0*prcn,(totPC+widStack)/2.0))
     
      # generate stack from Metal1 to Metal2
      lenStack = max(self.l, (via_size+2*max(met1_via_enc_1,met2_via_enc_1))/prcn)
      widStack = gate_contact_num*via_size+(gate_contact_num-1)*via_spc+2*max(met1_via_enc_2,met2_via_enc_2)
      if gate_contact == "Bottom" or gate_contact == "Both": 
        instViaStack._PcViaStack(self.layout, self.cell, widStack/prcn, lenStack, 0, 2,pya.Point(-lenStack/2.0*prcn,-(totPC+widStack)/2.0))
      if gate_contact == "Top" or gate_contact == "Both":
        instViaStack._PcViaStack(self.layout, self.cell, widStack/prcn, lenStack, 0, 2,pya.Point(-lenStack/2.0*prcn,(totPC+widStack)/2.0))
        
      
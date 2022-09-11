
# Taher Kourany, 13.08.22 -- Initial version of MOS18 finger tran
# Taher Kourany, 26.08.22 -- sab param, adpatation of pcViaStack fn tran param (to stay in micrometer world)
# Taher Kourany, 27.08.22 -- multi-finger purpose.

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
     
     
    def _MOS18Finger(self,layout, cell, well, w, l, sab, gate_contact,gate_contact_num, finger_num):
   
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
      self.sab = sab
   
      #---------------------
      #     sizes
      #---------------------
      licon_size = 0.17
      mcon_size = 0.17
      via_size = 0.15
     
      #---------------------
      #     spaces
      #---------------------
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #Spacing of licon on diff or tap to poly on diff (for all FETs inside :drc_tag:`areaid.sc` except 0.15um phighvt) = 0.05um
      #Spacing of metal1 to metal1 = 0.14um
      #Spacing of metal 2 to metal 2 = 0.14um
      #spacing of li to li = 0.17um
      licon_poly_spc = 0.05
      met1_spc = 0.14
      met2_spc = 0.14
      li_spc = 0.17
      via_spc = 0.17
      mcon_spc = 0.19
      licon_spc = 0.17
     
      #---------------------
      #     enclosures
      #---------------------
      diff_licon_enc_1 = 0.04 # diff LICON
      diff_licon_enc_2 = 0.06
      met_mcon_enc_1 = 0.03 # Met1 MCONT
      met_mcon_enc_2 = 0.06
     
      poly_licon_enc_2 = 0.08 # ok poly
      li_enc_licon_2 = 0.08
      npc_enc_pc_licon = 0.10
     
      met1_via_enc_1 = 0.055 #Met1 Via
      met2_via_enc_1 = 0.055 #Met2 Via
     
      met1_via_enc_2 = 0.085
      met2_via_enc_2 = 0.085
     
      #---------------------
      #     draw diff
      #---------------------  
      #Extension of diff beyond poly (min drain) = 0.25um
   
      diff_poly_ext = 0.25
      l_diff = self.layout.layer(diff_lay_num, diff_lay_dt)

      sab_min = max(diff_poly_ext,max(mcon_size+2*met_mcon_enc_1, licon_size+2*max(diff_licon_enc_1,li_enc_licon_2,licon_poly_spc)))
      widRx = self.w

      # for multiple finger, sab is calculated and RX is parameterized, only @ peripherals
      sab_max = max(sab_min, self.sab)
      lenRx = self.l*finger_num+sab_min*(finger_num-1)+2*sab_max
      self.cell.shapes(l_diff).insert(pya.DBox(-lenRx/2.0, -widRx/2.0, lenRx/2.0, widRx/2.0))
     
      #------------------------------------
      # draw poly on diff & poly extension
      #------------------------------------
      l_poly = self.layout.layer(poly_lay_num, poly_lay_dt)
     
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #calculate min poly_metal to diff_metal space
      #Extension of poly beyond diffusion (endcap) = 0.13um
      poly_diff_ext = 0.13
      lenPC = self.l
      widPC = self.w
      extPC = 2*max(met1_spc,met2_spc,poly_diff_ext,li_spc)
      totPC = widPC+extPC
     
      for i in range(0,finger_num):
        if gate_contact == "Bottom":
          self.cell.shapes(l_poly).insert(pya.DBox(-lenRx/2.0+sab_max+i*(lenPC+sab_min), -totPC/2.0, -lenRx/2.0+sab_max+lenPC+i*(lenPC+sab_min), widPC/2.0+poly_diff_ext))
        if gate_contact == "Top":
          self.cell.shapes(l_poly).insert(pya.DBox(-lenRx/2.0+sab_max+i*(lenPC+sab_min), -widPC/2.0-poly_diff_ext, -lenRx/2.0+sab_max+lenPC+i*(lenPC+sab_min), totPC/2.0))
        if gate_contact == "Both":
          self.cell.shapes(l_poly).insert(pya.DBox(-lenRx/2.0+sab_max+i*(lenPC+sab_min), -totPC/2.0, -lenRx/2.0+sab_max+lenPC+i*(lenPC+sab_min), totPC/2.0))
     
      #---------------------
      #   draw Tran well
      #---------------------
      npsdm_enc_diff = 0.125
      if self.well == "N+S/D":
        lay_well = "nsdm"
      if self.well == "P+S/D":
        lay_well =  "psdm"
      l_well = self.layout.layer(eval(lay_well+"_lay_num"), eval(lay_well+"_lay_dt"))
      self.cell.shapes(l_well).insert(pya.DBox(-lenRx/2.0-npsdm_enc_diff, -widPC/2.0-npsdm_enc_diff, lenRx/2.0+npsdm_enc_diff, widPC/2.0+npsdm_enc_diff))

      # call pcViaStack Class
      instViaStack = pcViaStackGenerator()
     
      #---------------------
      #  draw Diff contacts
      #---------------------
      # generate stack from Diff to Metal1
      #calulate contacts cell width/length
      widStack_licon = licon_size+2*max(diff_licon_enc_2,li_enc_licon_2)
      widStack_mcon = mcon_size+2*met_mcon_enc_2
      widStack = max(self.w, widStack_licon, widStack_mcon)
      lenStack_licon = licon_size+2*max(diff_licon_enc_1,li_enc_licon_2)
      lenStack_mcon  = mcon_size+2*met_mcon_enc_1
      lenStack_con = max(lenStack_licon, lenStack_mcon)
     
      #calculate contact placement distance to gate
      coX  = lenRx/2.0-sab_max+sab_min-lenStack_con/2.0
      ilenRx = self.l+2*sab_min # intrinsic length of diffusion
     
      for i in range(0,finger_num+1):
        instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack_con, -1, 1,pya.DPoint(-coX+i*(ilenRx-lenStack_con),0))
     
      #generate stack from Metal1 to Meta2
      #calulate contacts cell width/length
      lenStack_via = via_size+2*max(met1_via_enc_1,met2_via_enc_1)
      widStack_via = via_size+2*max(met1_via_enc_2,met2_via_enc_2)
      widStack = max(self.w, widStack_via)
     
      # coX of mcon,licon is used as center point for via placement. lenStack via < lenStack con
     
      for i in range(0,finger_num+1):
        instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack_via, 0, 2,pya.DPoint(-coX+i*(ilenRx-lenStack_con),0))
     
      #---------------------
      #  draw poly contacts
      #---------------------
     
      # generate stack from Poly1 to Metal1
      #calulate contacts cell width/length
      widStack_licon = gate_contact_num*licon_size+(gate_contact_num-1)*licon_spc+2*max(poly_licon_enc_2, npc_enc_pc_licon, li_enc_licon_2)
      widStack_mcon = gate_contact_num*mcon_size+(gate_contact_num-1)*mcon_spc+2*met_mcon_enc_2
      widStack = max(widStack_licon, widStack_mcon)
      lenStack_licon = licon_size+2*max(diff_licon_enc_1,li_enc_licon_2)
      lenStack_mcon = mcon_size+2*met_mcon_enc_1
      lenStack = max(self.l, lenStack_licon, lenStack_mcon)
     
      for i in range(0,finger_num):
        if gate_contact == "Bottom" or gate_contact == "Both":  
          instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack, -5, 1,pya.DPoint(-lenRx/2.0+sab_max+i*(lenPC+sab_min)+lenPC/2.0,-(totPC+widStack)/2.0))
        if gate_contact == "Top" or gate_contact == "Both":  
          instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack, -5, 1,pya.DPoint(-lenRx/2.0+sab_max+i*(lenPC+sab_min)+lenPC/2.0,(totPC+widStack)/2.0))
     
      # generate stack from Metal1 to Metal2
      #calulate contacts cell width/length
      lenStack = max(self.l, via_size+2*max(met1_via_enc_1,met2_via_enc_1))
      widStack = gate_contact_num*via_size+(gate_contact_num-1)*via_spc+2*max(met1_via_enc_2,met2_via_enc_2)
     
      for i in range(0,finger_num):
        if gate_contact == "Bottom" or gate_contact == "Both":
          instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack, 0, 2,pya.DPoint(-lenRx/2.0+sab_max+i*(lenPC+sab_min)+lenPC/2.0,-(totPC+widStack)/2.0))
        if gate_contact == "Top" or gate_contact == "Both":
          instViaStack._PcViaStack(self.layout, self.cell, widStack, lenStack, 0, 2,pya.DPoint(-lenRx/2.0+sab_max+i*(lenPC+sab_min)+lenPC/2.0,(totPC+widStack)/2.0))
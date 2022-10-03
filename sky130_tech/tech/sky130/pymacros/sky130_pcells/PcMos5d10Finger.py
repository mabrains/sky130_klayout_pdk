
# Taher Kourany, 03.010.22 -- Initial version of MOS5d10 finger tran

from sky130_pcells.imported_generators.layers_definiations import *
from sky130_pcells.PcViaStack import *
from sky130_pcells.PcMos18Finger import *
import pya
import math

class pcMos5d10FingerGenerator:

    """
    Description: g5vd10v5 MOSFET Finger Transistor Pcell for Skywaters 130nm
    """

    def __init__(self):
   
      ## Initialize super class.
        super(pcMos5d10FingerGenerator, self).__init__()
     
     
    def _MOS5d10Finger(self,layout, cell, well, w, l, sab, gate_contact,gate_contact_num, finger_num):
   
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
     
      #---------------------
      #     spaces
      #---------------------
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #Spacing of licon on diff or tap to poly on diff (for all FETs inside :drc_tag:`areaid.sc` except 0.15um phighvt) = 0.05um
      #Spacing of metal1 to metal1 = 0.14um
      #Spacing of metal 2 to metal 2 = 0.14um
      #spacing of li to li = 0.17um
      licon_poly_spc = 0.05
     
      #--------------
      # Enclosures
      #--------------
      #Min. enclosure of (n+_diff inside Hvi) but not overlapping :drc_tag:`areaid.ce` by hvntm = 0.185um
      diff_licon_enc_1 = 0.04 # diff LICON
      
      met_mcon_enc_1 = 0.03 # Met1 MCONT
     
      li_enc_licon_2 = 0.08
      
      hvtnm_enc_diff = 0.185
     
      #---------------------
      #     diff Rules
      #---------------------  
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #Extension of diff beyond poly (min drain) = 0.25um
   
      diff_poly_ext = 0.25

      sab_min = max(diff_poly_ext,max(mcon_size+2*met_mcon_enc_1, licon_size+2*max(diff_licon_enc_1,li_enc_licon_2,licon_poly_spc)))
      widRx = self.w
   
      # for multiple finger, sab is calculated and RX is parameterized, only @ peripherals
      sab_max = max(sab_min, self.sab)
      lenRx = self.l*finger_num+sab_min*(finger_num-1)+2*sab_max
   
      #----------------------------------------
      # poly on diff & poly extension Rules
      #----------------------------------------
     
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #calculate min poly_metal to diff_metal space
      #Extension of poly beyond diffusion (endcap) = 0.13um
      
      # instantiate NMOS18 Finger Transistor (_MOS18Finger)
      instpcMos18Finger = pcMos18FingerGenerator()
      mos18 = instpcMos18Finger._MOS18Finger(self.layout,self.cell,well,w, l, sab, gate_contact, gate_contact_num, finger_num)
   
      # draw hvntm for hvi thick gate oxide (5V) MOS
      l_hvntm = self.layout.layer(hvntm_lay_num,hvntm_lay_dt)
      self.cell.shapes(l_hvntm).insert(pya.DBox(-lenRx/2.0-hvtnm_enc_diff, -widRx/2.0-hvtnm_enc_diff, lenRx/2.0+hvtnm_enc_diff, widRx/2.0+hvtnm_enc_diff))

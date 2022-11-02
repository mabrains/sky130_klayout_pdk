# Taher Kourany, 05.08.22 -- Initial version of nmos18 pcell generator
# Taher Kourany, 26.08.22 -- high level sab param pass
# Taher Kourany, 27.08.22 -- high level multi-finger param pass.
# Taher Kourany, 02.11.22 -- Guard ring contact & S/D contact coverage param (%)

from sky130_pcells.imported_generators.layers_definiations import *
from sky130_pcells.PcMos18Finger import *
from sky130_pcells.PcGRing import *

import pya
import math


class pclvtNmos18Generator(pya.PCellDeclarationHelper):

    """
    Description: Low-vt Nmos18 Pcell for Skywaters 130nm
    """

    def __init__(self):

        ## Initialize super class.

        super(pclvtNmos18Generator, self).__init__()

        #----------------------------
        #         Parameters 
        #----------------------------

        # des_param       : Description of Pcell function
        # w               : Channel Wid
        # l               : Channel Length
        # sab             : diffusion extension on STI
        # gate_contact    : gate contact availability (top,bottom,both)
        # gate_contact_num: num of gate contact vertical direction (1,2)
        # finger_num      : number of tran fingers
        # grCovmCON       : coverage of guard ring contacts (%)
        # sdCovmCON       : coverage of Source/Drain contacts (%)
        # LmCON           : Toggle left side mCON placement (True,False)
        # RmCON           : Toggle Right side mCON placement (True,False)
        # BmCON           : Toggle Bottom mCON placement (True,False)
        # TmCON           : Toggle Top mCON placement (True,False)

        # declare the parameters
        self.param("des_param", self.TypeString, "Description", default= "SkyWater 130nm LVT-NMOS18 Pcell", readonly = True)
        self.param("w", self.TypeDouble, "Width", default=5.0)
        self.param("l", self.TypeDouble, "Length", default=5.0)
        self.param("sab", self.TypeDouble, "SAB", default=0.33)
        self.param("gate_contact", self.TypeString, "Gate Contact",default="Both", choices= (["Top","Top"], ["Bottom","Bottom"], ["Both","Both"],["Alternate","Alternate"]))
        self.param("gate_contact_num", self.TypeInt, "Gate Contact Num",default=1, choices= (["1",1], ["2",2]))
        self.param("finger_num", self.TypeInt, "Fingers Num", default=1)
        self.param("grCovmCON", self.TypeDouble, "Guard Ring Contact Coverage (%)",default=100.0)
        self.param("sdCovmCON", self.TypeDouble, "Source/Drain Contact Coverage (%)",default=100.0)
        self.param("LmCON", self.TypeBoolean, "Left CA",default=True)
        self.param("RmCON", self.TypeBoolean, "Right CA",default=True)
        self.param("BmCON", self.TypeBoolean, "Bottom CA",default=True)
        self.param("TmCON", self.TypeBoolean, "Top CA",default=True)

    def display_text_impl(self):

        # Provide a descriptive text for the cell
        return "pclvtNmos18 (w=%.4gum,l=%.4gum)" % (self.w,self.l)

    def coerce_parameters_impl(self):

      """
      parametrization is a two-stage process: the parameters are edited and then transferred to the PCell by
      "Apply". Only then the layout is modified. While editing, "coerce_parameters" is called to "fix" the 
      parameter configuration - e.g. to ensure parameters to be compatible or within a certain range. 
      Only the parameter values can be modified. 
      Parameter  attributes such as name, description, type and hidden flag are static.
      """
      #min. poly width = 0.15um 
      poly_size = 0.15
      #min. spacing of poly to poly = 0.21um
      poly_spc = 0.21
      #Extension of diff beyond poly (min drain) = 0.25um
      diff_poly_ext = 0.25
      #mcon min width = 0.17um
      mcon_size = 0.17
      #enclosure of mcon by met = 0.03um
      met_mcon_enc_1 = 0.03
      #enclosure of mcon by met at least one of two adjacent sides = 0.06um
      met_mcon_enc_2 = 0.06
      #licon size = 0.17um
      licon_size = 0.17
      #enclosure of licon by diff = 0.04um
      diff_licon_enc_1 = 0.04
      #enclosure of licon by Diff by at least one of two adjacent sides = 0.06 um
      diff_licon_enc_2 = 0.06
      #enclosure of licon by li = 0.08um
      li_enc_licon_2 = 0.08
      #Spacing of licon on diff or tap to poly on diff (for all FETs inside :drc_tag:`areaid.sc` except 0.15um phighvt) = 0.05um
      licon_poly_spc = 0.05
      #enclosure of licon by poly = 0.08um
      poly_licon_enc_2 = 0.08
      #spacing of li to li = 0.17um
      li_spc = 0.17
      
      #Min spacing of NPC to NPC = 0.27um
      npc_spc = 0.27
      
      #calulate min allowed length of poly/met enclosing contacts x-dir
      length_poly_licon = licon_size+2*max(poly_licon_enc_2,li_enc_licon_2)
      length_met_mcon = mcon_size+2*met_mcon_enc_1
      length_gate_contact = max(length_poly_licon,length_met_mcon)
      
      #calculate min allowed width of diff enclosing contacts
      sab_min = max(diff_poly_ext,max(mcon_size+2*met_mcon_enc_1, licon_size+2*max(diff_licon_enc_1,li_enc_licon_2,licon_poly_spc)))

      if self.w < sab_min:
        self.w = sab_min
        #raise AttributeError("Mininum channel width 0.33um")
       
      if self.sab < sab_min:
        self.sab = sab_min
        #raise AttributeError("Mininum sab 0.33um")
        
      if self.l < max(li_spc,poly_size):
        self.l = max(li_spc,poly_size)
        #raise AttributeError("Mininum poly width 0.15um & Minimum Li Space 0.17um")

      if (self.l+sab_min-length_gate_contact) < max(npc_spc,poly_spc) :
        self.gate_contact = "Alternate"
        #raise AttributeError("alternating gate contact placement")
      
      if round(self.sdCovmCON*100) > round(self.sdCovmCON*10):
        self.sdCovmCON = round(self.sdCovmCON*10.0)/10.0
        #("1 decimal place allowed ")
        
      if self.sdCovmCON > 100.0:
        self.sdCovmCON = 100.0
        #("max 100% ")
        
      if self.sdCovmCON < 0.01:
        #calulate contacts cell width/length
        widStack_licon = licon_size+2*max(diff_licon_enc_2,li_enc_licon_2)
        widStack_mcon = mcon_size+2*met_mcon_enc_2
        widStack = max(self.w*max(0,self.sdCovmCON/100.0), widStack_licon, widStack_mcon)
        self.sdCovmCON = widStack/self.w*100.0
        #("min 1 contact")

      ## ------------------------
      ## GUARD RING CallBACKS-->
      ## ------------------------
      if round(self.grCovmCON*100) > round(self.grCovmCON*10):
        self.grCovmCON = round(self.grCovmCON*10.0)/10.0
        #("1 decimal place allowed ")
        
      if self.grCovmCON > 100.0:
        self.grCovmCON = 100.0
        #("max 100% ")
        
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      # mcon to mcon space = 0.19um
      # licon to licon space = 0.17um
      # mcon to mcon space = 0.17
      via_spc = 0.17
      mcon_spc = 0.19
      licon_spc = 0.17
      diff_tap_spc = 0.27
      npsdm_tap_spc = 0.13
      npsdm_diff_spc = 0.13
      poly_tap_spc = 0.055
      
      met1_spc = 0.14
      met2_spc = 0.14
      
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      # licon size = 0.17um
      # via size = 0.15um
      # mcon size = 0.17um 
      licon_size = 0.17
      via_size = 0.15
      mcon_size = 0.17
      
      #Enclosures
      li_enc_licon_2 = 0.08
      npsdm_enc_tap = 0.125
      npsdm_enc_diff = 0.125
      
      poly_licon_enc_2 = 0.08
      npc_enc_pc_licon = 0.10
      
      met_mcon_enc_1 = 0.03
      met_mcon_enc_2 = 0.06
      
      met1_via_enc_2 = 0.085 
      met2_via_enc_2 = 0.085
      
      #extensions
      #Extension of diff beyond poly (min drain) = 0.25um
      diff_poly_ext = 0.25
      #Extension of poly beyond diffusion (endcap) = 0.13um
      poly_diff_ext = 0.13
      
      max_rect_size = max(licon_size, via_size, mcon_size)
      max_rect_spc = max(licon_spc, via_spc, mcon_spc)
      max_rect_enc = max(li_enc_licon_2, met_mcon_enc_2)
      
      if self.grCovmCON < 100.0:
        wgring_licon = licon_size
        wgring_mcon = mcon_size+2*met_mcon_enc_1

        wgring = max(wgring_licon, wgring_mcon)
        
        #calculate min required guard ring opening (x-dir)
        sab_max = max(sab_min, self.sab)
        lenRx = self.l*self.finger_num+sab_min*(self.finger_num-1)+2*sab_max
        lgring = lenRx+2*max(diff_tap_spc, npsdm_tap_spc+npsdm_enc_tap, npsdm_diff_spc+npsdm_enc_diff, npsdm_enc_diff+npsdm_enc_tap)
        
        #calculate min required guard ring opening (y-dir)
        gate_tap_spc = max(met1_spc,poly_tap_spc,li_spc)
        extPC = 2*max(met1_spc,met2_spc,poly_diff_ext,li_spc) #-- extension poly contacts away from diff
        widStack_licon = self.gate_contact_num*licon_size+(self.gate_contact_num-1)*licon_spc+2*max(poly_licon_enc_2, npc_enc_pc_licon, li_enc_licon_2)
        widStack_mcon = self.gate_contact_num*mcon_size+(self.gate_contact_num-1)*mcon_spc+2*met_mcon_enc_2
        widStack_via = self.gate_contact_num*via_size+(self.gate_contact_num-1)*via_spc+2*max(met1_via_enc_2,met2_via_enc_2)
        widStack = max(widStack_licon, widStack_mcon, widStack_via)
        hgring = self.w+extPC+2*widStack+2*gate_tap_spc
  
        pathLenx = lgring+wgring
        pathLeny = hgring+wgring
        delta_cov = (100-self.grCovmCON)/100.0/2.0
        delta_pathLenx = delta_cov*pathLenx
        delta_pathLeny = delta_cov*pathLeny
          
        if (delta_pathLenx < (max_rect_size+max_rect_spc) and delta_pathLeny < (max_rect_size+max_rect_spc) ) or min(delta_pathLenx, delta_pathLeny)+(wgring-max_rect_size)/2.0 < max_rect_enc or self.grCovmCON < 0.01:
          min_delta_cov1 = (max_rect_size+max_rect_spc)/max(pathLenx, pathLeny)
          min_delta_cov2 = (max_rect_enc-(wgring-max_rect_size)/2.0)/min(pathLenx, pathLeny)
          min_delta_cov = max(min_delta_cov1, min_delta_cov2)
          self.grCovmCON = int((100-2*100.0*min_delta_cov)*10)/10.0
          #("distance between corner contacts has to be respected and no negative values allowed")
          
    def _mos18FingerTrans(self, cell, well, w, l, sab, gate_contact, gate_contact_num, finger_num, sdCovmCON):

      instpcMos18Finger = pcMos18FingerGenerator()
      mos18 = instpcMos18Finger._MOS18Finger(self.layout,self.cell,well,w, l, sab, gate_contact, gate_contact_num, finger_num, sdCovmCON)

    def _ngringTrans(self, cell, well, w, l, sab, gate_contact_num, finger_num,typ, grCovmCON):

      #calculate width of guard ring. see pcViaStack.py
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #Diff and tap are not allowed to extend beyond their abutting edge

      #size

      licon_size = 0.17
      via_size = 0.15
      mcon_size = 0.17

      #spaces

      #Spacing of diff to diff, tap to tap, or non-abutting diff to tap = 0.27um
      #Spacing of (p+) tap to N-well. Rule exempted inside UHVI. = 0.13
      #Spacing of diff/tap abutting edge to a non-conciding diff or tap edge = 0.13um
      #Spacing of NSDM/PSDM to opposite implant diff or tap (for non-abutting diff/tap edges) = 0.13um
      #Spacing of nsdm(psdm) to nsdm(psdm) = 0.38um
      #Spacing of licon on diff or tap to poly on diff (for all FETs inside :drc_tag:`areaid.sc` except 0.15um phighvt) = 0.05um
      #Spacing of metal1 to metal1 = 0.14um
      #Spacing of metal 2 to metal 2 = 0.14um
      #spacing of li to li = 0.17um
      #Spacing of poly on field to tap = 0.055um

      via_spc = 0.17
      mcon_spc = 0.19
      licon_spc = 0.17
      met1_spc = 0.14
      met2_spc = 0.14
      li_spac = 0.17
      poly_tap_spc = 0.055
      npsdm_diff_spc = 0.13
      npsdm_tap_spc = 0.13
      diff_tap_spc = 0.27
      licon_poly_spc = 0.05
      nwell_ptap_spc = 0.13

      #enclosures

      #Enclosure of diff by nsdm(psdm), except for butting edge 0.125
      #Enclosure of tap by nsdm(psdm), except for butting edge 0.125
      #Enclosure of licon by one of two adjacent edges of isolated tap = 0.12um
      #Enclosure of licon by diff on one of two adjacent sides = 0.06um

      li_enc_licon_2 = 0.08
      
      diff_licon_enc_1 = 0.04
      diff_licon_enc_2 = 0.06
      
      tap_iso_enc_licon_2 = 0.12

      poly_licon_enc_2 = 0.08
      npc_enc_pc_licon = 0.10

      met1_via_enc_2 = 0.085 
      met2_via_enc_2 = 0.085

      npsdm_enc_diff = 0.125
      npsdm_enc_tap = 0.125
      met_mcon_enc_1 = 0.03
      met_mcon_enc_2 = 0.06

      #extensions

      #Extension of diff beyond poly (min drain) = 0.25um
      diff_poly_ext = 0.25
      #Extension of poly beyond diffusion (endcap) = 0.13um
      poly_diff_ext = 0.13
      
      if grCovmCON > 99.999:
        wgring_licon = licon_size+2*max(li_enc_licon_2,0)
        wgring_mcon = mcon_size+2*met_mcon_enc_2
        #wgring_via = via_size+2*max(met1_via_enc_2,met2_via_enc_2)
      else:
        wgring_licon = licon_size
        wgring_mcon = mcon_size+2*met_mcon_enc_1
        #wgring_via = via_size

      wgring = max(wgring_licon, wgring_mcon)    

      #calculate min required guard ring opening (x-dir)
      #for multiple finger, sab is calculated and RX is parameterized, only @ peripherals

      sab_min = max(diff_poly_ext,max(mcon_size+2*met_mcon_enc_1, licon_size+2*max(diff_licon_enc_1,li_enc_licon_2,licon_poly_spc)))
      sab_max = max(sab_min, sab)
      lenRx = l*finger_num+sab_min*(finger_num-1)+2*sab_max
      lgring = lenRx+2*max(diff_tap_spc, npsdm_tap_spc+npsdm_enc_tap, npsdm_diff_spc+npsdm_enc_diff, npsdm_enc_diff+npsdm_enc_tap)
      
      #calculate min required guard ring opening (y-dir)
      #calculate min poly_metal to diff_metal space
      
      gate_tap_spc = max(met1_spc,poly_tap_spc,li_spac)
      extPC = 2*max(met1_spc,met2_spc,poly_diff_ext,li_spac) #-- extension poly contacts away from diff
      widStack_licon = gate_contact_num*licon_size+(gate_contact_num-1)*licon_spc+2*max(poly_licon_enc_2, npc_enc_pc_licon, li_enc_licon_2)
      widStack_mcon = gate_contact_num*mcon_size+(gate_contact_num-1)*mcon_spc+2*met_mcon_enc_2
      widStack_via = gate_contact_num*via_size+(gate_contact_num-1)*via_spc+2*max(met1_via_enc_2,met2_via_enc_2)
      widStack = max(widStack_licon, widStack_mcon, widStack_via)
      hgring = w+extPC+2*widStack+2*gate_tap_spc

      instpcGRing = pcGRingGenerator()
      instpcGRing._GRing(self.layout, self.cell, well, False, False, wgring, lgring, hgring, self.LmCON, self.RmCON, self.BmCON, self.TmCON, grCovmCON)

      if typ != "none":
        if typ == "lvtn":
          # draw lvtn low-vt mos to block vt implants
          llvtn = lgring
          hlvtn = hgring
          l_lvtn = self.layout.layer(lvtn_lay_num,lvtn_lay_dt)
          self.cell.shapes(l_lvtn).insert(pya.DBox(-llvtn/2.0, -hlvtn/2.0, llvtn/2.0, hlvtn/2.0))
      
    def _lvtNmos18(self, w, l, sab, gate_contact, gate_contact_num, finger_num, grCovmCON, sdCovmCON):

      self.wellgring = "P+Tap"
      self.wellmos18 = "N+S/D"
      self._ngringTrans(self.cell, self.wellgring, w, l, sab, gate_contact_num, finger_num,"lvtn",grCovmCON)
      self._mos18FingerTrans(self.cell, self.wellmos18, w, l, sab, gate_contact, gate_contact_num, finger_num, sdCovmCON)

    def produce_impl(self):

      # call GRing sub fucntion (__pclvtNmos18)
      lvtnmos18 = self._lvtNmos18(self.w, self.l, self.sab, self.gate_contact,self.gate_contact_num, self.finger_num,self.grCovmCON,self.sdCovmCON)
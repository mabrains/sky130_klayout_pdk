# Taher Kourany, 05.08.22 -- Initial version of nmos18 pcell generator

from sky130_pcells.imported_generators.layers_definiations import *
from sky130_pcells.PcMos18Finger import *
from sky130_pcells.PcGRing import *
import pya
import math


class pcNmos18Generator(pya.PCellDeclarationHelper):
    """
    Description: Nmos18 Pcell for Skywaters 130nm
    """

    def __init__(self):

        ## Initialize super class.
        super(pcNmos18Generator, self).__init__()
        
        #----------------------------
        #         Parameters 
        #----------------------------
        # des_param : Description of Pcell function
        # w         : Channel Wid
        # l         : Channel Length
        # LmCON     : Toggle left side mCON placement (True,False)
        # RmCON     : Toggle Right side mCON placement (True,False)
        # BmCON     : Toggle Bottom mCON placement (True,False)
        # TmCON     : Toggle Top mCON placement (True,False)
        
        # declare the parameters
        self.param("des_param", self.TypeString, "Description", default= "SkyWater 130nm NMOS18 Pcell", readonly = True)
        self.param("w", self.TypeDouble, "Width", default=5.0)
        self.param("l", self.TypeDouble, "Length", default=5.0)
        self.param("gate_contact", self.TypeString, "Gate Contact",default="Both", choices= (["Top","Top"], ["Bottom","Bottom"], ["Both","Both"]))
        self.param("gate_contact_num", self.TypeInt, "Gate Contact Num",default=1, choices= (["1",1], ["2",2]))
        self.param("LmCON", self.TypeBoolean, "Left CA",default=True)
        self.param("RmCON", self.TypeBoolean, "Right CA",default=True)
        self.param("BmCON", self.TypeBoolean, "Bottom CA",default=True)
        self.param("TmCON", self.TypeBoolean, "Right CA",default=True)
        
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pcNmos18 (w=%.4gum,l=%.4gum)" % (self.w,self.l)
    
    def coerce_parameters_impl(self):
      """
      parametrization is a two-stage process: the parameters are edited and then transferred to the PCell by
      "Apply". Only then the layout is modified. While editing, "coerce_parameters" is called to "fix" the 
      parameter configuration - e.g. to ensure parameters to be compatible or within a certain range. 
      Only the parameter values can be modified. 
      Parameter  attributes such as name, description, type and hidden flag are static.
      """
      if self.w < 0.33:
        self.w = 0.33
        #raise AttributeError("Mininum channel width 0.33um")
    
    def _mos18FingerTrans(self, cell, well, w, l, gate_contact, gate_contact_num):
      instpcMos18Finger = pcMos18FingerGenerator()
      mos18 = instpcMos18Finger._MOS18Finger(self.layout,self.cell,well,w, l, gate_contact, gate_contact_num)
      
    def _gringTrans(self, cell, well, w, l,gate_contact_num):
      #calculate width of guard ring. see pcViaStack.py
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #Diff and tap are not allowed to extend beyond their abutting edge
      
      #size
      licon_size = 0.17
      via_size = 0.15
      mcon_size = 0.17
      
      #spaces
      #Spacing of diff to diff, tap to tap, or non-abutting diff to tap = 0.27um
      #Spacing of diff/tap abutting edge to a non-conciding diff or tap edge = 0.13um
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
      nsd_psd_spc = 0.38
      diff_tap_spc = 0.13
      licon_poly_spc = 0.05
      
      #enclosures
      #Enclosure of diff by nsdm(psdm), except for butting edge 0.125
      #Enclosure of tap by nsdm(psdm), except for butting edge 0.125
      
      li_enc_licon_2 = 0.08
      diff_licon_enc_2 = 0.06
      tap_enc_licon_2 = 0.12
      met_mcon_enc_2 = 0.06
      
      poly_licon_enc_2 = 0.08
      npc_enc_pc_licon = 0.10
      
      met1_via_enc_2 = 0.085 
      met2_via_enc_2 = 0.085
      
      npsdm_enc_diff = 0.125
      npsdm_enc_tap = 0.125
      
      met1_mcon_enc_1 = 0.03
      diff_licon_enc_1 = 0.04
      
      #extensions
      #Extension of poly beyond diffusion (endcap) = 0.13um
      poly_diff_ext = 0.13
      
      self.wgring_licon = licon_size+2*max(li_enc_licon_2,diff_licon_enc_2,tap_enc_licon_2)
      self.wgring_mcon = mcon_size+2*met_mcon_enc_2
      self.wgring_via = via_size+2*max(met1_via_enc_2,met2_via_enc_2)
      self.wgring = max(self.wgring_licon, self.wgring_mcon, self.wgring_via)
      
      #calculate min required guard ring opening (x-dir)
      
      sa = max(mcon_size+2*met1_mcon_enc_1, licon_size+2*max(diff_licon_enc_1,licon_poly_spc))
      self.lgring = self.l+2*(sa+nsd_psd_spc+npsdm_enc_diff+npsdm_enc_tap)
      
      #calculate min required guard ring opening (y-dir)
      #calculate min poly_metal to diff_metal space
      #given: psdm has to overlap tap and nsdm has to overlap diff, diff_tap_spc is not compared
      
      gate_tap_spc = max(met1_spc,poly_tap_spc,li_spac)
      extPC = 2*max(met1_spc,met2_spc,poly_diff_ext,li_spac) #-- extension poly contacts away from diff
      widStack_licon = gate_contact_num*licon_size+(gate_contact_num-1)*licon_spc+2*max(poly_licon_enc_2, npc_enc_pc_licon, li_enc_licon_2)
      widStack_mcon = gate_contact_num*mcon_size+(gate_contact_num-1)*mcon_spc+2*met_mcon_enc_2
      widStack_via = gate_contact_num*via_size+(gate_contact_num-1)*via_spc+2*max(met1_via_enc_2,met2_via_enc_2)
      widStack = max(widStack_licon, widStack_mcon, widStack_via)
      self.hgring = self.w+extPC+2*widStack+2*gate_tap_spc
    
      instpcGRing = pcGRingGenerator()
      gring = instpcGRing._GRing(self.layout,self.cell,well,self.wgring,self.lgring,self.hgring,self.LmCON,self.RmCON,self.BmCON,self.TmCON)

    def _Nmos18(self, w, l, gate_contact,gate_contact_num):
      self.wellgring = "P+Tap"
      self.wellmos18 = "N+S/D"
      self.gate_contact = gate_contact
      self.gate_contact_num = gate_contact_num
      self._gringTrans(self.cell, self.wellgring, self.w, self.l, self.gate_contact_num)
      self._mos18FingerTrans(self.cell, self.wellmos18, self.w, self.l, self.gate_contact,self.gate_contact_num)

    def produce_impl(self):
      
      # call GRing sub fucntion (__pcNmos18)
      nmos18 = self._Nmos18(self.w, self.l, self.gate_contact,self.gate_contact_num)
      

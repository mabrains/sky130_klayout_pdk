# Taher Kourany, 28.08.22 -- Initial version of pmos18 pcell generator (w,l,sab,gate_contact,gate_contact_num,finger_num,LmCON,RmCON,BmCON,TmCON)

from sky130_pcells.imported_generators.layers_definiations import *
from sky130_pcells.PcMos18Finger import *
from sky130_pcells.PcGRing import *
import pya
import math

class pcPmos18Generator(pya.PCellDeclarationHelper):

    """
    Description: Nmos18 Pcell for Skywaters 130nm
    """

    def __init__(self):
    
        ## Initialize super class.
        
        super(pcPmos18Generator, self).__init__()

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
        # subring         : Substrate ring placement
        # LmCON           : Toggle left side mCON placement (True,False)
        # RmCON           : Toggle Right side mCON placement (True,False)
        # BmCON           : Toggle Bottom mCON placement (True,False)
        # TmCON           : Toggle Top mCON placement (True,False)

        # declare the parameters
        self.param("des_param", self.TypeString, "Description", default= "SkyWater 130nm PMOS18 Pcell", readonly = True)
        self.param("w", self.TypeDouble, "Width", default=5.0)
        self.param("l", self.TypeDouble, "Length", default=5.0)
        self.param("sab", self.TypeDouble, "SAB", default=0.27)
        self.param("gate_contact", self.TypeString, "Gate Contact",default="Both", choices= (["Top","Top"], ["Bottom","Bottom"], ["Both","Both"]))
        self.param("gate_contact_num", self.TypeInt, "Gate Contact Num",default=1, choices= (["1",1], ["2",2]))
        self.param("finger_num", self.TypeInt, "Fingers Num", default=1)
        self.param("subring", self.TypeBoolean, "Sub-Ring",default=False)
        self.param("LmCON", self.TypeBoolean, "Left CA",default=True)
        self.param("RmCON", self.TypeBoolean, "Right CA",default=True)
        self.param("BmCON", self.TypeBoolean, "Bottom CA",default=True)
        self.param("TmCON", self.TypeBoolean, "Right CA",default=True)

    def display_text_impl(self):
    
        # Provide a descriptive text for the cell
        return "pcPmos18 (w=%.4gum,l=%.4gum)" % (self.w,self.l)

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
      
      if self.sab < 0.33:
        self.sab = 0.33
        #raise AttributeError("Mininum channel width 0.33um")

    def _mos18FingerTrans(self, cell, well, w, l, sab, gate_contact, gate_contact_num, finger_num):

      instpcMos18Finger = pcMos18FingerGenerator()
      mos18 = instpcMos18Finger._MOS18Finger(self.layout,self.cell,well,w, l, sab, gate_contact, gate_contact_num, finger_num) 

    def _pgringTrans(self, cell, well, subwell, w, l, sab, gate_contact_num, finger_num, subring):

      #calculate width of guard ring. see pcViaStack.py
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #Diff and tap are not allowed to extend beyond their abutting edge

      #size
      
      grid = 0.005
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
      #Enclosure of (n+) tap by N-well. Rule exempted inside UHVI = 0.18	
      li_enc_licon_2 = 0.08
      diff_licon_enc_1 = 0.04
      diff_licon_enc_2 = 0.06
      tap_enc_licon_2 = 0.12

      nwell_enc_ntap = 0.180

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

      wgring_licon = licon_size+2*max(li_enc_licon_2,diff_licon_enc_2,tap_enc_licon_2)
      wgring_mcon = mcon_size+2*met_mcon_enc_2
      wgring_via = via_size+2*max(met1_via_enc_2,met2_via_enc_2)
      wgring = max(wgring_licon, wgring_mcon, wgring_via)

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
      gring = instpcGRing._GRing(self.layout, self.cell, well, False, False, wgring, lgring, hgring, self.LmCON, self.RmCON, self.BmCON, self.TmCON)

      if subring:
        wsubgring_licon = licon_size+2*max(li_enc_licon_2,diff_licon_enc_2)
        wsubgring_mcon = mcon_size+2*met_mcon_enc_2
        wsubgring_via = via_size+2*max(met1_via_enc_2,met2_via_enc_2)
        wsubgring = max(wsubgring_licon, wsubgring_mcon, wsubgring_via)
        #if a sub contact is needed, and sub is a processed by p+diff, then "nwell_ptap_spc" should be replaced by nwell_diff_spc which is currently not found in .rst rule file.
        #if there is no shallow sub under sti, consider deleting.
        # either the direct space from diff to tap or space between implants and wells is dominating
        lsubgring = lgring+2*(wgring+max(diff_tap_spc, npsdm_tap_spc+npsdm_enc_tap, npsdm_diff_spc+npsdm_enc_diff, npsdm_enc_diff+npsdm_enc_tap, nwell_enc_ntap+nwell_ptap_spc))
        hsubgring = hgring+2*(wgring+max(diff_tap_spc, npsdm_tap_spc+npsdm_enc_tap, npsdm_diff_spc+npsdm_enc_diff, npsdm_enc_diff+npsdm_enc_tap, nwell_enc_ntap+nwell_ptap_spc))
        lsubgring = round((round(lsubgring/grid/2.0, 2))*grid*2.0, 2)
        hsubgring = round((round(hsubgring/grid/2.0, 2))*grid*2.0, 2)
        wsubgring = round((round(wsubgring/grid/2.0, 2))*grid*2.0, 2)
        
        subgring = instpcGRing._GRing(self.layout, self.cell, subwell, False, False, wsubgring, lsubgring, hsubgring, self.LmCON, self.RmCON, self.BmCON, self.TmCON)

    def _Pmos18(self, w, l, sab, gate_contact, gate_contact_num, finger_num, subring):
      self.wellgring = "N+Tap"
      self.wellsubgring = "P+Tap"
      self.wellmos18 = "P+S/D"
      self._pgringTrans(self.cell, self.wellgring, self.wellsubgring, w, l, sab, gate_contact_num, finger_num, subring)
      self._mos18FingerTrans(self.cell, self.wellmos18, w, l, sab, gate_contact, gate_contact_num, finger_num)

    def produce_impl(self):

      # call GRing sub fucntion (__pcPmos18)
      pmos18 = self._Pmos18(self.w, self.l, self.sab, self.gate_contact,self.gate_contact_num, self.finger_num, self.subring)

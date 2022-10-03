
# Taher Kourany, 05.08.22 -- Initial version of guard rings

from sky130_pcells.imported_generators.layers_definiations import *
import pya
import math
import pandas as pd


class pcGRingGenerator(pya.PCellDeclarationHelper):
    """
    Description: Guard Ring Pcell for Skywaters 130nm
    """

    def __init__(self):

        ## Initialize super class.
        super(pcGRingGenerator, self).__init__()
        
        #----------------------------
        #         Parameters 
        #----------------------------
        # des_param : Description of Pcell function
        # well      : Diffusion Well type (N+ tap NWell, N+S/D, P+ tap PWell, P+S/D) 
        # w         : width of diff layer
        # l         : Inner cell boundary opening in x-dir (um)
        # h         : Inner cell boundary opening in y-dir (um)
        # LmCON     : Toggle left side mCON placement (True,False)
        # RmCON     : Toggle Right side mCON placement (True,False)
        # BmCON     : Toggle Bottom mCON placement (True,False)
        # TmCON     : Toggle Top mCON placement (True,False)
        
        # declare the parameters
        self.param("des_param", self.TypeString, "Description", default= "SkyWater 130nm Guard Ring Pcell", readonly = True)
        self.param("well",self.TypeString,"Well", default="P+Tap",choices=(["N+Tap", "N+Tap"],["N+Tap in DNW","N+Tap in DNW"],["P+Tap", "P+Tap"],["N+S/D", "N+S/D"],["P+S/D","P+S/D"])) 
        self.param("hvnwell", self.TypeBoolean, "Thick Oxide",default=False)
        self.param("nwell_hole", self.TypeBoolean, "Nwell-Hole",default=False)
        self.param("w", self.TypeDouble, "Width", default=0.29)
        self.param("l", self.TypeDouble, "Length", default=5.0)
        self.param("h", self.TypeDouble, "Height", default=5.0)
        self.param("LmCON", self.TypeBoolean, "Left CA",default=True)
        self.param("RmCON", self.TypeBoolean, "Right CA",default=True)
        self.param("BmCON", self.TypeBoolean, "Bottom CA",default=True)
        self.param("TmCON", self.TypeBoolean, "Top CA",default=True)
        
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pcGRing (w=%.4gum,l=%.4gum)" % (self.w,self.l)


    def _GRing(self,layout, cell, well, hvnwell, nwell_hole, w, l, h, LmCON, RmCON, BmCON, TmCON):
      # draw polygons ring paths
      
      self.layout = layout
      self.cell = cell
      prcn = 1000
      w = w
      l = l
      h = h
      grid = 0.005
      
      #periphery.rst https://github.com/google/skywater-pdk/blob/main/docs/rules/periphery-rules.rst
      #check pcViaStack.py
      npsdm_enc_diff = 0.125
      npsdm_enc_tap = 0.125 
      nwell_enc_ntap = 0.180
      hvnwell_enc_tap = 0.33
      
      #Min enclosure of nwell hole by deep nwell outside UHVI = 1.03um
      dnwell_enc_nwellH = 1.03
      
      #Deep nwell must be enclosed by nwell by atleast 0.4um Exempted inside UHVI or :drc_tag:`areaid.lw` 
      nwell_enc_dnwell = 0.4
      
      #cell center-mark
      l_prBpundary = self.layout.layer(prbndry_lay_num,prbndry_lay_dt)
      self.cell.shapes(l_prBpundary).insert(pya.DBox(-grid*10, -grid*2, grid*10 , grid*2))
      self.cell.shapes(l_prBpundary).insert(pya.DBox(-grid*2, -grid*10, grid*2, grid*10))
      
      # active layers_definitions
      # match-case only possible thru py 3.10. check ur python version by print(sys.version)
      if well == "N+Tap" or well == "N+Tap in DNW":
        layList = ["li","tap","nsdm","nwell"]
        encList = [0.0, 0.0, npsdm_enc_tap, nwell_enc_ntap]
        
      if well == "N+Tap in DNW":
      
        if hvnwell:
          layList = layList+["hvi"]
          encList = encList+[hvnwell_enc_tap]
          
          #hvi blanket
          l_lay = self.layout.layer(hvi_lay_num,hvi_lay_dt)
          self.cell.shapes(l_lay).insert(pya.DBox(0-l/2.0, 0-h/2.0,l/2.0, h/2.0))
      
        if nwell_hole:
          # dnwell blanket 
          dnwell_enc_tap = -nwell_enc_ntap+dnwell_enc_nwellH
          l_lay = self.layout.layer(dnwell_lay_num,dnwell_lay_dt)
          self.cell.shapes(l_lay).insert(pya.DBox(
            0-l/2.0-dnwell_enc_tap, 0-h/2.0-dnwell_enc_tap,
            l/2.0+dnwell_enc_tap, h/2.0+dnwell_enc_tap))
        else:
          # dnwell blanket
          #calculate dnwell BBox
          dx_dnwell = w+nwell_enc_ntap-nwell_enc_dnwell 
          l_lay = self.layout.layer(dnwell_lay_num,dnwell_lay_dt)
          self.cell.shapes(l_lay).insert(pya.DBox(
            0-l/2.0-dx_dnwell, 0-h/2.0-dx_dnwell,
            l/2.0+dx_dnwell, h/2.0+dx_dnwell))
          # nwell blanket  
          l_lay = self.layout.layer(nwell_lay_num,nwell_lay_dt)
          self.cell.shapes(l_lay).insert(pya.DBox(0-l/2.0, 0-h/2.0,l/2.0, h/2.0))
        
      if well == "P+Tap":
        layList = ["li","tap","psdm"]
        encList = [0.0, 0.0, npsdm_enc_tap]  
      if well == "N+S/D":
        layList = ["diff","li","nsdm"]
        encList = [0.0, 0.0, npsdm_enc_diff]
      if well == "P+S/D":
        layList = ["diff","li","psdm"]   
        encList = [0.0, 0.0, npsdm_enc_diff]
      
      # active layer generation -- all expect M1
      for i in range(0,len(layList)):
        lay = layList[i]
        l_lay_enc = encList[i]
        
        l_lay = self.layout.layer(eval(lay+"_lay_num"),eval(lay+"_lay_dt"))
        self.cell.shapes(l_lay).insert(
          pya.DPath([pya.DPoint(0-(l+w)/2.0, 0.0), 
          pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0),
          pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0), 
          pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0), 
          pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0),
          pya.DPoint(0-(l+w)/2.0, 0.0)], w+2*l_lay_enc))
      
      # active layer generation -- M1
      lay = "met1"
      l_lay_enc = 0.0
      l_lay = self.layout.layer(eval(lay+"_lay_num"),eval(lay+"_lay_dt"))
      path_left = [pya.DPoint(0-(l+w)/2.0, 0-(h+2*w)/2.0), pya.DPoint(0-(l+w)/2.0, 0+(h+2*w)/2.0)]
      path_bottom = [pya.DPoint(0+(l+2*w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+2*w)/2.0, 0-(h+w)/2.0)]
      path_right = [pya.DPoint(0+(l+w)/2.0, 0+(h+2*w)/2.0),pya.DPoint(0+(l+w)/2.0, 0-(h+2*w)/2.0)]
      path_top = [pya.DPoint(0-(l+2*w)/2.0, 0+(h+w)/2.0), pya.DPoint(0+(l+2*w)/2.0, 0+(h+w)/2.0)]
      
      path_bl = [pya.DPoint(0+(l+2*w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0),
                 pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+w)/2.0, 0+(h+2*w)/2.0)]
       
      path_rb = [pya.DPoint(0+(l+w)/2.0, 0+(h+2*w)/2.0),pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0),
                 pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+2*w)/2.0, 0-(h+w)/2.0)]
      
      path_tr = [pya.DPoint(0-(l+2*w)/2.0, 0+(h+w)/2.0), pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0),
                 pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0),pya.DPoint(0+(l+w)/2.0, 0-(h+2*w)/2.0)]
      
      path_lt = [pya.DPoint(0-(l+w)/2.0, 0-(h+2*w)/2.0), pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0),
                 pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0), pya.DPoint(0+(l+2*w)/2.0, 0+(h+w)/2.0)]
      
      path_blt = [pya.DPoint(0+(l+2*w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0),
                  pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0),
                  pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0), pya.DPoint(0+(l+2*w)/2.0, 0+(h+w)/2.0)]
       
      path_ltr = [pya.DPoint(0-(l+w)/2.0, 0-(h+2*w)/2.0), pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0),
                  pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0), pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0),
                  pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0),pya.DPoint(0+(l+w)/2.0, 0-(h+2*w)/2.0)]
      
      path_trb = [pya.DPoint(0-(l+2*w)/2.0, 0+(h+w)/2.0), pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0),
                  pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0),pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0),
                 pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+2*w)/2.0, 0-(h+w)/2.0)]
      
      path_rbl = [pya.DPoint(0+(l+w)/2.0, 0+(h+2*w)/2.0),pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0),
                  pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0),
                  pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0), pya.DPoint(0-(l+w)/2.0, 0+(h+2*w)/2.0)]
      
      path_all = [pya.DPoint(0-(l+w)/2.0, 0.0), pya.DPoint(0-(l+w)/2.0, 0+(h+w)/2.0),
                  pya.DPoint(0+(l+w)/2.0, 0+(h+w)/2.0), pya.DPoint(0+(l+w)/2.0, 0-(h+w)/2.0), 
                  pya.DPoint(0-(l+w)/2.0, 0-(h+w)/2.0),pya.DPoint(0-(l+w)/2.0, 0.0)]
      
      if LmCON&BmCON&RmCON&TmCON == True:
        self.cell.shapes(l_lay).insert(pya.DPath(path_all, w+2*l_lay_enc))
        
      #2 connected shapes
      if (RmCON+TmCON == 0) & (LmCON+BmCON == 2):
        self.cell.shapes(l_lay).insert(pya.DPath(path_bl, w+2*l_lay_enc))
      if (LmCON+TmCON == 0) & (RmCON+BmCON == 2):
        self.cell.shapes(l_lay).insert(pya.DPath(path_rb, w+2*l_lay_enc))
      if (LmCON+BmCON == 0) & (TmCON+RmCON == 2):
        self.cell.shapes(l_lay).insert(pya.DPath(path_tr, w+2*l_lay_enc))
      if (RmCON+BmCON == 0) & (LmCON+TmCON == 2):
        self.cell.shapes(l_lay).insert(pya.DPath(path_lt, w+2*l_lay_enc))
        
      #2 unconnected shapes
      if (BmCON+TmCON == 0) & (LmCON+RmCON == 2):
        self.cell.shapes(l_lay).insert(pya.DPath(path_left, w+2*l_lay_enc))
        self.cell.shapes(l_lay).insert(pya.DPath(path_right, w+2*l_lay_enc))
        
      if (BmCON+TmCON == 2) & (LmCON+RmCON == 0):
        self.cell.shapes(l_lay).insert(pya.DPath(path_bottom, w+2*l_lay_enc))
        self.cell.shapes(l_lay).insert(pya.DPath(path_top, w+2*l_lay_enc))
      
      # 3 connected shapes 
      if (RmCON == False) & (BmCON+LmCON+TmCON == 3):
        self.cell.shapes(l_lay).insert(pya.DPath(path_blt, w+2*l_lay_enc))
      if (BmCON == False) & (LmCON+TmCON+RmCON == 3):
        self.cell.shapes(l_lay).insert(pya.DPath(path_ltr, w+2*l_lay_enc))
      if (LmCON == False) & (TmCON+RmCON+BmCON == 3):
        self.cell.shapes(l_lay).insert(pya.DPath(path_trb, w+2*l_lay_enc))
      if (TmCON == False) & (RmCON+BmCON+LmCON == 3):
        self.cell.shapes(l_lay).insert(pya.DPath(path_rbl, w+2*l_lay_enc))
       
      # 1 shape 
      if (BmCON+RmCON+TmCON == 0) & (LmCON == True):
        self.cell.shapes(l_lay).insert(pya.DPath(path_left, w+2*l_lay_enc))  
      if (LmCON+RmCON+TmCON == 0) & (BmCON == True):
        self.cell.shapes(l_lay).insert( pya.DPath(path_bottom, w+2*l_lay_enc))
      if (LmCON+BmCON+TmCON == 0) & (RmCON == True):  
        self.cell.shapes(l_lay).insert(pya.DPath(path_right, w+2*l_lay_enc))
      if (LmCON+BmCON+RmCON == 0) & (TmCON == True):  
        self.cell.shapes(l_lay).insert(pya.DPath(path_top, w+2*l_lay_enc))
      
      
      # active contacts generation
      
      # enclosures
      diff_enc_licon = 0.06
      li_enc_licon = 0.08
      met1_enc_mcon = 0.06
      
      # sizes 
      licon_size = 0.17
      mcon_size = 0.17
      
      # spaces
      licon_spc = 0.17
      mcon_spc = 0.19
      
      l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)
      l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
      
      # Generate licon contacts
      #--------------------------
      # length of contacts row: bottom
      pathLen = round((l+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, grid, 0-(l+w)/2.0, 0-(h+w)/2.0, "R0" )
      
      # length of contacts row: Top
      pathLen = round((l+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, grid, 0-(l+w)/2.0, 0+(h+w)/2.0, "R0" )
      
      # Heights of contacts row: Left
      pathLen = round((h+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, grid, 0-(h+w)/2.0, 0-(l+w)/2.0, "R90" )
      
      # Heights of contacts row: Right
      pathLen = round((h+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, grid, 0-(h+w)/2.0, 0+(l+w)/2.0, "R90" )
      
      # Generate mcon contacts
      #--------------------------
      # length of contacts row: bottom
      if BmCON:
        pathLen = round((l+w)/grid)*grid  
        self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, grid, 0-(l+w)/2.0, 0-(h+w)/2.0, "R0" )
      
      # length of contacts row: Top
      if TmCON:
        pathLen = round((l+w)/grid)*grid  
        self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, grid, 0-(l+w)/2.0, 0+(h+w)/2.0, "R0" )
      
      # Heights of contacts row: Left
      if LmCON:
        pathLen = round((h+w)/grid)*grid  
        self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, grid, 0-(h+w)/2.0, 0-(l+w)/2.0, "R90" )
      
      # Heights of contacts row: Right
      if RmCON:
        pathLen = round((h+w)/grid)*grid  
        self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, grid, 0-(h+w)/2.0, 0+(l+w)/2.0, "R90" )
    
    def rectRowCenterToCenter(self, l_rect, pathLen, min_rect_spc, rect_size, grid, varCrd, fixCrd, R):
      """
        A function that places first and last rect-centers over path beg&end
        spaces between rects are then calculated based on min_rect_spc param.+delta.
        delta changes when path lengths - over which rects are placed center to center - change.
      """
      std_pitch_rect = rect_size+min_rect_spc
      num_rects_dec = (pathLen+std_pitch_rect)/std_pitch_rect
      num_rects_int = int( (pathLen+std_pitch_rect)/std_pitch_rect )
      
      delta = round( (num_rects_dec-num_rects_int)*std_pitch_rect/grid )*grid
      rect_spc = min_rect_spc+int((delta/(num_rects_int-1))/grid)*grid
      pitch_rect = rect_size+rect_spc
      
      grid_delta = round( (delta-(rect_spc-min_rect_spc)*(num_rects_int-1))/grid )*grid
      
      for i in range(0, int(num_rects_int/2)):
        vcon1 = round((varCrd+i*pitch_rect)/grid )*grid
        if num_rects_int % 2 == 0:
          vcon2 = round((varCrd+grid_delta+(i+num_rects_int/2.0)*pitch_rect)/grid )*grid
        else:
          vcon2 = round((varCrd+grid_delta+(i+1+int(num_rects_int/2.0))*pitch_rect)/grid )*grid
          vcon3 = round((varCrd+grid_delta/2.0+int(num_rects_int/2.0)*pitch_rect)/grid )*grid
          
          #expectional contact placement
          if R == "R0":
            self.cell.shapes(l_rect).insert(pya.DBox(vcon3-rect_size/2.0, fixCrd-rect_size/2.0, vcon3+rect_size/2.0, fixCrd+rect_size/2.0))
          else:
            self.cell.shapes(l_rect).insert(pya.DBox(fixCrd-rect_size/2.0, vcon3-rect_size/2.0, fixCrd+rect_size/2.0, vcon3+rect_size/2.0))
        
        # draw contacts
        if R == "R0":
          self.cell.shapes(l_rect).insert(pya.DBox(vcon1-rect_size/2.0, fixCrd-rect_size/2.0, vcon1+rect_size/2.0, fixCrd+rect_size/2.0))
          self.cell.shapes(l_rect).insert(pya.DBox(vcon2-rect_size/2.0, fixCrd-rect_size/2.0, vcon2+rect_size/2.0, fixCrd+rect_size/2.0))
        else:
          self.cell.shapes(l_rect).insert(pya.DBox(fixCrd-rect_size/2.0, vcon1-rect_size/2.0, fixCrd+rect_size/2.0, vcon1+rect_size/2.0))
          self.cell.shapes(l_rect).insert(pya.DBox(fixCrd-rect_size/2.0, vcon2-rect_size/2.0, fixCrd+rect_size/2.0, vcon2+rect_size/2.0))
    def produce_impl(self):
      
      # call GRing sub fucntion (_GRing)
      self._GRing(self.layout,self.cell,self.well,self.hvnwell,self.nwell_hole,self.w,self.l,self.h,self.LmCON,self.RmCON,self.BmCON,self.TmCON)
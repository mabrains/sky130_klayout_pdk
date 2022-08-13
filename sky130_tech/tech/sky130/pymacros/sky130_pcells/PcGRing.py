
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
        self.param("well",self.TypeString,"Well", default="P+Tap",choices=(["N+Tap", "N+Tap"],["P+Tap", "P+Tap"],["N+S/D", "N+S/D"],["P+S/D","P+S/D"])) 
        self.param("w", self.TypeDouble, "Width", default=0.29)
        self.param("l", self.TypeDouble, "Length", default=5.0)
        self.param("h", self.TypeDouble, "Height", default=5.0)
        self.param("LmCON", self.TypeBoolean, "Left CA",default=True)
        self.param("RmCON", self.TypeBoolean, "Right CA",default=True)
        self.param("BmCON", self.TypeBoolean, "Bottom CA",default=True)
        self.param("TmCON", self.TypeBoolean, "Right CA",default=True)
        
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pcGRing (w=%.4gum,l=%.4gum)" % (self.w,self.l)


    def _GRing(self,well,w,l,h,LmCON,RmCON,BmCON,TmCON):
      # draw polygons ring paths
      
      PRCN = 1000
      w = w*PRCN
      l = l*PRCN
      h = h*PRCN
      grid = 0.005*PRCN
      
      npsdm_enc_diff = 0.125*PRCN
      npsdm_enc_tap = 0.125*PRCN 
      nwell_enc_ntap = 0.180*PRCN
      
      #cell center-mark
      l_prBpundary = self.layout.layer(prbndry_lay_num,prbndry_lay_dt)
      self.cell.shapes(l_prBpundary).insert(pya.Box(-grid*10, -grid*2, grid*10 , grid*2))
      self.cell.shapes(l_prBpundary).insert(pya.Box(-grid*2, -grid*10, grid*2, grid*10))
      
      # active layers_definitions
      # match-case only possible thru py 3.10. check ur python version by print(sys.version)
      if well == "N+Tap":
        layList = ["diff","li","tap","nsdm","nwell","met1"]
        encList = [0.0, 0.0, 0.0, npsdm_enc_tap, nwell_enc_ntap, 0.0]
        # nwell blanket
        l_lay = self.layout.layer(nwell_lay_num,nwell_lay_dt)
        self.cell.shapes(l_lay).insert(
          pya.Box(0-l/2.0+nwell_enc_ntap, 0-h/2.0+nwell_enc_ntap, 
          l/2.0+nwell_enc_ntap, h/2.0+nwell_enc_ntap))
      if well == "P+Tap":
        layList = ["diff","li","tap","psdm","met1"]
        encList = [0.0, 0.0, 0.0, npsdm_enc_tap, 0.0]  
      if well == "N+S/D":
        layList = ["diff","li","nsdm","met1"]
        encList = [0.0, 0.0, npsdm_enc_diff, 0.0]
      if well == "P+S/D":
        layList = ["diff","li","psdm","met1"]   
        encList = [0.0, 0.0, npsdm_enc_diff, 0.0]
      
      # active layer generation
      for i in range(0,len(layList)):
        lay = layList[i]
        l_lay_enc = encList[i]
        
        l_lay = self.layout.layer(eval(lay+"_lay_num"),eval(lay+"_lay_dt"))
        self.cell.shapes(l_lay).insert(
          pya.Path([pya.Point(0-(l+w)/2.0, 0-(h+w)/2.0), 
          pya.Point(0-(l+w)/2.0, 0+(h+w)/2.0),
          pya.Point(0+(l+w)/2.0, 0+(h+w)/2.0), 
          pya.Point(0+(l+w)/2.0, 0-(h+w)/2.0), 
          pya.Point(0-(l+w)/2.0, 0-(h+w)/2.0),
          pya.Point(0-(l+w)/2.0, 0.0)], w+2*l_lay_enc))
      
      # active contacts generation
      
      # enclosures
      diff_enc_licon = 0.06*PRCN
      li_enc_licon = 0.08*PRCN 
      met1_enc_mcon = 0.06*PRCN
      
      # sizes 
      licon_size = 0.17*PRCN
      mcon_size = 0.17*PRCN
      
      # spaces
      licon_spc = 0.17*PRCN
      mcon_spc = 0.19*PRCN
      
      l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)
      l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
      
      # Generate licon contacts
      #--------------------------
      # length of contacts row: bottom
      pathLen = int((l+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, 0.005*PRCN, 0-(l+w)/2.0, 0-(h+w)/2.0, "R0" )
      
      # length of contacts row: Top
      pathLen = int((l+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, 0.005*PRCN, 0-(l+w)/2.0, 0+(h+w)/2.0, "R0" )
      
      # Heights of contacts row: Left
      pathLen = int((h+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, 0.005*PRCN, 0-(h+w)/2.0, 0-(l+w)/2.0, "R90" )
      
      # Heights of contacts row: Right
      pathLen = int((h+w)/grid)*grid  
      self.rectRowCenterToCenter(l_licon, pathLen, licon_spc, licon_size, 0.005*PRCN, 0-(h+w)/2.0, 0+(l+w)/2.0, "R90" )
      
      # Generate mcon contacts
      #--------------------------
      # length of contacts row: bottom
      pathLen = int((l+w)/grid)*grid  
      self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, 0.005*PRCN, 0-(l+w)/2.0, 0-(h+w)/2.0, "R0" )
      
      # length of contacts row: Top
      pathLen = int((l+w)/grid)*grid  
      self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, 0.005*PRCN, 0-(l+w)/2.0, 0+(h+w)/2.0, "R0" )
      
      # Heights of contacts row: Left
      pathLen = int((h+w)/grid)*grid  
      self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, 0.005*PRCN, 0-(h+w)/2.0, 0-(l+w)/2.0, "R90" )
      
      # Heights of contacts row: Right
      pathLen = int((h+w)/grid)*grid  
      self.rectRowCenterToCenter(l_mcon, pathLen, mcon_spc, mcon_size, 0.005*PRCN, 0-(h+w)/2.0, 0+(l+w)/2.0, "R90" )
    
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
            self.cell.shapes(l_rect).insert(pya.Box(vcon3-rect_size/2.0, fixCrd-rect_size/2.0, vcon3+rect_size/2.0, fixCrd+rect_size/2.0))
          else:
            self.cell.shapes(l_rect).insert(pya.Box(fixCrd-rect_size/2.0, vcon3-rect_size/2.0, fixCrd+rect_size/2.0, vcon3+rect_size/2.0))
        
        # draw contacts
        if R == "R0":
          self.cell.shapes(l_rect).insert(pya.Box(vcon1-rect_size/2.0, fixCrd-rect_size/2.0, vcon1+rect_size/2.0, fixCrd+rect_size/2.0))
          self.cell.shapes(l_rect).insert(pya.Box(vcon2-rect_size/2.0, fixCrd-rect_size/2.0, vcon2+rect_size/2.0, fixCrd+rect_size/2.0))
        else:
          self.cell.shapes(l_rect).insert(pya.Box(fixCrd-rect_size/2.0, vcon1-rect_size/2.0, fixCrd+rect_size/2.0, vcon1+rect_size/2.0))
          self.cell.shapes(l_rect).insert(pya.Box(fixCrd-rect_size/2.0, vcon2-rect_size/2.0, fixCrd+rect_size/2.0, vcon2+rect_size/2.0))
    def produce_impl(self):
      
      # call GRing sub fucntion (_GRing)
      self._GRing(self.well,self.w,self.l,self.h,self.LmCON,self.RmCON,self.BmCON,self.TmCON)
from cc3d.cpp.PlayerPython import * 
from cc3d import CompuCellSetup


from cc3d.core.PySteppables import *
import numpy as np

class Projectv1Steppable(SteppableBasePy):

    def __init__(self,frequency=1):

        SteppableBasePy.__init__(self,frequency)

        
        

    def start(self):
        """
        any code in the start function runs before MCS=0
        """
        self.build_wall(self.WALL)
        self.Fieldu_threshold=4
        self.Fieldu_threshold2=2
        self.Fieldv_threshold=5
        self.creationrate=0.9
        #old =0.3
        self.XDThresh=0.8
        self.MDThresh=0.8
        self.MCThresh=2.0
        self.MCThresh2=0
        self.XCThresh=0
        self.XCThresh2=0
        
    def step(self,mcs):
        """
        type here the code that will run every frequency MCS
        :param mcs: current Monte Carlo step
        """
        totvolume=0  #volume check to make sure entire area not filled (may not need)
        for cell in self.cell_list:
            
            totvolume+=cell.volume  #volume incrementer

            
            #concentrations of fields in each cell
            LMelcon=self.field.Melanophore[cell.xCOM,cell.yCOM,0]
            LXancon=self.field.Xanthophore[cell.xCOM,cell.yCOM,0]
            SMelcon=self.field.Melanophores2[cell.xCOM,cell.yCOM,0]
            SXancon=self.field.Xanthophores2[cell.xCOM,cell.yCOM,0]
            

            #cell type changes if no longer in correct location
            if cell.type==self.MELANOPHORES and (LXancon<SXancon):
                cell.type=self.MELANOPHORES2
            if cell.type==self.XANTHOPHORES and (LMelcon<SMelcon):
                cell.type=self.XANTHOPHORES2
            
            #kills or reverts cells every 300 mcs (should count for every cell, but likely too slow)
            if mcs%300==0:
                if cell.type==self.MELANOPHORES2 and LXancon<SXancon:
                    totvolume-=cell.volume
                    self.delete_cell(cell)
                elif cell.type==self.MELANOPHORES2:
                    cell.type=self.MELANOPHORES
                if cell.type==self.XANTHOPHORES2 and LMelcon<SMelcon:
                    totvolume-=cell.volume
                    self.delete_cell(cell)
                elif cell.type==self.XANTHOPHORES2:
                  cell.type=self.XANTHOPHORES  
                    
                
            

                
        print(self.pixel_tracker_plugin.getMediumPixelSet())
        
        #cell seeding
        if np.random.uniform()<1 - np.exp(-self.creationrate*1) and totvolume < 0.95*(self.dim.x*self.dim.y*1): #and len(self.pixel_tracker_plugin.getMediumPixelSet())>0.1*(self.dim.x*self.dim.y*1):
            xseed=np.random.randint(self.dim.x)
            yseed=np.random.randint(self.dim.y)
            occupied= bool(self.cell_field[xseed,yseed,0])
            
            #occupied pixel check
            while occupied:
                xseed=np.random.randint(self.dim.x)
                yseed=np.random.randint(self.dim.y)
                occupied= bool(self.cell_field[xseed,yseed,0])
            
            

            
            
            #seeing according to paper parameters
            if self.field.Melanophores2[xseed,yseed,0]>self.field.Melanophore[xseed,yseed,0] or (self.field.Xanthophores2[xseed,yseed,0]<self.field.Xanthophore[xseed,yseed,0] and self.field.Xanthophore[xseed,yseed,0]>0.1):
                cell = self.new_cell(self.MELANOPHORES)
                self.cell_field[xseed, yseed, 0] = cell

            elif self.field.Melanophores2[xseed,yseed,0]<self.field.Melanophore[xseed,yseed,0] and self.field.Melanophore[xseed,yseed,0]>0.1 or (self.field.Xanthophores2[xseed,yseed,0]>self.field.Xanthophore[xseed,yseed,0]):
                cell = self.new_cell(self.XANTHOPHORES)
                self.cell_field[xseed, yseed, 0] = cell


                
                
        
    def finish(self):
        """
        Finish Function is called after the last MCS
        """



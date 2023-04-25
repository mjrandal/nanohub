from cc3d.core.PySteppables import *
import numpy as np

class FitzHughNagumoSteppable(SteppableBasePy):

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
        self.creationrate=0.3
    def step(self,mcs):
        """
        type here the code that will run every frequency MCS
        :param mcs: current Monte Carlo step
        """
        totvolume=0
        for cell in self.cell_list:
            totvolume+=cell.volume
            ucon=self.field.u[cell.xCOM,cell.yCOM,0]
            vcon=self.field.v[cell.xCOM,cell.yCOM,0]
            if cell.type==self.MELANOPHORES and ucon<self.Fieldu_threshold2:
                #try dying celltype
                #totvolume-=cell.volume
                #self.delete_cell(cell)
                cell.type=self.MELANOPHORES2
                
                
            if cell.type==self.XANTHOPHORES and ucon>self.Fieldu_threshold:
                #try dying celltype
                #totvolume-=cell.volume
                #self.delete_cell(cell)
                cell.type=self.XANTHOPHORES2
            if mcs%100==0:
                if cell.type==self.MELANOPHORES2 and ucon<self.Fieldu_threshold2:
                    totvolume-=cell.volume
                    self.delete_cell(cell)  
                
                if cell.type==self.XANTHOPHORES2 and ucon>self.Fieldu_threshold:
                    totvolume-=cell.volume
                    self.delete_cell(cell)
                if cell.type==self.MELANOPHORES2 and ucon>self.Fieldu_threshold:
                    cell.type=self.MELANOPHORES
                if cell.type==self.XANTHOPHORES2 and ucon<self.Fieldu_threshold2:
                    cell.type=self.XANTHOPHORES
                
        print(self.pixel_tracker_plugin.getMediumPixelSet())
        if mcs>1000 and np.random.uniform()<1 - np.exp(-self.creationrate*1) and totvolume < 0.95*(self.dim.x*self.dim.y*1): #and len(self.pixel_tracker_plugin.getMediumPixelSet())>0.1*(self.dim.x*self.dim.y*1):
            xseed=np.random.randint(self.dim.x)
            yseed=np.random.randint(self.dim.y)
            occupied= bool(self.cell_field[xseed,yseed,0])
            
            while occupied:
                xseed=np.random.randint(self.dim.x)
                yseed=np.random.randint(self.dim.y)
                occupied= bool(self.cell_field[xseed,yseed,0])
            
            
            if self.field.u[xseed,yseed,0] > self.Fieldu_threshold:

                cell = self.new_cell(self.MELANOPHORES)
                # size of cell will be 1x1x1
                self.cell_field[xseed, yseed, 0] = cell
            elif self.field.u[xseed,yseed,0] < self.Fieldu_threshold:
                cell = self.new_cell(self.XANTHOPHORES)
                # size of cell will be 1x1x1
                self.cell_field[xseed, yseed, 0] = cell
                
                
        
    def finish(self):
        """
        Finish Function is called after the last MCS
        """




from cc3d import CompuCellSetup
        

from FitzHughNagumoSteppables import Projectv1Steppable

CompuCellSetup.register_steppable(steppable=Projectv1Steppable(frequency=1))


CompuCellSetup.run()

#testing

from bMapManager import bMap
from bMapManager import bStack
from bMapManager import bStackPlot

m = bMap('a5n')

print m.stackList[1].getMask(z=10)

#m.stackList[1].loadtiff()

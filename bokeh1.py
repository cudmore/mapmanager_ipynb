#just make my qt app call functions like this for web plotting

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, gridplot, output_file, show

from bMapManager import bMap
from bMapManager import bStack
from bMapManager import bStackPlot

#use MapManager class library to open one timepoint in a map
mapName = 'a5n'
myMap = bMap(mapName)
spines = myMap.stackList[1].getSpines()
spinesInt = myMap.stackList[1].getSpinesInt() # !!!!! REMEMBER TO MERGE STACK DB AND INT1/INT2

#append spine intensity to spine stack db (tood: put this into main mapmanager class library)
for col in spinesInt.columns:
	spines[col] = spinesInt[col]
	
output_file(mapName + '_bokeh.html')

# create a column data source for the plots to share
source = ColumnDataSource(data=spines)

TOOLS = "box_select,lasso_select,box_zoom,pan,reset,resize,wheel_zoom,help"

# create a new plot and add a renderer
left = figure(tools=TOOLS, width=300, height=300, title=None, x_axis_label='x (um)', y_axis_label='y (um)')
left.circle('x', 'y', source=source)

# create another new plot and add a renderer
right = figure(tools=TOOLS, width=300, height=300, title=None, x_axis_label='sSum', y_axis_label='sLen2d (um)')
right.circle('sSum', 'sLen2d', source=source)

# create another new plot and add a renderer
right2 = figure(tools=TOOLS, width=300, height=300, title=None, x_axis_label='dSum', y_axis_label='sSum')
right2.circle('dSum', 'sSum', source=source)

# create another new plot and add a renderer
segments = figure(tools=TOOLS, width=300, height=300, title=None, x_axis_label='parentID', y_axis_label='pDist')
segments.circle('parentID', 'pDist', source=source)


'''
http://bokeh.pydata.org/en/0.11.1/docs/user_guide/interaction.html
'''
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import vform

columns = [
        TableColumn(field="roiType", title="roiType"),
        TableColumn(field="x", title="xTitle"),
        TableColumn(field="y", title="yTitle"),
        TableColumn(field="z", title="zTitle"),
        TableColumn(field="sLen2d", title="sLen2d"),
        TableColumn(field="sSum", title="sSum"),
        TableColumn(field="dSum", title="dSum"),
    ]

data_table = DataTable(source=source, columns=columns, width=400, height=280)

p = gridplot([[left, right, right2], [segments]])

layout = vform(data_table, p)

show(layout)
show(layout)
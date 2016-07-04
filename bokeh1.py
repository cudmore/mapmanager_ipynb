#just make my qt app call functions like this for web plotting

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, gridplot, output_file, show

from bMapManager import bMap
from bMapManager import bStack
from bMapManager import bStackPlot

myMap = bMap('a5n')
spines = myMap.stackList[1].getSpines()
spinesInt = myMap.stackList[1].getSpinesInt() # !!!!! REMEMBER TO MERGE STACK DB AND INT1/INT2

for col in spinesInt.columns:
	spines[col] = spinesInt[col]
	
output_file("brushing.html")

'''
x = list(range(-20, 21))
y0 = [abs(xx) for xx in x]
y1 = [xx**2 for xx in x]
'''

# create a column data source for the plots to share
#source = ColumnDataSource(data=dict(x=x, y0=y0, y1=y1))
source = ColumnDataSource(data=spines)

TOOLS = "box_select,lasso_select,help"

# create a new plot and add a renderer
left = figure(tools=TOOLS, width=300, height=300, title=None)
left.circle('x', 'y', source=source)

# create another new plot and add a renderer
right = figure(tools=TOOLS, width=300, height=300, title=None)
right.circle('sSum', 'sLen2d', source=source)


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

p = gridplot([[left, right]])

layout = vform(data_table, p)

show(layout)
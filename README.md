# mapmanager_ipynb
Repository providing python code to load, analyze, and plot MapManager files


# Map Manager class library

See [bMapManager][bMapManager]. Include the following in a Python script...

	from bMapManager import bMap
	from bMapManager import bStack
	from bMapManager import bStackPlot

To run inside an ipython/jupiter notebook, also include

	%matplotlib inline
	from plotly.offline import init_notebook_mode
	init_notebook_mode() # run at the start of every ipython notebook to use plotly.offline

Requires numpy, pandas, tifffile

See [map.ipynb][1] for more sample code.

# [pyQT][pyqt] stack browser

A full GUI stack browser using pyqt. Run the browser with...

    python stackbrowser2.py
    
## Required libraries

    numpy
    pandas
    pyqt #see below
    tifffile #see below
    
### Install tifffile

    pip install tifffile

### Install pyQT on OSX

    brew install pyqt
    
### Installing additional image readers

The QT .jpg reader is not installed by default. Just use .png until this is figured out.

# [Bokeh][bokeh] linked plotting.

This is amazing, generates an html table from a pandas dataframe and quickly make some x/y plots (also in html from a pandas dataframe). Then on selecting points in one plot, these points are propagated to all other plots.

	python bokeh1.py
	

[![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/cudmore/mapmanager_ipynb)
[bokeh]: http://bokeh.pydata.org/en/latest/
[bMapManager]: https://github.com/cudmore/mapmanager_ipynb/blob/master/bMapManager.py
[pyqt]: https://riverbankcomputing.com/software/pyqt/intro
[1]: https://github.com/cudmore/mapmanager_ipynb/blob/master/map.ipynb
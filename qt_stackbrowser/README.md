
# Map Manager class library

Include the following

	from bMapManager import bMap
	from bMapManager import bStack
	from bMapManager import bStackPlot

To run inside an ipython/jupiter notebook, also include

	%matplotlib inline
	from plotly.offline import init_notebook_mode
	init_notebook_mode() # run at the start of every ipython notebook to use plotly.offline

See map.ipynb for sample code

# pyQT stack browser

Run the browser with

    python pyqt_stackbrowser.py
    
# Required libraries

    numpy
    pandas
    pyqt #see below
    tifffile #see below
    
## Install tifffile

    pip install tifffile

## Install pyQT on OSX

    brew install pyqt
    
### Installing additional image readers

The QT .jpg reader is not installed by default. Just use .png until this is figured out.

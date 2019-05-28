# Analytics
A dashboard for data analysis. This is a GUI for [fc-analytics](http://github.com/jboes/fc-analytics).

# Setup
## Prerequisites
A server running:
 - PHP
 - Python
 
 ## Environment
 I have a Python3 environment in `vendor/python3-analytics/bin`. To activate it, navigate to that directory, and then run `source activate`

## Installation
Clone the repository. Then install [plot.ly](https://dash.plot.ly/installation):
```bash
pip install dash==0.42.0  # The core dash backend
pip install dash-daq==0.1.0  # DAQ components (newly open-sourced!)
```


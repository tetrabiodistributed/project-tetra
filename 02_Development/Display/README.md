Ventilator Splitter Display
===========================

A system to take pressure and flow data from sensors on a ventilator splitter, calculate descriptive parameters based on these data like PEEP or Tidal Volume, and display them for medical professionals to monitor.  This is for use against COVID-19.

To set it up for tests, run `./setup.sh` to build the virtual environment and then `source ./venv/bin/activate` to activate it.  To do the tests, run `./runtests.sh`.  This will first show the results of unit tests and then behaviour tests.

To run the display, first make sure Docker is installed, then run these commands.

```bash
docker build -t zmq_proxy:latest .
docker run --rm -p 8000:8000 zmq_proxy:latest
```

Then open http://localhost:8000 in a browser.  With this, you'll see a webpage which every second writes some JSON in a bullet list, where each bullet ought to looks something like this (though it won't be printed as nicely).

```json
{   "0": {   "Flow Rate": -0.12102553332090354,
             "Inspiratory Pressure": 25.185687032203397,
             "PEEP": 7.600443036648329,
             "Peak Pressure": 29.143715376593427,
             "Tidal Volume": 2982.643040302767},
    "1": {   "Flow Rate": -0.1853025137003232,
             "Inspiratory Pressure": 27.589362195098154,
             "PEEP": 9.0296093948397,
             "Peak Pressure": 32.05751894822633,
             "Tidal Volume": 123.60199756683565},
    "2": {   "Flow Rate": -0.23654912423232322,
             "Inspiratory Pressure": 26.474812956451874,
             "PEEP": 7.607352013212795,
             "Peak Pressure": 27.6944434648811,
             "Tidal Volume": 3712.3769706397325},
    "3": {   "Flow Rate": 0.13331473843016745,
             "Inspiratory Pressure": 10.52283673388029,
             "PEEP": 7.33283292927223,
             "Peak Pressure": 23.519565988527702,
             "Tidal Volume": 359.06476658825846}}
```

Ventilator Splitter Display
===========================

A system to take pressure and flow data from sensors on a ventilator splitter, calculate descriptive parameters based on these data like PEEP or Tidal Volume, and display them for medical professionals to monitor.  This is for use against COVID-19.

To run tests, first install the requirements with `pip install -r requirements.txt`, then run `python -m unittest discover Tests`.

To run the display, first make sure Docker is installed (Linux `apt install docker`, macOS `brew install docker`, Windows [try this](https://docs.docker.com/docker-for-windows/install/)).  Then run these commands to build and run the container.

```bash
docker build -t zmq_proxy:latest .
docker run --rm -p 8000:8000 zmq_proxy:latest
```

Following that if you go to http://localhost:8000/, you'll see a webpage which every second writes some JSON in a bullet list, where each datum ought to looks something like this.

```json
{"0": {"Inspiratory Pressure": 9.831078924585793, "Tidal Volume": 3045.260112276059, "PEEP": 5.257976297519821, "PIP": 27.122873643761356, "Mean Airway Pressure": 16.17554322576723, "Flow Rate": 0.11350780740073768}, "1": {"Inspiratory Pressure": 24.986482709967422, "Tidal Volume": 4968.554445248502, "PEEP": 6.839471687488463, "PIP": 39.8287710948516, "Mean Airway Pressure": 38.184401727521475, "Flow Rate": 0.2191122580929193}, "2": {"Inspiratory Pressure": 13.374206048514766, "Tidal Volume": 3985.2655287595157, "PEEP": 5.879469338112722, "PIP": 28.07875697578995, "Mean Airway Pressure": 22.986703544547005, "Flow Rate": 0.15228292450414116}, "3": {"Inspiratory Pressure": 33.34244932566607, "Tidal Volume": 3027.5994824607587, "PEEP": 8.857630366243326, "PIP": 33.92857801463594, "Mean Airway Pressure": 8.10262514131296, "Flow Rate": 0.11257487203612809}}
```

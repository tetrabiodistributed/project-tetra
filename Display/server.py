import sys
import time
import json

import zmq

from PatientTubingDescriptorCalculator \
    import PatientTubingDescriptorCalculator

NUMBER_OF_PATIENTS = 4

def poll_sensors():
    """Pulls data from the pressure and flow sensors"""

    # placeholder
    return [(i, i) for i in range(NUMBER_OF_PATIENTS)]

def main():

    patient_calcuators = []
    for _ in range(NUMBER_OF_PATIENTS):
        patient_calcuators.append(PatientTubingDescriptorCalculator())

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5000")
    running = True
    while running:
        try:
            sensorState = poll_sensors()
            patient_descriptors = {}
            for i in range(NUMBER_OF_PATIENTS):
                patient_calcuators[i].add_flow_rate_datum(sensorState[i][0])
                patient_calcuators[i].add_pressure_datum(sensorState[i][1])
                patient_descriptors.update({i:patient_calcuators[i]
                                              .descriptors})
            socket.send_multipart([b"", json.dumps(patient_descriptors)
                                            .encode("ascii")])
            time.sleep(1.0)
        except:
            running = False
            raise

if "__main__" == __name__:
    main()
    
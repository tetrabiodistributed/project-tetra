Feature: gets data from sensors

    Scenario: connects to the sensors that are connected
        Given some sensors are physically connected to the Pressure Sensor and Airflow Sensor PI Hat
        Then the software will determine which tubes have both pressure and airflow sensing
        Then the software will initialize and calibrate the sensors
        Then the software will return the state of the sensor to the user.

    Scenario: there are not enough sensors
        Given there are no tubes with both pressure and airflow sensing connected
        Then the software will raise an error

    Scenario: there are multiple airflow sensors on a single tube
        Given more than one airflow sensor is connected to a single tube
        Then the data from the worse sensor will be ignored

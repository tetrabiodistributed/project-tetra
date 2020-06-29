Feature: gets data from sensors

    Scenario: connects to the sensors that are connected
        Given there are these objects that represent these sensors
        When these sensors are initialized
        Then the software will calibrate the sensors
        Then the software will determine which tubes have both pressure and airflow sensing
        Then the software will return the state of the sensor to the user.

    Scenario: there are not enough sensors
        Given a set of functioning sensors
        And a set of malfunctioning or missing sensors
        When the software diagnostic is run
        Then an error "NotEnoughSensors" will be raised

    Scenario: there are multiple airflow sensors on a single tube
        # Not relevant to July 18; we'll only use Sensirion for that
        Given "SFM3300" sensor on a tube
        And "Mass Air Flow" sensor on a tube
        When data is read
        Then the data from "Mass Air Flow" will be used

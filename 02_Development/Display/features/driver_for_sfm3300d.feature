Feature: Driver for SFM3300-D Flow Sensor

    Scenario:
        Given an SFM3300-D Flow sensor is connected to hardware
        And the SFM3300-D is initialized
        Then you can collect flow data
        And you can collect a serial number

    Scenario: Can positively inquire about the sensor's presense
        Given an SFM3300-D Flow sensor is connected to hardware
        And the SFM3300-D is initialized
        Then you can check that the SFM3300-D is in fact present


    Scenario: Can negatively inquire about the sensor's presense
        Given an SFM3300-D Flow sensor is not connected to hardware
        And the SFM3300-D is initialized
        Then you can check that the SFM3300-D is in fact not present

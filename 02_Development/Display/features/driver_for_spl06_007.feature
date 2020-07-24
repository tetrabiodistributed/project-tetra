Feature: Driver for SPL06-007 Pressure Sensor

    Scenario: Collects valid data
        Given an SPL06-007 Pressure sensor is connected to hardware
        And the SPL06-007 is initialized
        When you set the sampling parameters
        And you set the op mode to Command
        Then you can collect pressure data
        And you can collect temperature data


    Scenario: Can positively inquire about the sensor's presense
        Given an SPL06-007 Pressure sensor is connected to hardware
        And the SPL06-007 is initialized
        Then you can check that the SPL06-007 is in fact present


    Scenario: Can negatively inquire about the sensor's presense
        Given an SPL06-007 Pressure sensor is not connected to hardware
        And the SPL06-007 is initialized
        Then you can check that the SPL06-007 is in fact not present

Feature: Calculating tubing descriptors

    Scenario: Calculating descriptors
        Given we can use sensor data
        Then we can calculate these descriptors
            | descriptor           |
            | Inspiratory Pressure |
            | Tidal Volume         |
            | PEEP                 |
            | Peak Pressure        |
            | Flow Rate            |

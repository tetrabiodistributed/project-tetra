Feature: Runs backend from a Docker image

@slow
Scenario:
    Given A running Docker image on port 8000
    Then there will be a JSON packet sent every 1.0 seconds
    And that JSON packet will have several keys named with integers
    And those keys will refer to a dictionary of these descriptors
        | descriptor           |
        | Inspiratory Pressure |
        | Tidal Volume         |
        | PEEP                 |
        | Peak Pressure        |
        | Flow Rate            |

Feature: Runs backend from a Docker image

<<<<<<< HEAD
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
=======
@wip
@slow
Scenario:
    Given a Docker image is built
    When that image is run on port 8000
    Then there will be a JSON packet sent every 1.0 seconds
>>>>>>> changed the sensors module so it will read data from a file when it's not run on a raspberry pi and added the start of a behave test to verify that the Docker image works.

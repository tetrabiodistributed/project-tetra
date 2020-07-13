Feature: Runs backend from a Docker image

@wip
@slow
Scenario:
    Given a Docker image is built
    When that image is run on port 8000
    Then there will be a JSON packet sent every 1.0 seconds

from behave import *

import server
import constants

@given("there are these objects that represent these sensors")
def step_impl(context):
    sensors = server.Sensors(constants.NUMBER_OF_PATIENTS)
    pass

@when("these sensors are initialized")
def step_impl(context):
    pass

@then("the software will calibrate the sensors")
def step_impl(context):
    pass

@then("the software will determine which tubes have both pressure and "
      "airflow sensing")
def step_impl(context):
    sensors = server.Sensors(constants.NUMBER_OF_PATIENTS)
    assert (len(sensors
               .tubes_with_enough_sensors()) == 
            constants.NUMBER_OF_PATIENTS)

@then("the software will return the state of the sensor to the user.")
def step_impl(context):
    sensors = server.Sensors(constants.NUMBER_OF_PATIENTS)
    datum = next(sensors.poll_sensors())
    assert len(datum) == constants.NUMBER_OF_PATIENTS

@given("a set of functioning sensors")
def step_impl(context):
    pass

@given("a set of malfunctioning or missing sensors")
def step_impl(context):
    pass

@when("the software diagnostic is run")
def step_impl(context):
    pass

@then("an error {error} will be raised")
def step_impl(context, error):
    pass

@given("{sensor} sensor on a tube")
def step_impl(context, sensor):
    pass

@when("data is read")
def step_impl(context):
    pass

@then("the data from {sensor} will be used")
def step_impl(context, sensor):
    pass

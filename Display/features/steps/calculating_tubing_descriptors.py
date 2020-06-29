from behave import *

import server
import constants


@given("there are sensors connected")
def step_impl(context):
    pass


@given("there is a calculator to parse sensor data")
def step_impl(context):
    a = server.Calculator(constants.NUMBER_OF_PATIENTS)
    assert context.failed is False


@when("data is requested from the sensors")
def step_impl(context):
    sensors = server.Sensors(constants.NUMBER_OF_PATIENTS)
    sensor_data = sensors.poll_sensors()


@then("the sensors yield all of these descriptors")
def step_impl(context):
    sensors = server.Sensors(constants.NUMBER_OF_PATIENTS)
    sensor_data = sensors.poll_sensors()
    calculator = server.Calculator(constants.NUMBER_OF_PATIENTS)
    calculator.add_datum(sensor_data)
    assert all(calculator.get_datum()[patient][row["descriptor"]] is not None
               for row in context.table
               for patient in range(constants.NUMBER_OF_PATIENTS))

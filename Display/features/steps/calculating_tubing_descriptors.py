from behave import given, when, then

import server
import constants


@given("there are sensors connected")
def step_impl(context):
    context.sensors = server.Sensors(1, 1, 1, 1)


@given("there is a calculator to parse sensor data")
def step_impl(context):
    context.calculator = server.Calculator()


@when("data is requested from the sensors")
def step_impl(context):
    context.sensor_data = context.sensors.poll_sensors()


@then("the sensors yield all of these descriptors")
def step_impl(context):
    sensors = server.Sensors(1, 1, 1, 1)
    sensor_datum = sensors.poll_sensors()
    calculator = server.Calculator()
    calculator.add_datum(sensor_datum)
    assert all(row["descriptor"] in calculator.get_datum()[patient]
               for row in context.table
               for patient in range(constants.NUMBER_OF_PATIENTS))

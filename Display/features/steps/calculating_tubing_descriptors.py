from behave import *

import server

@given("we can use sensor data")
def step_impl(context):

    sensor_data = next(server.poll_sensors(4))
    assert len(sensor_data) == 4 and all(len(datum) == 2
                                         for datum in sensor_data)

@then("we can calculate these descriptors")
def step_impl(context):

    NUMBER_OF_PATIENTS = 4
    sensor_data = server.poll_sensors(NUMBER_OF_PATIENTS)
    calculator = server.Calculator(NUMBER_OF_PATIENTS)
    calculator.add_datum(sensor_data)
    assert all(calculator.get_datum()[patient][row["descriptor"]] is not None
               for row in context.table for patient in range(4))

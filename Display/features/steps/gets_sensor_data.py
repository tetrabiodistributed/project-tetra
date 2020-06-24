from behave import *

@given("some sensors are physically connected to the Pressure Sensor "
       "and Airflow Sensor PI Hat")
def step_impl(context):

    pass

@then("the software will determine which tubes have both pressure and "
      "airflow sensing")
def step_impl(context):

    pass

@then("the software will initialize and calibrate the sensors")
def step_impl(context):

    pass

@then("the software will return the state of the sensor to the user.")
def step_impl(context):

    pass    

@given("there are no tubes with both pressure and airflow sensing "
       "connected")
def step_impl(context):

    pass

@then("the software will raise an error")
def step_impl(context):

    pass

@given("more than one airflow sensor is connected to a single tube")
def step_impl(context):

    pass

@then("the data from the worse sensor will be ignored")
def step_impl(context):

    pass

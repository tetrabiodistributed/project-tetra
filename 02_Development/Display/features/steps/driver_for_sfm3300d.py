from behave import given, when, then
import math

from sfm3300d import FlowSensor
from tca9548a import I2CMux
from rpi_check import is_on_raspberry_pi
import constants


@given("an SFM3300-D Flow sensor is connected to hardware")
def step_impl(context):
    if not is_on_raspberry_pi():
        context.scenario.skip("Cannot test that the sensor is present unless "
                              "this is run on hardware.")
        return


@given("the SFM3300-D is initialized")
def step_impl(context):
    context.mux = I2CMux(constants.SENSIRION_SENSOR_MUX_ADDRESS)
    context.mux.select_channel(1)
    context.flow_sensor = FlowSensor()


@then("you can collect flow data")
def step_impl(context):
    assert math.isfinite(context.flow_sensor.flow()), \
        "Fails to generate valid flow data."


@then("you can collect a serial number")
def step_impl(context):
    assert context.flow_sensor.serial_number() > 0, \
        "Fails to generate a valid serial number."


@then("you can check that the SFM3300-D is in fact present")
def step_impl(context):
    assert context.flow_sensor.is_present(), \
        "Fails to indicate the sensor is present when it is."


@given("an SFM3300-D Flow sensor is not connected to hardware")
def step_impl(context):
    if is_on_raspberry_pi():
        context.scenario.skip("Cannot automatically test that the "
                              "sensor is not present unless this is "
                              "run on hardware.")
        return


@then("you can check that the SFM3300-D is in fact not present")
def step_impl(context):
    assert not context.flow_sensor.is_present(), \
        "Fails to indicate the sensor is not present when it's not."

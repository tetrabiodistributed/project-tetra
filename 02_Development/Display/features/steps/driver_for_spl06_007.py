from behave import given, when, then

from spl06_007 import PressureSensor
from tca9548a import I2CMux
from rpi_check import is_on_raspberry_pi
import constants


@given("an SPL06-007 Pressure sensor is connected to hardware")
def step_impl(context):
    if not is_on_raspberry_pi():
        context.scenario.skip("Cannot test that the sensor is present "
                              "unless this is run on hardware.")
        return


@given("the SPL06-007 is initialized")
def step_impl(context):
    context.mux = I2CMux(constants.PRESSURE_SENSOR_MUX_ADDRESS)
    context.mux.select_channel(0)
    context.sensor = PressureSensor()


@when("you set the sampling parameters")
def step_impl(context):
    context.sensor.set_sampling(
        pressure_oversample=constants.PRESSURE_OVERSAMPLING,
        pressure_sampling_rate=constants.PRESSURE_SAMPLING_RATE,
        temperature_oversample=constants.TEMPERATURE_OVERSAMPLE,
        temperature_sampling_rate=constants.TEMPERATURE_SAMPLING_RATE)


@when("you set the op mode to {mode}")
def step_impl(context, mode):
    context.sensor.set_op_mode(mode)


@then("you can collect pressure data")
def step_impl(context):
    assert context.sensor.pressure() > 0, \
        "Fails to collect pressure data."


@then("you can collect temperature data")
def step_impl(context):
    absolute_zero_degC = -273.15
    assert context.sensor.temperature() > absolute_zero_degC, \
        "Fails to collect temperature data."


@then("you can check that the SPL06-007 is in fact present")
def step_impl(context):
    assert context.sensor.is_present(), \
        "Fails to indicate the sensor is present when it is."


@given("an SPL06-007 Pressure sensor is not connected to hardware")
def step_impl(context):
    if is_on_raspberry_pi():
        context.scenario.skip("Cannot automatically test that the "
                              "sensor is not present unless this is "
                              "run on hardware.")
        return


@then("you can check that the SPL06-007 is in fact not present")
def step_impl(context):
    assert not context.sensor.is_present(), \
        "Fails to indicate the sensor is not present when it's not."

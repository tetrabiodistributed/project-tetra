from behave import given, when, then
<<<<<<< HEAD
from behave.api.async_step import async_run_until_complete
import math
import websocket
import json
import time

import docker

import constants


@given("A running Docker image on port {port}")
def step_impl(context, port):
    context.port = port
=======

import docker


@given("a Docker image is built")
def step_impl(context):
    context.client = docker.from_env()
    context.image = context.client.images.build(
        path=".", tag="zmq_proxy:latest")


@when("that image is run on port {port}")
def step_impl(context, port):
    context.container_name = "zmq_proxy"
>>>>>>> changed the sensors module so it will read data from a file when it's not run on a raspberry pi and added the start of a behave test to verify that the Docker image works.
    context.client.containers.run("zmq_proxy:latest",
                                  name=context.container_name,
                                  detach=True,
                                  auto_remove=True,
<<<<<<< HEAD
                                  ports={f"{port}": port})
    time.sleep(1.2)  # give the container a moment to start up


@then("there will be a JSON packet sent every {t:f} seconds")
def step_impl(context, t):
    number_of_messages = 5
    uri = f"ws://localhost:{context.port}/ws"
    start_time = time.time()
    ws = websocket.create_connection(uri)
    for _ in range(number_of_messages):
        context.message = ws.recv()
    end_time = time.time()
    context.json = json.loads(context.message)
    assert math.isclose((end_time - start_time)/number_of_messages, t,
                        rel_tol=0.15), \
        "Fails to send packets at 1 Hz"


@then("that JSON packet will have several keys named with integers")
def step_impl(context):
    for i in range(constants.NUMBER_OF_PATIENTS):
        assert f"{i}" in context.json, \
            ("JSON packet doesn't have top-level keys formatted as "
             "expected.")


@then("those keys will refer to a dictionary of these descriptors")
def step_impl(context):
    for i in range(constants.NUMBER_OF_PATIENTS):
        for row in context.table:
            assert row["descriptor"] in context.json[f"{i}"], \
                "Patient descriptors aren't formatted as expected."
=======
                                  ports={"8000/tcp": port})


@then("there will be a JSON packet sent every {t} seconds")
def step_impl(context, t):
    context.client.containers.get(context.container_name).kill()
>>>>>>> changed the sensors module so it will read data from a file when it's not run on a raspberry pi and added the start of a behave test to verify that the Docker image works.

from behave import given, when, then
import math
import websocket
import json
import time

import constants


@given("A running Docker image on port {port}")
def step_impl(context, port):
    context.port = port
    context.client.containers.run(context.container_tag,
                                  name=context.container_name,
                                  detach=True,
                                  auto_remove=True,
                                  ports={f"{context.port}": context.port})
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

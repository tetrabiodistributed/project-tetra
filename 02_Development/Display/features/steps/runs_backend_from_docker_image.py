from behave import given, when, then

import docker


@given("a Docker image is built")
def step_impl(context):
    context.client = docker.from_env()
    context.image = context.client.images.build(
        path=".", tag="zmq_proxy:latest")


@when("that image is run on port {port}")
def step_impl(context, port):
    context.container_name = "zmq_proxy"
    context.client.containers.run("zmq_proxy:latest",
                                  name=context.container_name,
                                  detach=True,
                                  auto_remove=True,
                                  ports={"8000/tcp": port})


@then("there will be a JSON packet sent every {t} seconds")
def step_impl(context, t):
    context.client.containers.get(context.container_name).kill()

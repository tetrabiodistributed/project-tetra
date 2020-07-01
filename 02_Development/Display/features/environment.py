<<<<<<< HEAD
import docker


def before_all(context):
    context.client = docker.from_env()
    context.image = context.client.images.build(path=".",
                                                tag="zmq_proxy:latest")
    context.container_name = "zmq_proxy"


def after_all(context):
    try:
        context.client.containers.get(context.container_name).kill()
    except docker.errors.NotFound:
        pass
=======


def after_step(context, step):
    if step.status == "failed":
        try:
            context.client.containers.get(context.container_name).kill()
        except NameError:
            pass
>>>>>>> changed the sensors module so it will read data from a file when it's not run on a raspberry pi and added the start of a behave test to verify that the Docker image works.

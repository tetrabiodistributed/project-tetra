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

import docker


def before_all(context):
    context.client = docker.from_env()
    context.container_name = "zmq_proxy"
    context.tag = "zmq_proxy:latest"
    context.image = context.client.images.build(path=".",
                                                tag=context.tag)


def after_all(context):
    try:
        context.client.containers.get(context.container_name).kill()
    except docker.errors.NotFound:
        pass


def after_step(context, step):
    if step.status == "failed":
        try:
            context.client.containers.get(context.container_name).kill()
        except docker.errors.NotFound:
            pass

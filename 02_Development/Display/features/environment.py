

def after_step(context, step):
    if step.status == "failed":
        try:
            context.client.containers.get(context.container_name).kill()
        except NameError:
            pass

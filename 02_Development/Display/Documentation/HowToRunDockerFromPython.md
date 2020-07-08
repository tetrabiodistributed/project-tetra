How to Run a Docker Container from a Python Script
==================================================

Docker is a very useful tool for when you want to run an application from a known environment.  If you're developing a Docker container and testing the components within it outside the container, you may want to write a test program to validate your container.  The obvious way to do this in Python is by calling shell commands with `os.system()`.  But you can, in fact, use the Docker SDK to do this!

This snippet here
```python
import docker

client = docker.from_env()
image = client.images.build(
        path=".", tag="example:latest")
container_name = "example_container"
client.containers.run("example:latest",
                      name=container_name,
                      detach=True,
                      auto_remove=True,
                      ports={"8000/tcp": 8000})

# Test that it's working

client.containers.get(container_name).kill()
```
is equivalent to this shell script.
```bash
docker build -t example:latest .
docker run --rm -dp 8000:8000 --name example_container example:latest
# Test that it's working
docker kill example_container
```
You can learn more about the Docker SDK at https://docker-py.readthedocs.io/en/stable/.

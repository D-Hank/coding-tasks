import os
import docker

from docker.types import DeviceRequest, Mount

client = docker.from_env()

try:
    net = client.networks.get("vllm_net")
except docker.errors.NotFound:
    net = client.networks.create("vllm_net", driver="bridge")

cc = client.containers.run(
    image="qweneval:latest",
    network=net.name,
    # point the OpenAI SDK at vLLM by using this env var
    environment={
        "OPENAI_API_BASE": "http://vllm:8000/v1",
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    },
    # mount your app code in /app
    mounts=[Mount(target="/eval", source=os.getcwd() + "/eval", type="bind", read_only=True)],
    working_dir="/eval",
    command="python3 evaluate.py",
    remove=True,
    detach=False,
)

cc.kill()

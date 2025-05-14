import os
import docker

from docker.types import DeviceRequest, Mount

client = docker.from_env()

cc = client.containers.run(
    image="qweneval:latest",
    # point the OpenAI SDK at vLLM by using this env var
    environment={
        "OPENAI_API_BASE": "http://vllm:8000/v1",
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    },
    # mount your app code in /app
    mounts=[Mount(target="/eval", source=os.getcwd() + "/eval", type="bind", read_only=False)],
    working_dir="/eval",
    command="python3 evaluate.py",
    remove=True,
    detach=True,
    stdout=True,
    stderr=True
)

for line in cc.logs(stream=True):
    print(line.decode("utf-8").rstrip())

#cc.kill()

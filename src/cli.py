import docker
import time

from docker.types import DeviceRequest

image = "vllm/vllm-openai:latest"

model = "--model Qwen/Qwen2.5-Coder-0.5B-Instruct"
context_len = "--max_model_len 4096"
api_key = "--api_key EMPTY"

command = model + " " + context_len + " " + api_key

client = docker.from_env()

#try:
#    net = client.networks.get("vllm_net")
#except docker.errors.NotFound:
#    net = client.networks.create("vllm_net", driver="bridge")

container = client.containers.run(
    image,
    command=command,
    detach=True,
    remove=True,
    # Output
    stdout=True,
    #stderr=True,
    # -p
    ports={"8000/tcp" : 8000},
    # -v
    volumes={
        "/home/daihankun/.cache/huggingface": {
            "bind" : "/root/.cache/huggingface",
            "mode" : "rw"
        }
    },
    # --env
    environment={
        "HF_HUB_OFFLINE" : "1"
    },
    # --gpus all
    device_requests=[DeviceRequest(count=-1, capabilities=[["gpu"]])],
    # --ipc=host
    ipc_mode="host",
    #network=net.name
)

print("Server docker id:", container.short_id)

start_time = time.time()

for line in container.logs(stream=True):
    print(line.decode("utf-8").rstrip())
    end_time = time.time()
    elapse = end_time - start_time

    # 180 seconds
    #if elapse > 180.0:
    #    break

container.kill()

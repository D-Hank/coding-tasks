docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HF_HUB_OFFLINE=1" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model Qwen/Qwen2.5-Coder-0.5B-Instruct \
    --max_model_len 4096 \
    --api_key "EMPTY"

# max_model_len should be greater than output token len
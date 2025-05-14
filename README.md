# Coding Tasks

## Description

Someone's implementation for the coding tasks. See `./doc` for detailed information.

## User Guide

### Serving

Make sure your current dir is `src/` under the master folder, run:
```
./run.sh
```
on your remote target, which will serve vLLM in a docker instance.

### Inference

Run:
```
cd eval
python evaluate.py
```
on target (remember to turn off your proxies). Output programs will be saved as `samples.jsonl`.

### Evaluation

On the server side, build a docker by (You may need to set your proxies in Dockerfile if necessary):
```
docker build -t qweneval:latest .
```
Then use
```
evaluate_functional_correctness samples.jsonl
```
and the evaluation result will be `samples.jsonl_results.json`. Pass@k scores will be displayed in your terminal.

## Package Info

### vllm

0.8.5.post1

### docker

From vllm-openai:latest
Latest version: v0.8.6
Digest: sha256:c48cf118e1e6e39d7790e174d6014f7af5d06f79c2d29d984d11cbe2e8d414e7

## Reference

Self-written evaluation for Qwen:

https://zhuanlan.zhihu.com/p/721218072

Note that code extraction should be used.

Extraction rules for Qwen:

https://github.com/QwenLM/Qwen/blob/main/eval/evaluate_chat_humaneval.py
https://github.com/QwenLM/Qwen2.5-Coder/blob/main/qwencoder-eval/instruct/eval_plus/generate.py

Python regex:
https://blog.csdn.net/Q52099999/article/details/135736328
https://blog.csdn.net/weixin_57992300/article/details/138274664
https://blog.csdn.net/m0_58878709/article/details/143838698

Use docker with vLLM:

https://docs.vllm.ai/en/stable/deployment/docker.html

Docker SDK for Python:

https://docker-py.readthedocs.io/en/stable/

Docker network:

https://blog.csdn.net/2301_80163789/article/details/147163421

Python multiprocessing:
https://blog.csdn.net/riven78/article/details/147233715

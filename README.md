# Coding Tasks

## Description

Someone's implementation for the coding tasks. See `./doc` for detailed information.

## User Guide

Under the master folder, run:
```
cd src
python3 cli.py
```
where output programs will be saved as `samples.jsonl`. Then use
```
evaluate_functional_correctness samples.jsonl
```
and the evaluation result will be `samples.jsonl_results.json`. Pass@k scores will be displayed on command line.

## Reference

Self-written evaluation for Qwen:

https://zhuanlan.zhihu.com/p/721218072

Note that code extraction should be used.


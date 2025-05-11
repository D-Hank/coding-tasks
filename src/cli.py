import re
import textwrap

from typing import Dict

from vllm import LLM, SamplingParams
from human_eval.data import write_jsonl, read_problems


if __name__ == "__main__":

    model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

    # Pass the default decoding hyperparameters of Qwen1.5-32B-Chat
    # max_tokens is for the maximum length for generation.
    sampling_params = SamplingParams(temperature=0.01, top_p=0.8, top_k=20, repetition_penalty=1.05, max_tokens=1024)

    problems = read_problems()

    num_samples_per_task = 1
    task_ids = list(problems.keys())

    prompts = []
    for task_id in task_ids:
        problem = problems[task_id]
        snippet = problem["prompt"]
        entry_point = problem["entry_point"]
        # use humanevalpack prompt
        signature = re.search(
            rf"def\s+{entry_point}.*:.*\n", snippet
        )

        rest = snippet[signature.end() + 1 : ].strip()
        docstring = re.search(
            rf"(?:\"\"\"|''')(.*?)(?:\"\"\"|''')", rest, re.DOTALL
        )

        # Drop \n in the signature
        # Drop """ in docstring by using the first captured group
        prompt = (
            f"I'm trying to write a Python function with the signature of `{signature.group(0)[ : -1]}` to solve the following problem:\n"
            f"{docstring.group(1)}\n"
            f"I already have a code snippet. Note that I do not need test cases. Please help me complete my draft code below:\n"
            f"{snippet}"
        )

        prompts.append(prompt)

    # Input the model name or path. Can be GPTQ or AWQ models.
    llm = LLM(model=model_name)

    outputs = llm.generate(prompts, sampling_params)

    samples = []
    for i in range(len(task_ids)):
        task_id = task_ids[i]
        problem = problems[task_id]
        code = outputs[i].outputs[0].text
        samples.append(
            dict(task_id=task_id, completion=code)
        )

    write_jsonl("samples.jsonl", samples)

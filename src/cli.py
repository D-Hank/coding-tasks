import re
import os
import numpy as np

from typing import List, Dict

from vllm import LLM, SamplingParams
from human_eval.data import write_jsonl, read_problems


def generate_prompts(problems: Dict[int, Dict], task_ids: List[int], num_samples: int) -> List[str]:
    prompts = []
    for task_id in task_ids:
        problem = problems[task_id]
        snippet = problem["prompt"]
        entry_point = problem["entry_point"]
        # use humanevalpack prompt
        signature = re.search(
            rf"def\s+({entry_point}.*?):\s*\n", snippet
        )

        rest = snippet[signature.end() + 1 : ].strip()
        docstring = re.search(
            rf"(?:\"\"\"|''')(.*?)(?:\"\"\"|''')", rest, re.DOTALL
        )

        # Drop \n in the signature
        # Drop """ in docstring by using the first captured group
        prompt = (
            f"Write a Python function `{signature.group(1)}` to solve the following problem. You may need to import necessary libraries.\n"
            f"{docstring.group(1)}\n"
            f"{snippet}"
        )

        for i in range(num_samples): prompts.append(prompt)

    return prompts

def extract_code(answer: str, entry_point: str) -> str:
    # Pattern 1: in markdown code block
    code = re.search(
        rf'''
        ```python\n
        [\s\S]*
        def\s+{entry_point}.*:.*\n
        ([\s\S]*)
        ```
        ''',
        answer
    )
    # Pattern 2: not in markdown
    if code is None:
        code = re.search(
            rf'''
            [\s\S]*
            def\s+{entry_point}.*:.*\n
            ([\s\S]*)
            ''',
            answer
        )
    if code is not None:
        code = code.group(1)
    # Pattern 3: directly complete the snippet
    else:
        code = answer

    # Drop content after ``` if it is given since they are content out of the code box (chat content)
    return code.split("```")[0]

def process_outputs(answers: List, problems: Dict[int, Dict], task_ids: List[int], num_samples: int) -> List[Dict]:
    samples = []
    for i in range(len(task_ids)):
        task_id = task_ids[i]
        problem = problems[task_id]
        entry_point = problem["entry_point"]
        for s in range(num_samples):
            answer = answers[i * num_samples + s]
            #code = extract_code(answer, entry_point).split("```")[0]
            code = answer.split("```")[0].split("# Test ")[0].split("def check")[0].split("assert")[0]
            # Save raw answer for checking
            samples.append(
                dict(task_id=task_id, completion=code, response=answer)
            )

    return samples

if __name__ == "__main__":

    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

    # Pass the default decoding hyperparameters of Qwen1.5-32B-Chat
    # max_tokens is for the maximum length for generation.
    sampling_params = SamplingParams(temperature=0.01, top_p=0.8, top_k=20, repetition_penalty=1.05, max_tokens=1024)

    problems = read_problems()

    num_samples_per_task = 1
    task_ids = list(problems.keys())

    # Cached raw output
    if not os.path.exists("raw.npy"):
        prompts = generate_prompts(problems, task_ids, num_samples_per_task)

        # Input the model name or path. Can be GPTQ or AWQ models.
        llm = LLM(model=model_name)

        outputs = llm.generate(prompts, sampling_params)
        answers = [output.outputs[0].text for output in outputs]
        np.save("raw.npy", answers)

    else:
        answers = np.load("raw.npy")

    samples = process_outputs(answers, problems, task_ids, num_samples_per_task)

    write_jsonl("samples.jsonl", samples)

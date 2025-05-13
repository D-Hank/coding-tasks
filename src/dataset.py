import re

from typing import List, Dict


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
        rf"```python\n(.*?)```",
        answer, re.DOTALL
    )
    if code is not None:
        code = code.group(1)
        start_code = re.search(
            rf"^assert",
            code
        )

        # If this extracted code block is a test block, use the whole answer instead for subsequent extraction
        if start_code != None:
            code = answer

    # Pattern 2: directly complete the snippet
    else:
        code = answer

    # Remove signature if it appears at the beginning
    signature = re.search(
        rf"^def\s+({entry_point}.*?):\s*\n", code
    )
    if signature is not None:
        code = code[len(signature.group(0)) : ]

    # Drop content after ``` if it is given since they are content out of the code box, especially when llm directly fills the answer
    # Drop test cases
    code = code.split("```")[0].split("# Test ")[0].split("assert")[0].split("def check")[0]

    return code

def process_outputs(answers: List, problems: Dict[int, Dict], task_ids: List[int], num_samples: int) -> List[Dict]:
    samples = []
    for i in range(len(task_ids)):
        task_id = task_ids[i]
        problem = problems[task_id]
        entry_point = problem["entry_point"]
        for s in range(num_samples):
            answer = answers[i * num_samples + s]
            code = extract_code(answer, entry_point)
            #code = answer.split("```")[0].split("# Test ")[0].split("def check")[0].split("assert")[0]
            # Save raw answer for checking
            samples.append(
                dict(task_id=task_id, completion=code, response=answer)
            )

    return samples

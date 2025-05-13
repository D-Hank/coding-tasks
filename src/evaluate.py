import os
import numpy as np

from openai import OpenAI
from human_eval.data import write_jsonl, read_problems

from dataset import generate_prompts, process_outputs

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

if __name__ == "__main__":

    problems = read_problems()

    num_samples_per_task = 1
    task_ids = list(problems.keys())

    # Cached raw output
    if not os.path.exists("raw.npy"):
        prompts = generate_prompts(problems, task_ids, num_samples_per_task)

        # Build a client and interact with LLM
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )

        outputs = client.completions.create(
            model=model_name,
            prompt=prompts,
            temperature=0.01,
            top_p=0.8,
            max_tokens=1024,
            extra_body={
                "top_k": 20,
                "repetition_penalty": 1.05
            }
        )

        answers = [output.text for output in outputs.choices]
        np.save("raw.npy", answers)

    else:
        answers = np.load("raw.npy")

    samples = process_outputs(answers, problems, task_ids, num_samples_per_task)

    write_jsonl("samples.jsonl", samples)

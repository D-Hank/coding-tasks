from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
from human_eval.data import write_jsonl, read_problems

model_name = "Qwen/Qwen2.5-Coder-0.5B"
# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Pass the default decoding hyperparameters of Qwen1.5-32B-Chat
# max_tokens is for the maximum length for generation.
sampling_params = SamplingParams(temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.05, max_tokens=1024)

# Input the model name or path. Can be GPTQ or AWQ models.
llm = LLM(model=model_name)

# Print the outputs.
#for output in outputs:
#    prompt = output.prompt
#    generated_text = output.outputs[0].text
#    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

problems = read_problems()

num_samples_per_task = 1
task_ids = list(problems.keys())
prompts = [
    problems[task_id]["prompt"]
    for task_id in task_ids
    for _ in range(num_samples_per_task)
]

outputs = llm.generate(prompts, sampling_params)

samples = [
    dict(task_id=task_ids[i], completion=outputs[i].outputs[0].text)
    for i in range(len(task_ids))
]
write_jsonl("samples.jsonl", samples)
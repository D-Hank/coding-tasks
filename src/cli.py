from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

model_name = "Qwen/Qwen2.5-Coder-0.5B"
# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Pass the default decoding hyperparameters of Qwen1.5-32B-Chat
# max_tokens is for the maximum length for generation.
sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05, max_tokens=1024)

# Input the model name or path. Can be GPTQ or AWQ models.
llm = LLM(model=model_name)

# Prepare your prompts
prompt = "#write a quick sort algorithm.\ndef quick_sort("

# generate outputs
outputs = llm.generate([prompt], sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
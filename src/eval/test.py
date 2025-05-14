from human_eval.data import read_problems

mine = read_problems("result.jsonl")
base = read_problems("samples.jsonl_results.jsonl")

task_ids = mine.keys()

for task in task_ids:
    m = mine[task]
    b = base[task]
    if m["passed"] != b["passed"]:
        print(task)

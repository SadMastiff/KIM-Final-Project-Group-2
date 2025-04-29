import pandas as pd
import requests
import time
import math
# ──────────────────────────────── CONFIG ────────────────────────────────
CSV_FILE        = "Final_Report.csv"     # source data (Must be CSV)
OUTPUT_CSV      = "Final_Report.csv"                # output CSV (Could be a different format but code would need to be updated)
MODEL_NAME      = "llama3"                          # Model called by the function (Must match the model you pulled)
BATCH_SIZE      = 5                                 # 5 abstracts per batch (How many elements chosen from the abstract csv at a time.)
CTX_SIZE        = 6_000                             # context window    (Size of the batch of abstracts)
MAX_PREDICT     = 2_048                               # max output tokens (Size of the output of the analysis)
PAUSE_SECS      = 2                                 # pause between batches
TEMPERATURE     = 0.2                               # Chat Temperature (How often low probability words will be choosen)
TOP_P           = 0.9                               # Top_P of Chat (Tells what words are in the pool to be selected)         

# ────────────────────────────────────────────────────────────────────────

# 1. Read the CSV (expects columns 'pmids' and 'output')
AbsTable = pd.read_csv(CSV_FILE)
pmids = AbsTable["pmids"].fillna("").tolist()
abstracts = AbsTable["output"].fillna("").tolist()

# 2. Instruction block 
initial_prompt = """
You will be looking at analysis of research.
Your job is to read through the analysis and make a master report on what the research analysis says would be beneficial to a company producing a standing desk with a built in treadmill.
Your final report should be professional and formal.
Your goal is to find the best information for the company and product to succeed.
Your report should be APA format.
You should write as much as you feel is necessary to convey your point.

Summaries:"""

# 3. Split into batches
batch_records = []  # will hold each batch's PMIDs and model outputs

for i in range(0, len(abstracts), BATCH_SIZE):
    batch_pmids = pmids[i:i+BATCH_SIZE]
    batch_abstracts = abstracts[i:i+BATCH_SIZE]

    print(f"Processing batch: {i//BATCH_SIZE + 1} of {math.ceil(len(abstracts)/5)}...")

    # Build the batch prompt
    zipped_absPMID = zip(batch_pmids, batch_abstracts)
    batch_prompt = initial_prompt
    for abs_id, abs_text in zipped_absPMID:
        batch_prompt += f"\nAbstract {abs_id}:\n{abs_text}\n"

    # Send to Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": batch_prompt,
                "stream": False,
                "options": {
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "num_ctx": CTX_SIZE,
                    "num_predict": MAX_PREDICT,
                },
            },
            timeout = 60*math.ceil(len(abstracts)/5) # Timeout for the program in case Ollama breaks (1 minute * Number of inputs)
        )
        response.raise_for_status()
        model_output = response.json()["response"]
    except Exception as e:
        model_output = f"Error: {e}"

    # Record this batch
    batch_records.append({
        "pmids": "; ".join(str(pmid) for pmid in batch_pmids),  # save PMIDs as one semi-colon-separated string
        "output": model_output,
    })

    time.sleep(PAUSE_SECS)

# 4. Save to a new CSV
output_df = pd.DataFrame(batch_records)
output_df.to_csv(OUTPUT_CSV, index=False)


# 5. Create a master summary with separators
print("Building Master summary: ")

# Build the master summary with separation
separator = "\n\n" + "*" * 200 + "\n\n"  # asterisks line

all_outputs = separator.join(
    record["output"] for record in batch_records
)

# Save the master summary to its own file
with open("master_report.txt", "w", encoding="utf-8") as f:
    f.write(all_outputs)

print("Master report saved to master_report.txt")


print(f"\nDone Analyzing. Batches written to {OUTPUT_CSV}")

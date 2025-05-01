To use this software you will need the following:

Requirements:
- A dedicated GPU
- Ollama installed
- Python installed 
- Biopython installed

Instructions:

The system of gathering the information and analyzing it works in this order:

PubMedAPIGatherer:

1. Before you can run "PubMedAPIGatherer.py", in the file "email.txt" (if it is missing make one) add your email to the file.
   The only thing in the file should be your email.
   
   Example:
   [File Begin]JohnDoe@email.com[File End]
   
2. Edit the config file for search terms and number of abstracts to search for.

3. CD into the directory PubMedAPIGatherer.py is held in.

4. Run: Python './PubMedAPIGatherer.py'

LlamaStudyAnalyzer:

1. (If not started) Start the Ollama server in PowerShell via running the command: Ollama serve

2. (optional)Check the config in code before running.

3. CD into the directory for LlamaStudyAnalyzer.py
   
4. Run: Python './LlamaStudyAnalyzer.py'

Final Analysis Batch:

1. (If not started) Start the Ollama server in PowerShell via running the command: Ollama serve

2. (optional)Check config in code before running.

3. CD into the director for LlamaStudyAnalyzer.py
   
4. Run: Python './Final Analysis Batch.py'

(Optional) Final Analysis Loop:

Final Analysis Loop is a looped batch analysis of the output of Final Analysis Batch.

It allows the user to loop through the summaries of the studies to produce one full summary of all the summaries.

This is not necessary unless you want a generalized report on what the data says. You will lose some nuance in the reports if you condense the reports.

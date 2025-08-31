# Call Summarizer Bot

A command-line Conversational AI Copilot for summarizing and querying your call transcripts using retrieval-augmented generation (RAG) and large language models (LLMs).

## Features
- Ingest call transcripts from plain text files
- Chunk, embed, and store transcripts in a persistent vector database
- Query your calls using natural language
- Retrieve and summarize relevant call segments using LLMs
- Context-aware filtering for focused search
- Simple, interactive CLI with helpful commands

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/suyash143/call_summarizer_bot
   cd call_summarizer_bot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **IMPORTANT**
You will be required to change the current LLM model because the current LLM model used in this code is locally deployed on a GPU machine, Please go to core/llm.py 

## Usage

### Start the CLI
```bash
python main.py
```

### Get Help
start by typing help in cli to get better idea of Bots ability.
```bash
help
```

### Ingest a Call Transcript

Provide the path to a plain text transcript file:
```bash
ingest a new call transcript from <path-to-file.txt>
```

### List All Ingested Calls
```bash
list my call ids
```

### Select a Call for Focused Querying
```bash
select call <file_path>
```

### Clear Selected Call (Search All Calls)
```bash
clear selected call
```

### Ask Questions About Your Calls
Type any natural language question:
```bash
What were the main objections or hurdle that happened in the last call?
Summarize the pricing discussion.
```



---

## Example Workflow
1. Ingest one or more transcript files.
2. List available calls to see their file ids.
3. Ask questions or request summaries about your calls.
4. (Optional) Select a specific call for focused queries.
5. Use `clear selected call` to broaden your search again.

---

## CLI Commands Reference
Currently as the model was locally hosted function calling is not added hence the commands need to be an exact match
- `ingest a new call transcript from <path>`: Ingest a transcript file
- `list my call ids`: List all ingested call file paths
- `select call <file_path>`: Focus queries on a specific call
- `clear selected call`: Remove filter to search all calls
- `help`: Show help and current selection
- `<any question>`: Query or summarize your calls
- `exit`: Exit the CLI

---

## Project Structure
```
call_summarizer_bot/
│
├── cli/                # CLI interface and related text
│   ├── __init__.py
│   ├── cli.py
│   └── cli_text.py
│
├── core/               # Core logic: database, ingestion, retrieval, LLM, utils
│   ├── __init__.py
│   ├── db.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── llm.py
│   └── utils.py
│
├── config/             # Configuration and prompts
│   ├── __init__.py
│   ├── config.py
│   └── prompts.py
│
├── data/               # Example transcripts and user data
│   ├── 1_demo_call.txt
│   ├── 2_pricing_call.txt
│   ├── 3_objection_call.txt
│   └── 4_negotiation_call.txt
│
├── chroma/             # Vector DB storage (auto-generated, gitignored)
│
├── main.py             # Entry point
├── requirements.txt
├── README.md
└── README_PROBLEM_STATEMENT.md
```

---

## Customization & Extensibility
- Ability to Swap out the LLM or embedding provider by editing `core/llm.py`.
- Adjust chunking or metadata schema in `core/ingest.py` and `core/db.py`.
- Add new CLI commands in `cli/cli.py` for advanced workflows.

---

## Troubleshooting & FAQ
- **Database files change after each query:**
  - The `chroma/` directory contains the vector database and is updated on every operation. Add it to your `.gitignore` to avoid tracking changes.
- **No results found:**
  - Make sure you have ingested at least one transcript file.
- **LLM Error:**
  - Ensure to replace your LLM endpoint in the config file and edit the model hosted to get the correct generation

---

For further customization or support, please refer to the code comments or open an issue.

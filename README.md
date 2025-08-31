# Call Summarizer Bot

A CLI-based Conversational AI Copilot for summarizing and querying your call transcripts using retrieval-augmented generation (RAG) and large language models (LLMs).

## Features
- Ingest call transcripts from text files
- Chunk, embed, and store transcripts in a vector database (FAISS)
- Query your calls using natural language
- Retrieve and summarize relevant call segments using LLMs
- Simple command-line interface with helpful commands

## Project Structure
- `main.py`: Entry point; launches the CLI
- `cli.py`: Command-line interface for ingesting and querying calls
- `llm.py`: Embedding and LLM query logic
- `db.py`: In-memory vector database using FAISS
- `ingest.py`: Transcript ingestion, chunking, and embedding
- `retriever.py`: Retrieves relevant transcript chunks for a query
- `utils.py`: Utility functions (e.g., text chunking)

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Set up your `.env` file for any required API keys or endpoints

## Usage
Run the CLI:
```bash
python main.py
```

### CLI Commands
- `ingest a new call transcript from <path>`: Ingests a transcript file
- `list my call ids`: Lists all ingested call files
- `<ask any question about your calls>`: Ask any question; the bot will retrieve and summarize relevant segments
- `help`: Show available commands
- `exit`: Quit the CLI

## Example
```
> ingest a new call transcript from 1_demo_call.txt
Ingested 10 chunks from 1_demo_call.txt
> list my call ids
1_demo_call.txt
> What were the main objections in the call?
... (LLM-generated answer)
```

## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies

## Notes
- The LLM endpoint and model can be configured in `llm.py`
- This project is for demo/research purposes and does not persist data between runs

## License
MIT


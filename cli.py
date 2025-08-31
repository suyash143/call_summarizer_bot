# CLI interface for the chatbot

from llm import Embedder, LLM
from db import DB
from ingest import Ingestor
from retriever import Retriever
from rich import print
from cli_text import CLI_BANNER, CLI_INTRO, CLI_HELP
from config import *


def main():
    embedder = Embedder()
    db = DB()
    ingestor = Ingestor(embedder, db)
    retriever = Retriever(embedder, db)
    llm = LLM()
    # Initialize call_files from persistent DB
    call_files = set(db.get_all_file_paths())

    print(CLI_BANNER)
    print(CLI_INTRO)

    while True:
        try:
            cmd = input("[bold blue]> [/bold blue]").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not cmd:
            continue
        if cmd == "exit":
            break
        if cmd == "help":
            print(CLI_HELP)
            continue
        if cmd.startswith("ingest a new call transcript from "):
            path = cmd[len("ingest a new call transcript from "):].strip()
            try:
                n = ingestor.ingest(path)
                call_files.add(path)
                print(f"Ingested {n} chunks from {path}")
            except Exception as e:
                print(f"[red]Error ingesting:[/red] {e}")
            continue
        if cmd == "list my call ids":
            call_files = set(db.get_all_file_paths())
            if not call_files:
                print("No calls ingested yet.")
            else:
                for f in call_files:
                    print(f)
            continue
        results = retriever.retrieve(cmd, top_k=10)
        if not results:
            print("No relevant transcript segments found. Try ingesting a call transcript first.")
            continue
        context = "\n".join([r['text'] for r in results])
        prompt = f"Answer the following question using only the provided transcript segments. Cite the relevant segment(s) in your answer.\nQuestion: {cmd}\nTranscript Segments:\n{context}"
        answer = llm.ask(prompt)
        print(f"[bold]Answer:[/bold] {answer}")
        print("[bold]Source Segments:[/bold]")
        for r in results:
            print(f"- {r['text']}")

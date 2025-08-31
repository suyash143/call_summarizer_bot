
from core.llm import Embedder, LLM
from core.db import DB
from core.ingest import Ingestor
from core.retriever import Retriever
from rich.console import Console
from rich.prompt import Prompt
from cli.cli_text import CLI_BANNER, CLI_INTRO, CLI_HELP, CLI_PROMPT, CLI_ERROR_STYLE, CLI_INFO_STYLE, CLI_ANSWER_STYLE, CLI_SOURCE_STYLE
from config.prompts import PROMPT_TEMPLATE
from config.config import *

def main():
    embedder = Embedder()
    db = DB()
    ingestor = Ingestor(embedder, db)
    retriever = Retriever(embedder, db)
    llm = LLM()
    call_files = set(db.get_all_file_paths())
    console = Console()
    selected_file = None
    console.print(CLI_BANNER)
    console.print(CLI_INTRO)

    first_interaction = True
    while True:
        if not first_interaction:
            console.rule(style="dim")
        else:
            first_interaction = False
        try:
            cmd = Prompt.ask(CLI_PROMPT, console=console).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nExiting.", style=CLI_INFO_STYLE)
            break
        if not cmd:
            continue
        if cmd == "exit":
            break
        if cmd == "help":
            console.print(CLI_HELP + "\n[bold]Advance Filteration commands:[/bold]\n- select call <file_path>\n- clear selected call", style=CLI_INFO_STYLE)
            if selected_file:
                console.print(f"[bold]Currently selected call:[/bold] {selected_file}", style=CLI_INFO_STYLE)
            else:
                console.print("[bold]Currently selected call:[/bold] None (searching all calls)", style=CLI_INFO_STYLE)
            continue
        if cmd.startswith("ingest a new call transcript from "):
            path = cmd[len("ingest a new call transcript from "):].strip()
            try:
                n = ingestor.ingest(path)
                call_files.add(path)
                console.print(f"Ingested {n} chunks from {path}", style=CLI_INFO_STYLE)
            except Exception as e:
                console.print(f"Error ingesting: {e}", style=CLI_ERROR_STYLE)
            continue
        if cmd == "list my call ids":
            call_files = set(db.get_all_file_paths())
            if not call_files:
                console.print("No calls ingested yet.", style=CLI_INFO_STYLE)
            else:
                for f in call_files:
                    console.print(f, style=CLI_INFO_STYLE)
            continue
        if cmd.startswith("select call "):
            file_candidate = cmd[len("select call "):].strip()
            if file_candidate in call_files:
                selected_file = file_candidate
                console.print(f"Selected call: {selected_file}", style=CLI_INFO_STYLE)
            else:
                console.print(f"File not found: {file_candidate}", style=CLI_ERROR_STYLE)
            continue
        if cmd == "clear selected call":
            selected_file = None
            console.print("Cleared selected call. All calls will be searched.", style=CLI_INFO_STYLE)
            continue
        metadata_filter = {'file_path': selected_file} if selected_file else None
        results = retriever.retrieve(cmd, top_k=10, metadata_filter=metadata_filter)
        if not results:
            console.print("No relevant transcript segments found. Try ingesting a call transcript first.", style=CLI_ERROR_STYLE)
            continue
        context = "\n".join([r['text'] for r in results])
        prompt = PROMPT_TEMPLATE.format(context=context, question=cmd)
        answer = llm.ask(prompt)
        console.print(f"[bold]Answer:[/bold] [green]{answer}[/green]", style=CLI_ANSWER_STYLE)
        console.print("[bold]Source Segments:[/bold]", style=CLI_SOURCE_STYLE)
        for r in results:
            console.print(f"- {r['text']}", style=CLI_SOURCE_STYLE)
        console.rule(style="dim")

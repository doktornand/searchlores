import typer

from rich import print

from searchlores.core.engine import InvestigationEngine
from searchlores.plugins.builtin.authority import AuthorityDetector

app = typer.Typer()

@app.command()
def investigate(prompt: str):
    engine = InvestigationEngine()
    engine.register(AuthorityDetector())
    result = engine.run(prompt)
    print(result.findings)
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
import json

from searchlores.core.engine import InvestigationEngine
from searchlores.plugins.builtin.authority import AuthorityDetector, AssumptionExtractor, ContradictionFinder, OmissionDetector, NarrativeArcheologist, CognitiveGenealogist
from searchlores.graph.searchmap import SearchMap

app = typer.Typer(help="Searchlores Ultimate — Archéologie Cognitive")
console = Console()

@app.command()
def investigate(
    prompt: str = typer.Argument(..., help="Le prompt à excaver"),
    depth: str = typer.Option("full", help="Profondeur : surface | deep | full"),
    export: str = typer.Option(None, help="Exporter la Search Map (mermaid|json)")
):
    engine = InvestigationEngine()

    engine.register(AuthorityDetector())
    engine.register(AssumptionExtractor())
    engine.register(ContradictionFinder())

    if depth in ["deep", "full"]:
        engine.register(OmissionDetector())
        engine.register(NarrativeArcheologist())

    if depth == "full":
        engine.register(CognitiveGenealogist())

    context = engine.run(prompt)

    console.print(Panel(f"[bold cyan]{prompt}[/bold cyan]", title="🔍 PROMPT EXCAVÉ", border_style="cyan"))

    table = Table(title="Strates Archéologiques")
    table.add_column("Strate", style="magenta")
    table.add_column("Plugin", style="green")
    table.add_column("Découverte", style="yellow")

    for layer in context.layers:
        findings_str = json.dumps(layer['findings'], indent=2)[:100]
        table.add_row(layer['stratum'], layer['plugin'], findings_str)

    console.print(table)

    if context.contradictions:
        console.print("\n[bold red]⚡ TENSIONS DÉTECTÉES :[/bold red]")
        for c in context.contradictions:
            console.print(f"  • {c['tension']} — {c['description']}")

    if context.omissions:
        console.print(f"\n[bold dim]🔇 DIMENSIONS SILENCIEUSES : {', '.join(context.omissions)}[/bold dim]")

    if context.power_vectors:
        console.print("\n[bold red]⚔️ VECTEURS DE POUVOIR :[/bold red]")
        for v in context.power_vectors:
            console.print(f"  → {v}")

    if export == "mermaid":
        sm = SearchMap(context)
        console.print("\n[bold]📊 SEARCH MAP (Mermaid) :[/bold]")
        console.print(sm.to_mermaid())
    elif export == "json":
        console.print(json.dumps(context.to_searchmap(), indent=2))

@app.command()
def compare(
    prompts: List[str] = typer.Argument(..., help="Les prompts à comparer")
):
    engine = InvestigationEngine()
    engine.register(AuthorityDetector())
    engine.register(AssumptionExtractor())
    engine.register(OmissionDetector())

    analysis = engine.comparative_analysis(prompts)

    console.print(Panel("[bold]ANALYSE COMPARATIVE SYSTÉMIQUE[/bold]", border_style="blue"))

    tree = Tree("🔬 Résultats")

    shared = tree.add("🎯 Présupposés Partagés")
    for a in analysis["shared_assumptions"]:
        shared.add(f"[green]{a}[/green]")

    divergent = tree.add("⚡ Autorités Divergentes")
    for a in analysis["divergent_authorities"]:
        divergent.add(f"[yellow]{a}[/yellow]")

    systemic = tree.add("🔇 Silences Systémiques")
    for s in analysis["systemic_omissions"]:
        systemic.add(f"[dim]{s}[/dim]")

    console.print(tree)

@app.command()
def lore_inspect(lore_file: str = typer.Argument(..., help="Chemin vers le fichier .lore")):
    import yaml
    from searchlores.lore.models import Lore

    with open(lore_file) as f:
        data = yaml.safe_load(f)

    lore = Lore(**data)

    console.print(Panel(f"[bold]{lore.metadata.name}[/bold]", title="📜 LORE", border_style="purple"))

    metrics = Table(title="Métriques Épistémologiques")
    metrics.add_column("Dimension")
    metrics.add_column("Count")
    metrics.add_column("Densité")

    total = (len(lore.investigation.assumptions) +
             len(lore.investigation.myths) +
             len(lore.investigation.vectors) +
             len(lore.investigation.questions) +
             len(lore.investigation.counter_questions))

    metrics.add_row("Hypothèses", str(len(lore.investigation.assumptions)), "🔴" * min(5, len(lore.investigation.assumptions)))
    metrics.add_row("Mythes", str(len(lore.investigation.myths)), "🟠" * min(5, len(lore.investigation.myths)))
    metrics.add_row("Vecteurs", str(len(lore.investigation.vectors)), "🟡" * min(5, len(lore.investigation.vectors)))
    metrics.add_row("Questions", str(len(lore.investigation.questions)), "🟢" * min(5, len(lore.investigation.questions)))
    metrics.add_row("Contre-questions", str(len(lore.investigation.counter_questions)), "🔵" * min(5, len(lore.investigation.counter_questions)))
    metrics.add_row("Réponses interdites", str(len(lore.investigation.forbidden_answers)), "⚫" * min(5, len(lore.investigation.forbidden_answers)))

    console.print(metrics)

    transgression_score = len(lore.investigation.counter_questions) + len(lore.investigation.forbidden_answers)
    console.print(f"\n[bold]Score de Transgression Épistémologique : {transgression_score}/10[/bold]")

if __name__ == "__main__":
    app()
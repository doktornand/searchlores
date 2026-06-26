from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

@dataclass
class InvestigationContext:
    prompt: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    findings: Dict[str, Any] = field(default_factory=dict)
    layers: List[Dict] = field(default_factory=list)
    contradictions: List[Dict] = field(default_factory=list)
    power_vectors: List[str] = field(default_factory=list)
    omissions: List[str] = field(default_factory=list)

    def add_layer(self, name: str, findings: Dict, plugin: str):
        self.layers.append({
            "stratum": name,
            "plugin": plugin,
            "timestamp": datetime.now().isoformat(),
            "findings": findings
        })

    def to_searchmap(self) -> Dict:
        return {
            "origin": self.prompt,
            "strata": self.layers,
            "contradictions": self.contradictions,
            "power_analysis": self.power_vectors,
            "silences": self.omissions,
            "archaeological_depth": len(self.layers)
        }

class Plugin(ABC):
    name: str = "base"
    stratum: str = "surface"

    @abstractmethod
    def run(self, context: InvestigationContext) -> None:
        pass

class InvestigationEngine:
    def __init__(self):
        self.plugins: List[Plugin] = []
        self.history: List[InvestigationContext] = []

    def register(self, plugin: Plugin):
        self.plugins.append(plugin)
        return self

    def run(self, prompt: str) -> InvestigationContext:
        context = InvestigationContext(prompt=prompt)
        print(f"\n🔍 [ARCHÉOLOGIE] Excavation du prompt : '{prompt[:80]}...'\n")

        for plugin in self.plugins:
            print(f"  ⛏️  Strate {plugin.stratum.upper()} — {plugin.name}")
            plugin.run(context)
            if plugin.name in context.findings:
                context.add_layer(
                    plugin.stratum,
                    {plugin.name: context.findings[plugin.name]},
                    plugin.name
                )

        self.history.append(context)
        return context

    def comparative_analysis(self, prompts: List[str]) -> Dict:
        contexts = [self.run(p) for p in prompts]
        return {
            "shared_assumptions": self._find_intersections(c.findings.get("assumptions", []) for c in contexts),
            "divergent_authorities": self._find_divergences(c.findings.get("authority", []) for c in contexts),
            "systemic_omissions": self._find_intersections(c.omissions for c in contexts),
            "power_constellations": list(set(sum([c.power_vectors for c in contexts], [])))
        }

    def _find_intersections(self, iterables):
        sets = [set(x) for x in iterables if x]
        return list(set.intersection(*sets)) if sets else []

    def _find_divergences(self, iterables):
        all_items = set()
        for items in iterables:
            all_items.update(items)
        return list(all_items)
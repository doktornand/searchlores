# Searchlores

> *"The Search Is The Program. The Ontology Is The Map."*
>
> — In memoriam Fravia (1952–2009)

```
searchlores investigate "You are an expert in artificial intelligence. Explain why LLMs understand language."
```

```yaml
prompt_archaeology:
  assumptions:
    - expertise exists
    - understanding is defined
    - understanding is measurable
  authority:
    - expert
  omissions:
    - token prediction
    - hallucinations
  counter_prompts:
    - Explain why LLMs do not understand language.
    - Compare understanding and prediction.
```

---

**Searchlores** is a Python framework for *Fravian Cognitive Archaeology* — the systematic deconstruction of prompts, narratives, and concepts as epistemological artifacts. Rather than asking *"how do I write a better prompt?"*, Searchlores asks: *"what hidden worldview produced this prompt?"*

Conceived as a spiritual successor to [Fravia's searchlores.com](https://github.com/soxoj/FRAVIA), this project applies the spirit of classical search theory — skepticism, lateral thinking, and layered inquiry — to the age of language models, knowledge graphs, and cognitive cartography.

---

## Table des matières

- [Philosophy](#philosophy)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Concepts fondamentaux](#concepts-fondamentaux)
  - [Lore](#lore)
  - [Investigation Engine](#investigation-engine)
  - [Plugins](#plugins)
  - [Archaeology Modules](#archaeology-modules)
  - [Graph & Search Maps](#graph--search-maps)
- [RFC Specification Stack](#rfc-specification-stack)
- [Structure du projet](#structure-du-projet)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Hommage](#hommage)

---

## Philosophy

Fravia did not teach people to use search engines.
He taught people to *think about* search engines.

Searchlores inherits this posture.

Every prompt is an archaeological site.
Every claim is a layer of sediment.
Every concept is a ruin waiting to be excavated.

The framework operates across five strata of inquiry:

```
Prompt Archaeology       ← What assumptions live inside the prompt?
        ↓
Narrative Archaeology    ← What story is the prompt trying to tell?
        ↓
Cognitive Archaeology    ← What concepts make the story possible?
        ↓
Ontology Builder         ← How do those concepts relate to each other?
        ↓
Cognitive Atlas          ← How does this domain connect to all others?
```

**Searchlores does not answer questions. Searchlores teaches exploration.**

---

## Architecture

```
searchlores/
├── core/
│   ├── engine.py          ← InvestigationEngine — orchestre les plugins
│   ├── context.py         ← InvestigationContext — état partagé de l'enquête
│   └── report.py          ← Génération de rapports structurés
├── lore/
│   ├── models.py          ← Modèles Pydantic : Lore, Investigation, Metadata
│   ├── loader.py          ← Chargement YAML → objets Lore validés
│   └── validator.py       ← Validation structurelle des Lores
├── plugins/
│   ├── base.py            ← Plugin ABC (interface commune)
│   ├── manager.py         ← Gestionnaire de plugins
│   └── builtin/
│       ├── authority.py   ← Détection d'autorités rhétoriques
│       ├── assumptions.py ← Extraction d'hypothèses implicites
│       └── contradictions.py ← Identification de contradictions
├── archaeology/
│   └── prompt.py          ← Module Prompt Archaeology
├── graph/
│   ├── searchmap.py       ← Search Maps conceptuelles
│   ├── mermaid.py         ← Export Mermaid
│   └── graphviz.py        ← Export Graphviz
└── cli/
    └── main.py            ← Interface CLI (Typer + Rich)
```

### Flux d'exécution

```
Prompt
  │
  ▼
InvestigationEngine.run(prompt)
  │
  ├── Plugin 1 : AuthorityDetector
  ├── Plugin 2 : AssumptionExtractor
  ├── Plugin 3 : ContradictionFinder
  │   ...
  ▼
InvestigationContext.findings
  │
  ▼
Report / Search Map / Ontology
```

---

## Installation

**Prérequis :** Python ≥ 3.11

```bash
git clone https://github.com/doktornand/searchlores.git
cd searchlores
pip install -e .
```

### Dépendances

| Paquet       | Rôle                                          |
|--------------|-----------------------------------------------|
| `pydantic`   | Validation et modélisation des Lores          |
| `networkx`   | Graphes conceptuels et Search Maps            |
| `pyyaml`     | Chargement des fichiers `.lore`               |
| `rich`       | Affichage terminal enrichi                    |
| `typer`      | Interface CLI déclarative                     |
| `jinja2`     | Templates de rapports                         |

---

## Quickstart

### Analyser un prompt

```bash
searchlores investigate "You are an expert in AI. Explain why LLMs understand language."
```

### Charger et utiliser un Lore

```python
from searchlores.lore.loader import load_lore
from searchlores.core.engine import InvestigationEngine
from searchlores.plugins.builtin.authority import AuthorityDetector

lore = load_lore("lores/llm.lore")
engine = InvestigationEngine()
engine.register(AuthorityDetector())

context = engine.run("AI experts agree that large language models are transforming education.")
print(context.findings)
# → {'authority': ['expert']}
```

### Anatomie d'un fichier `.lore`

```yaml
version: "1.0"

metadata:
  name: LLM Investigation
  author: Searchlores Academy
  version: "1.0"

investigation:
  assumptions:
    - intelligence
    - understanding
    - reasoning

  myths:
    - ai_thinks
    - ai_understands

  vectors:
    - cognition
    - economics
    - regulation

  questions:
    - Who benefits?
    - Who loses?
    - What assumptions exist?
```

Un fichier `.lore` est une **discipline d'investigation encapsulée** : il ne contient pas des réponses, mais des angles d'attaque, des mythes à déconstruire, et des questions à poser.

---

## Concepts fondamentaux

### Lore

Un `Lore` est l'unité de base de connaissance investigatrice dans Searchlores. Ce n'est pas un fichier de configuration ordinaire : c'est une *méthodologie d'enquête encodée sous forme d'artefact*.

```
Lore
 ├── Metadata       (nom, auteur, version)
 └── Investigation
      ├── assumptions   (hypothèses implicites à détecter)
      ├── myths         (récits dominants à déconstruire)
      ├── vectors       (axes d'investigation)
      └── questions     (questions génératrices)
```

Les Lores sont chargés, validés et composables : un Lore peut hériter d'un autre, fusionner avec des Lore-packs thématiques, ou être audité pour détecter ses propres angles morts.

### Investigation Engine

`InvestigationEngine` est l'orchestrateur central. Il reçoit un prompt textuel, instancie un `InvestigationContext`, puis le passe séquentiellement à chaque plugin enregistré. Chaque plugin enrichit `context.findings` selon sa spécialité.

```python
class InvestigationEngine:
    def run(self, prompt: str) -> InvestigationContext:
        context = InvestigationContext(prompt=prompt)
        for plugin in self.plugins:
            plugin.run(context)
        return context
```

### Plugins

Les plugins sont la mécanique d'extension principale. Chaque plugin hérite de `Plugin(ABC)` et implémente `run(context)`.

**Plugins built-in :**

| Plugin               | Rôle                                                          |
|----------------------|---------------------------------------------------------------|
| `AuthorityDetector`  | Détecte les marqueurs d'autorité (`expert`, `scientist`, …)   |
| `AssumptionExtractor`| Identifie les hypothèses implicites dans le texte            |
| `ContradictionFinder`| Repère les tensions logiques et conceptuelles                 |

**Créer un plugin personnalisé :**

```python
from searchlores.plugins.base import Plugin

class PropagandaDetector(Plugin):
    name = "propaganda"

    def run(self, context):
        loaded_terms = ["revolutionary", "obviously", "undeniably"]
        hits = [t for t in loaded_terms if t in context.prompt.lower()]
        context.findings["loaded_language"] = hits
```

### Archaeology Modules

Searchlores implémente trois niveaux d'archéologie, du plus superficiel au plus profond :

**Prompt Archaeology** — analyse le prompt comme artefact culturel :
- Couche de surface : instructions visibles
- Couche d'hypothèses : prémisses cachées
- Couche d'autorité : mécanismes de légitimation
- Couche narrative : récit sous-jacent
- Couche d'omission : ce qui n'est *pas* demandé

**Narrative Archaeology** — remonte vers les récits qui produisent les prompts :
```
Statement → Narrative → Myth → Ideology → Incentive → Power
```

**Cognitive Archaeology** — déconstruit les concepts eux-mêmes :
```yaml
concept: understanding
definitions: [linguistic, philosophical, computational]
genealogy: [Logic → Cybernetics → AI]
contradictions: [prediction, simulation]
schools: [cognitivism, enactivism, embodied cognition]
open_questions:
  - Can understanding exist without embodiment?
  - Can prediction produce understanding?
```

### Graph & Search Maps

Le module `graph/` permet de projeter les résultats d'investigation sous forme de cartes conceptuelles, exportables en Mermaid ou Graphviz.

```
Concept
   │
   ├── Assumptions ──→ Counter-Assumptions
   ├── Narratives  ──→ Counter-Narratives
   ├── Sources     ──→ Source Genealogy
   └── Questions   ──→ New Investigation Targets
```

---

## RFC Specification Stack

Searchlores est guidé par une série de spécifications formelles (RFC), disponibles dans `docs/RFCs/` :

| RFC      | Titre                              | Statut       |
|----------|------------------------------------|--------------|
| RFC-0001 | Core Concepts                      | ✅ Stable    |
| RFC-0002 | Lore Specification                 | ✅ Stable    |
| RFC-0003 | Search Map Specification           | ✅ Stable    |
| RFC-0004 | Investigation Engine Specification | ✅ Stable    |
| RFC-0005 | Prompt Archaeology                 | 🔬 Expérimental |
| RFC-0006 | Narrative Archaeology              | 🔬 Expérimental |
| RFC-0007 | Cognitive Archaeology              | 🔬 Expérimental |
| RFC-0008 | Ontology Builder                   | 📐 Draft     |
| RFC-0009 | Cognitive Atlas                    | 📐 Draft     |
| RFC-0010 | Cognitive Expeditions              | 📐 Draft     |
| RFC-0011 | LoreForge Specification            | 📐 Draft     |

La vision architecturale complète :

```
                    SEARCHLORES

                          │

       ┌──────────────────┼──────────────────┐

       ▼                  ▼                  ▼

  Archaeology        Investigation       Ontology

       │                  │                  │

       ▼                  ▼                  ▼

   Prompt             Search Maps       Knowledge Maps
   Narrative
   Cognitive

       │                  │                  │

       └──────────────────┼──────────────────┘

                          ▼

                   Cognitive Atlas

                          ▼

                Cognitive Expeditions

                          ▼

                       LoreForge

                          ▼

                  Investigative Culture
```

---

## Structure du projet

```
searchlores/
├── searchlores/          ← Package principal (Python)
│   ├── archaeology/
│   ├── cli/
│   ├── core/
│   ├── graph/
│   ├── lore/
│   └── plugins/
├── lores/                ← Lores de démonstration
│   ├── llm.lore
│   └── worldbuilding.lore
├── docs/
│   ├── RFCs/             ← Spécifications formelles (PDF + TXT)
│   └── Searchlores Manifesto.pdf
├── examples/             ← Prompts d'exemple
├── tests/                ← Suite de tests (pytest)
└── pyproject.toml
```

---

## Roadmap

- [ ] **Prompt Archaeology CLI** — `searchlores archaeology prompt "<texte>"`
- [ ] **Lore Validator** — validation structurelle complète + rapport d'audit
- [ ] **Search Map export** — génération Mermaid et Graphviz depuis les contextes
- [ ] **Plugin Manager** — découverte automatique et chargement dynamique
- [ ] **Ontology Builder** (RFC-0008) — fusion des artefacts en cartes de connaissances
- [ ] **Cognitive Atlas** (RFC-0009) — fédération d'ontologies inter-domaines
- [ ] **Cognitive Expeditions** (RFC-0010) — investigations reproductibles et versionnées
- [ ] **LoreForge** (RFC-0011) — forge, validation et publication de Lores
- [ ] **Lore Registry** — dépôt communautaire de disciplines d'investigation

---

## Contributing

Les contributions sont bienvenues, qu'il s'agisse de nouveaux plugins, de Lores thématiques, d'amélioration des modules d'archéologie, ou de l'implémentation des RFCs en cours.

```bash
git clone https://github.com/doktornand/searchlores.git
cd searchlores
pip install -e .
pytest tests/
```

Pour proposer un nouveau Lore, créer un fichier `lores/<domaine>.lore` en respectant le format RFC-0002 et ouvrir une Pull Request avec sa justification épistémologique.

---

## Hommage

> *"Searching is not about finding. It is about learning how to look."*
> — Fravia

**Fravia** (Francesco Vianello, 1952–2009) fut l'un des chercheurs les plus originaux de l'ère Internet. Son site `searchlores.com` n'était pas un moteur de recherche — c'était une école de pensée critique appliquée à la navigation dans l'information. Il enseignait à ses lecteurs à questionner les résultats, à contourner les filtres, à remonter aux sources, et à ne jamais faire confiance à l'évidence.

Ce projet tente de porter cet héritage dans l'ère des LLMs et des graphes de connaissance : non pas pour trouver des réponses plus vite, mais pour fouiller les questions plus profondément.

*The Search Is The Program.*

---

<div align="center">
<sub>Searchlores Academy · Python 3.11+ · MIT</sub>
</div>

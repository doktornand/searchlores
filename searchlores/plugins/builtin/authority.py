from searchlores.core.engine import Plugin, InvestigationContext

class AuthorityDetector(Plugin):
    name = "authority"
    stratum = "autorité"

    AUTHORITY_MARKERS = {
        "institutional": ["expert", "scientist", "researcher", "official", "government", "study", "peer-reviewed"],
        "moral": ["obviously", "clearly", "undeniably", "everyone knows", "common sense"],
        "technocratic": ["algorithm", "data shows", "metrics indicate", "AI determined", "model predicts"],
        "historical": ["traditionally", "historically", "always been", "since ancient times"],
        "futurist": ["inevitable", "the future", "progress demands", "next generation"]
    }

    def run(self, context: InvestigationContext):
        prompt_lower = context.prompt.lower()
        detected = {}

        for category, markers in self.AUTHORITY_MARKERS.items():
            hits = [m for m in markers if m in prompt_lower]
            if hits:
                detected[category] = hits

        context.findings["authority"] = detected

        if "expert" in prompt_lower and "you are" in prompt_lower:
            context.findings["authority"]["inversion_rhetorique"] = [
                "Le prompt confère une identité d'expert à l'IA — mécanisme de transfert d'autorité"
            ]

        if detected:
            context.power_vectors.append(
                f"Autorité {list(detected.keys())} utilisée pour légitimer le cadre de réponse"
            )

class AssumptionExtractor(Plugin):
    name = "assumptions"
    stratum = "hypothèse"

    ASSUMPTION_PATTERNS = {
        "ontological": ["is", "are", "exists", "nature of", "essence", "fundamentally"],
        "epistemological": ["know", "understand", "explain", "prove", "evidence", "truth"],
        "axiological": ["better", "worse", "should", "must", "important", "valuable"],
        "causal": ["because", "leads to", "causes", "results in", "therefore"],
        "teleological": ["purpose", "goal", "designed to", "meant to", "function"]
    }

    def run(self, context: InvestigationContext):
        prompt = context.prompt.lower()
        assumptions = {}

        for category, patterns in self.ASSUMPTION_PATTERNS.items():
            hits = [p for p in patterns if p in prompt]
            if hits:
                assumptions[category] = hits

        context.findings["assumptions"] = assumptions

        if "why" in prompt:
            context.findings["assumptions"]["interrogation_presupposante"] = [
                "La question 'pourquoi' présuppose l'existence d'une cause/rationnelle"
            ]
        if "how" in prompt and "should" in prompt:
            context.findings["assumptions"]["prescriptif_cache"] = [
                "La question normative est masquée sous une forme technique"
            ]

class ContradictionFinder(Plugin):
    name = "contradictions"
    stratum = "cognitif"

    CONTRADICTION_PAIRS = [
        (["unique", "original", "novel"], ["standard", "conventional", "typical"]),
        (["objective", "neutral", "unbiased"], ["believe", "think", "feel", "opinion"]),
        (["everyone", "all", "always"], ["some", "sometimes", "exception"]),
        (["natural", "organic", "authentic"], ["artificial", "synthetic", "constructed"]),
        (["efficient", "optimal", "best"], ["human", "ethical", "fair"])
    ]

    def run(self, context: InvestigationContext):
        prompt_lower = context.prompt.lower()
        contradictions = []

        for pos, neg in self.CONTRADICTION_PAIRS:
            pos_hits = [p for p in pos if p in prompt_lower]
            neg_hits = [n for n in neg if n in prompt_lower]

            if pos_hits and neg_hits:
                contradictions.append({
                    "tension": f"{pos_hits} vs {neg_hits}",
                    "type": "sémantique",
                    "description": f"Le prompt mobilise simultanément {pos_hits} et {neg_hits}"
                })

        context.findings["contradictions"] = contradictions
        context.contradictions = contradictions

class OmissionDetector(Plugin):
    name = "omissions"
    stratum = "omission"

    SILENCE_TRIGGERS = {
        "economique": ["cost", "price", "money", "profit", "market", "investor"],
        "politique": ["power", "control", "governance", "policy", "regulation"],
        "ecologique": ["environment", "climate", "sustainability", "impact"],
        "social": ["inequality", "access", "class", "race", "gender", "labor"],
        "temporel": ["history", "future", "legacy", "debt", "generations"]
    }

    def run(self, context: InvestigationContext):
        prompt_lower = context.prompt.lower()
        absences = []

        for dimension, markers in self.SILENCE_TRIGGERS.items():
            if not any(m in prompt_lower for m in markers):
                absences.append(dimension)

        context.findings["omissions"] = {
            "dimensions_silencieuses": absences,
            "note": f"Le prompt occulte {len(absences)} dimensions d'analyse"
        }
        context.omissions = absences

        if "technical" in prompt_lower or "how to" in prompt_lower:
            context.power_vectors.append("Occultation du politique sous le technique")

class NarrativeArcheologist(Plugin):
    name = "narrative"
    stratum = "narratif"

    NARRATIVE_TEMPLATES = {
        "hero_journey": ["improve", "achieve", "overcome", "success", "master"],
        "tragedy": ["fail", "collapse", "crisis", "threat", "danger", "warning"],
        "utopia": ["future", "potential", "transform", "revolution", "new era"],
        "dystopia": ["surveillance", "control", "loss", "replacement", "extinction"],
        "techno_solutionism": ["fix", "solve", "optimize", "automate", "eliminate"],
        "progress_myth": ["advance", "evolve", "modern", "cutting-edge", "state-of-the-art"]
    }

    def run(self, context: InvestigationContext):
        prompt_lower = context.prompt.lower()
        narratives = {}

        for narrative, markers in self.NARRATIVE_TEMPLATES.items():
            hits = [m for m in markers if m in prompt_lower]
            if hits:
                narratives[narrative] = hits

        context.findings["narratives"] = narratives

        if narratives:
            dominant = max(narratives, key=lambda k: len(narratives[k]))
            context.findings["narratives"]["recit_dominant"] = dominant
            context.power_vectors.append(f"Récit dominant : {dominant} — cadre de pensée imposé")

class CognitiveGenealogist(Plugin):
    name = "genealogy"
    stratum = "cognitif"

    CONCEPT_GENEALOGIES = {
        "intelligence": {
            "origins": ["militaire (tests IQ)", "coloniale (hiérarchies raciales)", "industrielle (productivité)"],
            "contradictions": ["mesurable vs holistique", "innée vs acquise"],
            "alternatives": ["sagesse", "créativité", "intuition", "résilience"]
        },
        "understanding": {
            "origins": ["herméneutique (interprétation)", "phénoménologie (expérience vécue)"],
            "contradictions": ["prédiction vs compréhension", "simulation vs incarnation"],
            "alternatives": ["familiarité", "habileté", "connivence"]
        },
        "efficiency": {
            "origins": ["taylorisme", "fordisme", "cybernétique"],
            "contradictions": ["efficacité vs justice", "optimisation vs résilience"],
            "alternatives": ["frugalité", "suffisance", "lenteur"]
        }
    }

    def run(self, context: InvestigationContext):
        prompt_lower = context.prompt.lower()
        genealogies = {}

        for concept, data in self.CONCEPT_GENEALOGIES.items():
            if concept in prompt_lower:
                genealogies[concept] = data

        context.findings["genealogy"] = genealogies
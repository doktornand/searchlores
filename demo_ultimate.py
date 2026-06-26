#!/usr/bin/env python3
"""
Searchlores Ultimate — Démonstration Complète
Exécutez : python demo_ultimate.py
"""

import sys
sys.path.insert(0, '.')

from searchlores.core.engine import InvestigationEngine
from searchlores.plugins.builtin.authority import (
    AuthorityDetector, AssumptionExtractor, ContradictionFinder,
    OmissionDetector, NarrativeArcheologist, CognitiveGenealogist
)
from searchlores.graph.searchmap import SearchMap

def demo_single_excavation():
    print("=" * 70)
    print("DÉMO 1 : EXCAVATION D'UN PROMPT CORPORATISTE")
    print("=" * 70)

    engine = InvestigationEngine()
    (engine
     .register(AuthorityDetector())
     .register(AssumptionExtractor())
     .register(ContradictionFinder())
     .register(OmissionDetector())
     .register(NarrativeArcheologist())
     .register(CognitiveGenealogist()))

    prompt = ("As a leading AI expert, explain how our company's revolutionary "
              "new language model will disrupt the education market and deliver "
              "unprecedented efficiency gains for institutions worldwide.")

    ctx = engine.run(prompt)

    print(f"\n📊 PROFONDEUR ARCHÉOLOGIQUE : {len(ctx.layers)} strates")
    print(f"⚡ CONTRADICTIONS : {len(ctx.contradictions)}")
    print(f"🔇 SILENCES : {ctx.omissions}")
    print(f"⚔️ VECTEURS DE POUVOIR : {len(ctx.power_vectors)}")

    sm = SearchMap(ctx)
    print("\n📈 SEARCH MAP (Mermaid) :\n")
    print(sm.to_mermaid())

    return ctx

def demo_comparative_bias():
    print("\n" + "=" * 70)
    print("DÉMO 2 : DÉTECTION DE BIAIS SYSTÉMIQUES")
    print("=" * 70)

    prompts = [
        "How do we maximize ROI with AI automation?",
        "What are the social impacts of workplace automation?",
        "Who controls the data used to train these systems?"
    ]

    engine = InvestigationEngine()
    engine.register(AuthorityDetector())
    engine.register(AssumptionExtractor())
    engine.register(OmissionDetector())

    analysis = engine.comparative_analysis(prompts)

    print(f"\n🎯 PRÉSUPPOSÉS PARTAGÉS : {analysis['shared_assumptions']}")
    print(f"⚡ CONSTELLATION DE POUVOIR : {analysis['power_constellations']}")
    print(f"🔇 SILENCES SYSTÉMIQUES : {analysis['systemic_omissions']}")

def demo_lore_audit():
    print("\n" + "=" * 70)
    print("DÉMO 3 : AUDIT ÉPISTÉMOLOGIQUE D'UN LORE")
    print("=" * 70)

    import yaml
    from searchlores.lore.models import Lore

    lore_data = {
        "version": "1.0",
        "metadata": {
            "name": "Surveillance Capitalism",
            "author": "Searchlores Ultimate",
            "tags": ["privacy", "power", "economics"]
        },
        "investigation": {
            "assumptions": [
                "data is neutral",
                "consent is possible",
                "transparency solves power"
            ],
            "myths": [
                "privacy_is_personal",
                "opt_out_is_freedom",
                "regulation_protects"
            ],
            "vectors": ["economics", "law", "technology", "psychology"],
            "questions": [
                "Who owns the infrastructure?",
                "What is extracted beyond data?"
            ],
            "counter_questions": [
                "What if privacy is not the right frame?",
                "What if the problem is not surveillance but capitalism?"
            ],
            "forbidden_answers": [
                "Users should read terms of service",
                "Blockchain will fix this"
            ]
        }
    }

    lore = Lore(**lore_data)

    transgression = len(lore.investigation.counter_questions) + len(lore.investigation.forbidden_answers)
    print(f"\n📜 LORE : {lore.metadata.name}")
    print(f"🏷️  TAGS : {', '.join(lore.metadata.tags)}")
    print(f"🔥 SCORE DE TRANSGRESSION : {transgression}/10")
    print(f"🎯 MYTHES À DÉCONSTRUIRE : {len(lore.investigation.myths)}")
    print(f"❓ CONTRE-QUESTIONS SUBVERSIVES : {len(lore.investigation.counter_questions)}")

if __name__ == "__main__":
    demo_single_excavation()
    demo_comparative_bias()
    demo_lore_audit()

    print("\n" + "=" * 70)
    print("✨ SEARCHLORES ULTIMATE — The Search Is The Program")
    print("=" * 70)
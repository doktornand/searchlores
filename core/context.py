from dataclasses import dataclass, field


@dataclass
class InvestigationContext:

    prompt: str

    findings: dict = field(
        default_factory=dict
    )
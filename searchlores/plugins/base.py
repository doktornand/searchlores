from abc import ABC, abstractmethod
from searchlores.core.context import InvestigationContext

class Plugin(ABC):
    name = "plugin"
    @abstractmethod
    def run(self, context: InvestigationContext) -> None:
        pass
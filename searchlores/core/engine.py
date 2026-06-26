from searchlores.core.context import InvestigationContext

class InvestigationEngine:
    def __init__(self):
        self.plugins = []
    def register(self, plugin):
        self.plugins.append(plugin)
    def run(self, prompt: str) -> InvestigationContext:
        context = InvestigationContext(prompt=prompt)
        for plugin in self.plugins:
            plugin.run(context)
        return context
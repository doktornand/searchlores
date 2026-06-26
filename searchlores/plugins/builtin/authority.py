from searchlores.plugins.base import Plugin

AUTHORITY_WORDS = {"expert", "professional", "doctor", "scientist", "guru"}

class AuthorityDetector(Plugin):
    name = "authority"
    def run(self, context):
        prompt = context.prompt.lower()
        hits = []
        for word in AUTHORITY_WORDS:
            if word in prompt:
                hits.append(word)
        context.findings["authority"] = hits
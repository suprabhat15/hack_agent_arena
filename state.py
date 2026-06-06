from dataclasses import dataclass, field

@dataclass
class AgentState:

    credentials: dict = field(default_factory=dict)

    tokens: dict = field(default_factory=dict)

    entities: dict = field(default_factory=dict)

    seen_api_docs: set = field(default_factory=set)

    completed_steps: list = field(default_factory=list)

    observations: list = field(default_factory=list)

    last_error: str = ""

    def summary(self) -> str:

        return f"""
Known Credentials:
{self.credentials}

Known Tokens:
{list(self.tokens.keys())}

Seen API Docs:
{list(self.seen_api_docs)}

Known Entities:
{list(self.entities.keys())}

Last Error:
{self.last_error}

Recent Steps:
{self.completed_steps[-5:]}
"""
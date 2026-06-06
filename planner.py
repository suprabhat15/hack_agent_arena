class Planner:

    def next_hint(
        self,
        task: str,
        state_summary: str
    ):

        return f"""
TASK:

{task}

CURRENT STATE:

{state_summary}

RULES:

1. Never login twice if a token exists.

2. Never inspect the same API docs twice.

3. Reuse credentials.

4. Reuse access tokens.

5. If an API failed,
   fix the failure instead of restarting.

6. Prefer completing the task
   over exploring.

Return only the NEXT action.
"""
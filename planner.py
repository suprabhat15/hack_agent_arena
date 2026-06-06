class Planner:

    def next_hint(
        self,
        task: str,
        state_summary: str
    ):
        # The task and full state are already supplied to the model
        # elsewhere, so keep this hint short and behavioural — it is
        # prepended to every turn.
        return (
            "Decide the single next action that moves the task forward.\n"
            "- Don't re-login, re-inspect docs, or re-fetch data you "
            "already have (see Known State / Recent Steps).\n"
            "- If the last action failed, fix THAT call; don't restart.\n"
            "- Prefer making progress over exploring.\n"
            "- For action tasks, actually perform the mutation and verify "
            "it succeeded before completing.\n"
            "Return only the NEXT action as one python block."
        )

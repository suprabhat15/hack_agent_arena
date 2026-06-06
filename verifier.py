class Verifier:

    def should_stop(
        self,
        output: str
    ) -> bool:

        output = output.lower()

        return (
            "marked the active task complete"
            in output
            or "task complete"
            in output
        )

    def error_hint(
        self,
        output: str
    ) -> str:

        output = output.lower()

        if "401" in output:
            return (
                "Authentication failed. "
                "Reuse or refresh token."
            )

        if "null" in output:
            return (
                "JSON null must become "
                "Python None."
            )

        if "unexpected keyword" in output:
            return (
                "Check API docs "
                "for parameter names."
            )

        return ""
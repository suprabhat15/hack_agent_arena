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

        # Only emit a failure hint when the step ACTUALLY failed.
        # AppWorld JSON contains the literal "null" all the time, so we
        # must not treat its presence as an error.
        failed = (
            "execution failed" in output
            or "traceback" in output
            or "status code is 4" in output
            or "status code is 5" in output
        )

        if not failed:
            return ""

        if "401" in output or "unauthorized" in output:
            return (
                "Authentication failed. "
                "Reuse or refresh token."
            )

        if (
            "name 'null'" in output
            or "null is not defined" in output
        ):
            return (
                "JSON null must become "
                "Python None."
            )

        if (
            "unexpected keyword" in output
            or "field required" in output
            or "validation error" in output
        ):
            return (
                "Check the API doc for exact parameter "
                "names and required fields; fetch any "
                "missing ids instead of guessing."
            )

        if "no api named" in output:
            return (
                "That API does not exist. List the app's "
                "APIs and pick the correct one."
            )

        return "Fix this specific failing call; do not restart the task."
import re
import json

from state import AgentState


class Memory:

    def __init__(self):
        self.state = AgentState()

    def update(self, output: str):

        self._extract_token(output)

        self._extract_email(output)

        self._extract_credentials(output)

        self._extract_errors(output)

        self.state.observations.append(
            output[:1000]
        )

        if len(self.state.observations) > 20:
            self.state.observations = (
                self.state.observations[-20:]
            )

    def _extract_token(self, output):

        token_match = re.search(
            r'"access_token"\s*:\s*"([^"]+)"',
            output
        )

        if token_match:
            self.state.tokens["latest"] = (
                token_match.group(1)
            )

    def _extract_email(self, output):

        email_match = re.search(
            r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})',
            output
        )

        if email_match:
            self.state.credentials["email"] = (
                email_match.group(1)
            )

    def _extract_credentials(self, output):

        try:

            data = json.loads(output)

            if isinstance(data, list):

                for item in data:

                    if (
                        isinstance(item, dict)
                        and "account_name" in item
                        and "password" in item
                    ):

                        self.state.credentials[
                            item["account_name"]
                        ] = item["password"]

        except Exception:
            pass

    def _extract_errors(self, output):

        if (
            "Execution failed" in output
            or "Traceback" in output
        ):
            self.state.last_error = (
                output[:500]
            )
        else:
            self.state.last_error = ""

    def remember_api_doc(
        self,
        app_name: str
    ):

        self.state.seen_api_docs.add(
            app_name
        )
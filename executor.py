import re


# API name prefixes/names that only READ state (never mutate the world).
_READONLY_PREFIXES = (
    "show", "search", "get", "list", "read",
    "view", "login", "describe", "find", "check",
)
_READONLY_NAMES = {
    "complete_task",
    "show_account_passwords",
}

# apis.<app>.<method>(  -> capture app + method
_API_CALL_RE = re.compile(r"apis\.([a-zA-Z_]+)\.([a-zA-Z_]+)\s*\(")


class Executor:

    @staticmethod
    def calls_mutating_api(code: str) -> bool:
        """True if code calls any API that changes world state.

        Used to detect premature 'no-op' completions: an action task that
        finishes without ever mutating anything almost always failed.
        """
        for app, method in _API_CALL_RE.findall(code):
            if app == "api_docs":
                continue
            if method in _READONLY_NAMES:
                continue
            if method.startswith(_READONLY_PREFIXES):
                continue
            return True
        return False

    @staticmethod
    def completes_task(code: str) -> bool:
        return "complete_task" in code

    @staticmethod
    def passes_answer(code: str) -> bool:
        return bool(re.search(r"complete_task\s*\(\s*answer", code))

    @staticmethod
    def extract_code(text: str) -> str:

        blocks = re.findall(
            r"```(?:python|py)?\s*\n(.*?)```",
            text,
            flags=re.S | re.I
        )

        if blocks:
            code = blocks[-1].strip()
        else:
            code = (
                text
                .replace("```python", "")
                .replace("```py", "")
                .replace("```", "")
                .strip()
            )

        if not code:
            return "print('No code generated')"

        return code
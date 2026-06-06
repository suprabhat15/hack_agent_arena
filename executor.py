import re


class Executor:

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
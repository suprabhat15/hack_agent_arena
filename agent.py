from memory import Memory
from planner import Planner
from verifier import Verifier
from executor import Executor
from llm import complete, MODEL

import os

from appworld import AppWorld, load_task_ids

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


DATASET = os.environ.get(
    "APPWORLD_DATASET",
    "dev"
)

EXPERIMENT = os.environ.get(
    "APPWORLD_EXPERIMENT",
    "team_noob_guy"
)

MAX_INTERACTIONS = int(
    os.environ.get(
        "MAX_INTERACTIONS",
        "30"
    )
)

MAX_TASKS = int(
    os.environ.get(
        "MAX_TASKS",
        "0"
    )
)


def solve(world: AppWorld) -> None:

    memory = Memory()
    planner = Planner()
    verifier = Verifier()

    sup = world.task.supervisor

    task_text = (
        f"Your supervisor (the main user) is:\n"
        f"- Name: {sup.first_name} {sup.last_name}\n"
        f"- Email: {sup.email}\n"
        f"- Phone number: {sup.phone_number}\n\n"
        f"In the task below, 'I', 'me', 'my' refer to this supervisor.\n"
        f"Their app accounts are listed by "
        f"apis.supervisor.show_account_passwords().\n\n"
        f"Task: {world.task.instruction}\n\n"
        f"Begin by taking the first concrete step. Remember to finish with "
        f"apis.supervisor.complete_task(answer=...) once the task is done."
    )

    messages = [
        {
            "role": "user",
            "content": task_text
        }
    ]

    for step in range(MAX_INTERACTIONS):

        state_summary = memory.state.summary()

        hint = planner.next_hint(
            world.task.instruction,
            state_summary
        )

        reply = complete([
            {
                "role": "user",
                "content": (
                    f"Known State:\n"
                    f"{state_summary}\n\n"
                    f"Planner Hint:\n"
                    f"{hint}"
                )
            },
            *messages
        ])

        code = Executor.extract_code(reply)

        print("\n" + "=" * 80)
        print(code)
        print("=" * 80 + "\n")

        output = world.execute(code)

        print(
            f"step {step + 1}: "
            f"{str(output)[:300]!r}"
        )

        output_str = str(output)

        # --------------------------------------------------
        # MEMORY UPDATE
        # --------------------------------------------------

        memory.update(output_str)

        # --------------------------------------------------
        # ERROR RECOVERY
        # --------------------------------------------------

        error_hint = verifier.error_hint(
            output_str
        )

        if error_hint:
            messages.append(
                {
                    "role": "user",
                    "content":
                    f"Previous action failed.\n"
                    f"{error_hint}"
                }
            )

        # --------------------------------------------------
        # CONVERSATION HISTORY
        # --------------------------------------------------

        messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        messages.append(
            {
                "role": "user",
                "content":
                f"Execution output:\n{output_str}"
            }
        )

        # Keep context small
        if len(messages) > 10:
            messages = (
                [messages[0]]
                + messages[-9:]
            )

        # --------------------------------------------------
        # TASK FINISHED?
        # --------------------------------------------------

        if (
            world.task_completed()
            or verifier.should_stop(
                output_str
            )
        ):
            print("✓ task_completed")
            return

    print(
        f"✗ hit MAX_INTERACTIONS "
        f"({MAX_INTERACTIONS})"
    )


def main() -> None:

    task_ids = load_task_ids(DATASET)

    if MAX_TASKS:
        task_ids = task_ids[:MAX_TASKS]

    print(
        f"Running '{EXPERIMENT}' "
        f"on {len(task_ids)} "
        f"'{DATASET}' tasks "
        f"with {MODEL}"
    )

    for i, task_id in enumerate(
        task_ids,
        start=1
    ):

        print(
            f"[{i}/{len(task_ids)}] "
            f"{task_id}"
        )

        try:

            with AppWorld(
                task_id=task_id,
                experiment_name=EXPERIMENT
            ) as world:

                solve(world)

        except Exception as e:

            print(
                f"  ! error: {e}"
            )

    print(
        f"\nDone. Outputs in:\n"
        f"./experiments/outputs/{EXPERIMENT}/"
    )

    print(
        "Run evaluation with:\n"
        f"appworld evaluate {EXPERIMENT} {DATASET}"
    )


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Return success when a target-command list needs the pytest executable.

The helper is deliberately small and unit-tested because a false negative here
can turn a missing test runner into a misleading test result.
"""
import json
import re
import sys

PYTEST_COMMAND = re.compile(r"(^|\s)(pytest|py\.test)(\s|$)")


def requires_pytest(commands):
    if not isinstance(commands, list) or not all(isinstance(x, str) for x in commands):
        raise ValueError("commands must be a JSON list of strings")
    return any(PYTEST_COMMAND.search(command) for command in commands)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: evidence_abstention_requires_pytest.py '<commands-json>'", file=sys.stderr)
        return 2
    try:
        commands = json.loads(argv[0])
        required = requires_pytest(commands)
    except (json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0 if required else 1


if __name__ == "__main__":
    raise SystemExit(main())

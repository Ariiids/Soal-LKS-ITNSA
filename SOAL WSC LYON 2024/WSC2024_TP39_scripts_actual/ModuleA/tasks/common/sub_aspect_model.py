from typing import TypedDict


class SubAspectResult(TypedDict):
    score: int
    msg: str
    command: str | list[str]
    command_output: str | list[str]

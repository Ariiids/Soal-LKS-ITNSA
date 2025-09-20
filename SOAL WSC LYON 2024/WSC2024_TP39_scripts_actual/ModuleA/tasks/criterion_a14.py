from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG


def task_A14_01(task: Task) -> Result:
    """Check if main.html is served"""
    command = "curl -s --connect-timeout 2 http://127.0.0.1/ 2>&1"
    score = 0
    cmd_result = None
    msg = f"main.html is NOT served as index page on {task.host}"
    try:
        cmd_result = run_command(task=task, command=command)
        if "7ecb4e033421b96f88e2111fe97cdad4ddceacc6" in cmd_result.result:
            msg = f"main.html is served as index page on {task.host}"
            score = 0.2
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.2,
    )


def task_A14_02(task: Task) -> Result:
    """Check if 404.html is served"""
    command = "curl -s --connect-timeout 2 http://127.0.0.1/loremipsum 2>&1"
    score = 0
    cmd_result = None
    msg = f"404.html is NOT served as 404 page on {task.host}"
    try:
        cmd_result = run_command(task=task, command=command)
        if "Sorry, but something went wrong" in cmd_result.result:
            msg = f"404.html is served as 404 page on {task.host}"
            score = 0.2
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.2,
    )

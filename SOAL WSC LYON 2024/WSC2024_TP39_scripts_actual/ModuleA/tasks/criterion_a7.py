from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code


def task_A07_01(task: Task) -> Result:
    """Check wireguard interface"""
    command = "wg show"
    score = 0
    cmd_result = None
    msg = "wg0 interface is not up"
    try:
        cmd_result = run_command(task=task, command=command)
        if "interface: wg0" in cmd_result.result:
            msg = "wg0 interface is up"
            score = 0.1
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.1,
    )


def task_A07_02(task: Task) -> Result:
    """Check if PSK is configured for wg0"""
    command = "wg show wg0 preshared-keys"
    score = 0
    msg = "PSK is not configured for wg0"
    try:
        run_command(task=task, command=command)
        msg = "PSK is configured for wg0"
        score = 0.2
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=process_result_exit_code(score != 0.0),
        score=score,
        max_score=0.2,
    )


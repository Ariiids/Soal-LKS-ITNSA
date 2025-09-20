from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG

# Firewall
def task_A06_01a(task: Task) -> Result:
    """SNAT precheck"""
    command = "ip route show default"
    cmd_result = None
    cheated = False
    try:
        cmd_result = run_command(task=task, command=command)
        if "1.1.1.10" in cmd_result.result:
            cheated = True
    except Exception:
        pass

    return Result(
        host=task.host,
        result=cheated,
        command=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
    )


def task_A06_01(
    task: Task, cheated: bool, check_command: str, check_command_output: str
) -> Result:
    """SNAT check"""
    if cheated:
        return Result(
            host=task.host,
            msg="SNAT is probably not working on fw01 as default route exists on jamie-ws01",
            command_run=check_command,
            command_output=check_command_output,
            score=0,
            max_score=0.1,
        )

    command = r"""timeout 2  bash -c "echo -e '\x1dclose\x0d' | telnet 1.1.1.20 22" """
    score = 0
    cmd_result = None
    msg = "SNAT is not working on fw01"
    try:
        cmd_result = run_command(task=task, command=command)
        if "Connected to 1.1.1.20" in cmd_result.result:
            msg = "SNAT is working on fw01"
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

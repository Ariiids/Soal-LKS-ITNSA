from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG


def task_A08_01(task: Task) -> Result:
    """Check transparent proxy"""
    command = "curl -s -I --connect-timeout 3 http://10.1.20.10 2>&1"
    second_command = "curl -s -I --connect-timeout 3 http://[2001:db8:1001:20::20] 2>&1"
    score = 0
    commands = [command, second_command]
    command_outputs = []
    msg = "IPv4 traffic not intercepted by transparent proxy"
    v4_intercepted = False
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "x-secured-by: clearsky-proxy" in cmd_result.result:
            msg = "Only IPv4 traffic intercepted by transparent proxy"
            score += 0.5
            v4_intercepted = True
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    try:
        cmd_result = run_command(task=task, command=second_command)
        command_outputs.append(cmd_result.result)
        if "x-secured-by: clearsky-proxy" in cmd_result.result:
            msg = (
                "IPv4 & IPv6 traffic intercepted by transparent proxy"
                if v4_intercepted
                else "Only IPv6 traffic intercepted by transparent proxy"
            )
            score += 0.5
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=f"{task.host} sending web traffic - {msg}",
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=1.0,
    )

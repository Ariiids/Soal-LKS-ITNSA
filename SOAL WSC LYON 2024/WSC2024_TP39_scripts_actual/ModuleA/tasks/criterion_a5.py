from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG


def task_A05_01(task: Task) -> Result:
    """IPv4 & IPv6 forwarding enabled check"""
    command = "sysctl -p"
    score = 0
    msg = "IPv4 and IPv6 forwarding are not enabled on FW"
    cmd_result = None
    try:
        cmd_result = run_command(task=task, command=command)
        if "net.ipv4.ip_forward = 1" in cmd_result.result:
            msg = "IPv4 forwarding is enabled"
            score += 0.1
        
        if "net.ipv6.conf.all.forwarding = 1" in cmd_result.result:
            msg += "; IPv6 forwarding is enabled"
            score += 0.1
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

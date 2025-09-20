from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG


def task_A11_01(task: Task) -> Result:
    """Check if option TrustedUserCAKeys is set"""
    command = "sshd -T"
    score = 0
    cmd_result = None
    msg = "TrustedUserCAKeys is NOT set on sshd"
    try:
        cmd_result = run_command(task=task, command=command)
        if "trustedusercakeys" in cmd_result.result and "trustedusercakeys none" not in cmd_result.result:
            msg = "TrustedUserCAKeys is set on sshd"
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


def task_A11_02(task: Task) -> Result:
    """Check ssh cert auth"""
    command = 'timeout 2 bash -c \'ssh -vv -o StrictHostKeyChecking=no root@10.1.20.10 "lsb_release -is" 2>&1 | grep "Server accepts"\''
    score = 0
    cmd_result = None
    msg = "SSH certificate based auth failed"
    try:
        cmd_result = run_command(task=task, command=command)
        if "CERT" in cmd_result.result:
            msg = "SSH certificate based auth was successful"
            score = 1.5
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=1.5,
    )

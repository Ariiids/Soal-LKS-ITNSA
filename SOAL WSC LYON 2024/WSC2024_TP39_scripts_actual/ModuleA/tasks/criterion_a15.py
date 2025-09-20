from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG


def task_A15_01(task: Task) -> Result:
    """Check ansible ping"""
    command = "cd /opt/ansible/ && timeout 10 ansible -m ping all"
    score = 0
    cmd_result = None
    msg = "ansible cannot connect to web02"
    try:
        cmd_result = run_command(task=task, command=command)
        if "SUCCESS" in cmd_result.result:
            msg = "ansible can connect to web02"
            score = 0.25
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.25,
    )

def task_A15_02(task: Task) -> Result:
    """Check if main.html is served"""
    command = "curl -s --connect-timeout 2 http://127.0.0.1/ 2>&1"
    commands = [command]
    score = 0
    cmd_result = None
    command_outputs = []
    msg = f"main.html is NOT served as index page on {task.host}"
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "7ecb4e033421b96f88e2111fe97cdad4ddceacc6" in cmd_result.result:
            score = 0.25
    except Exception:
        command_outputs.append(UNKNOWN_MSG)
    
    command = "curl -s --connect-timeout 2 http://127.0.0.1/invalid 2>&1"
    commands.append(command)
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "Sorry, but something went wrong" in cmd_result.result:
            score += 0.25
    except Exception:
        command_outputs.append(UNKNOWN_MSG)
    
    command = "curl -s --connect-timeout 2 http://127.0.0.1/whoami 2>&1"
    commands.append(command)
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if task.host.name in cmd_result.result.lower():
            score += 0.25
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.75,
    )


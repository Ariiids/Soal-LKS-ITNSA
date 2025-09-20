from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code

def task_A10_01(task: Task) -> Result:
    """Check fstab"""
    command = "cat /etc/fstab"
    score = 0
    cmd_result = None
    msg = "/opt/backup is missing in fstab"
    try:
        cmd_result = run_command(task=task, command=command)
        if "/opt/backup" in cmd_result.result:
            msg = "/opt/backup exists in fstab"
            score = 0.2
    except Exception:
        # not exit code 0
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.2,
    )

def task_A10_02(task: Task) -> Result:
    """Check backup script"""
    command = "rm -rf /opt/backup/* ; bash /opt/backup.sh"
    score = 0
    cmd_result = None
    commands = [command]
    command_outputs = []
    msg = "Backup script not found"
    categories = []
    try:
        run_command(task=task, command=command)
        command_outputs.append(process_result_exit_code(True))
    except Exception:
        command_outputs.append(process_result_exit_code(False))

    command = (
        "find /opt/backup/ -name dovecot.conf -o -name main.cf -o -name dovecot.index*"
    )
    commands.append(command)
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "main.cf" in cmd_result.result:
            score += 0.5
            categories.append("postfix")
        if "dovecot.conf" in cmd_result.result:
            score += 0.5
            categories.append("dovecot")
        if "dovecot.index" in cmd_result.result:
            score += 1
            categories.append("mailboxes")
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    command = "cat /opt/backup.sh"
    commands.append(command)
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    if categories:
        msg = f"Backup script is working. {', '.join(categories)} are backed up"

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=2.0,
    )

from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code


def task_A03_01(task: Task) -> Result:
    """Samba user check"""
    command = "smbclient -L //localhost/ -I 127.0.0.1 -U jamie%Skill39@Lyon"
    score = 0
    msg = "Jamie user cannot login"
    try:
        run_command(task=task, command=command)
        msg = "jamie can login on Samba share."
        score = 0.5
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=process_result_exit_code(score != 0),
        score=score,
        max_score=0.5,
    )


def task_A03_02(task: Task) -> Result:
    """Access public share without user"""
    command = 'smbclient //localhost/public -I 127.0.0.1 -U "%" -c ls 2>&1 || true'
    score = 0
    msg = "Cannot access public share."
    cmd_result = None
    try:
        # Read
        cmd_result = run_command(task=task, command=command)
        # Check if there is not login failure
        if (
            ".." in cmd_result.result
            and "NT_STATUS_ACCESS_DENIED" not in cmd_result.result
        ):
            score = 0.25
            msg = "public share can be accessed without user."
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


def task_A03_03(task: Task) -> Result:
    """Write on public share with user"""
    cmd_result = None
    score = 0
    msg = "Cannot access public share with user."
    write_command = 'echo "Lorem Ipsum" > /tmp/lorem.txt; smbclient //localhost/public -I 127.0.0.1 -U "jamie%Skill39@Lyon" -c "put /tmp/lorem.txt lorem.txt"'
    try:
        cmd_result = run_command(task=task, command=write_command)
        # Check if there is not login failure
        if (
            "NT_STATUS_ACCESS_DENIED" not in cmd_result.result
            and "average" in cmd_result.result
        ):
            score = 0.25
            msg = "Public share is writable with user"
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=write_command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.25,
    )


def task_A03_04(task: Task) -> Result:
    """Write on public share without user"""
    score = 0
    cmd_result = None
    msg = "Cannot access public share."
    write_command = 'echo "Lorem Ipsum" > /tmp/lorem.txt; smbclient //localhost/public -I 127.0.0.1 -U "%" -c "put /tmp/lorem.txt lorem.txt" 2>&1 || true'
    try:
        cmd_result = run_command(task=task, command=write_command)
        # Check if there is not login failure
        if "NT_STATUS_ACCESS_DENIED" in cmd_result.result:
            score = 0.25
            msg = "Public share is not writable without user."
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=write_command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.25,
    )


def task_A03_05(task: Task) -> Result:
    """Access internal share without user"""
    score = 0
    msg = "Can access internal share without user."
    write_command = (
        'smbclient //localhost/internal -I 127.0.0.1 -U "%" -c "ls" 2>&1 || true'
    )
    cmd_result = None
    try:
        cmd_result = run_command(task=task, command=write_command)
        # Check if there is not login failure
        if "NT_STATUS_ACCESS_DENIED" in cmd_result.result:
            score = 0.25
            msg = "Internal share is not accessible without user"
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=write_command,
        command_output=cmd_result.result if cmd_result else None,
        score=score,
        max_score=0.25,
    )


def task_A03_06(task: Task) -> Result:
    """Write on internal share with user"""
    score = 0
    msg = "Cannot write on internal share with user"
    write_command = 'echo "Lorem Ipsum" > /tmp/lorem.txt; smbclient //localhost/internal -I 127.0.0.1 -U "jamie%Skill39@Lyon" -c "put /tmp/lorem.txt lorem.txt" || true'
    cmd_result = None
    try:
        cmd_result = run_command(task=task, command=write_command)
        # Check if there is not login failure
        if (
            "NT_STATUS_ACCESS_DENIED" not in cmd_result.result
            and "average" in cmd_result.result
        ):
            score = 0.25
            msg = "Internal share is writable with user"
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=write_command,
        command_output=cmd_result.result if cmd_result else None,
        score=score,
        max_score=0.25,
    )

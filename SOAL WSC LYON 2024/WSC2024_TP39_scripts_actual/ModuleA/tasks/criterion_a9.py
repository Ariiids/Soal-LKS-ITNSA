from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code


def task_A09_01(task: Task) -> Result:
    """Send mail as jamie"""
    verify_command = "cat /etc/passwd | grep jamie"
    score = 0
    commands = [verify_command]
    command_outputs = []
    # Cheat check
    msg = "Cannot send mail as jamie."
    try:
        cmd_result = run_command(task=task, command=verify_command)
        command_outputs.append(cmd_result.result)
        if "jamie:" in cmd_result.result:
            return Result(
                host=task.host,
                result="User jamie has been found in /etc/passwd. Probably not using LDAP for IMAP authentication",
                command_run=commands,
                command_output=command_outputs,
                score=0,
                max_score=1.0,
            )
    except Exception:
        command_outputs.append(process_result_exit_code(True))

    # Send mail over SMTP
    command = "printf 'Subject: WSC2024_FLAG\n\nWSC2024_FLAG'  | curl -s -k --ssl-reqd  --url smtps://localhost --user jamie:Skill39@Lyon -H 'Subject: WSC2024_FLAG' --mail-from 'jamie.oliver@dmz.worldskills.org(Jamie Oliver)' --mail-rcpt jamie.oliver@dmz.worldskills.org --upload-file -"
    commands.append(command)
    cmd_result = None
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        msg = "LDAP user jamie can send mail over SMTPS"
    except Exception:
        command_outputs.append(cmd_result.result if cmd_result else UNKNOWN_MSG)

    # Search for Subject WSC2024_FLAG on IMAP server
    cmd_result = None
    command = r"""IFS=" " read -r -a mail_ids <<< "$(curl -s -k --user jamie:Skill39@Lyon imaps://localhost/INBOX?SUBJECT%20WSC2024_FLAG 2>&1 | grep -oP '(?<=SEARCH)[ 0-9]+')" && curl -s -k --user jamie:Skill39@Lyon "imaps://localhost/INBOX;MAILINDEX=${mail_ids[-1]}" 2>&1"""
    commands.append(command)
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        msg = "LDAP user jamie can send and receive mail."
        score = 1.0
    except Exception:
        command_outputs.append(cmd_result.result if cmd_result else UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=1.0,
    )


def task_A09_02(task: Task) -> Result:
    """test echo service"""
    score = 0
    command = "printf 'Subject: WSC2024_ECHO_FLAG\nFrom: jamie.oliver@dmz.worldskills.org\nTo: echo@dmz.worldskills.org\n\nWSC2024_ECHO_FLAG' | curl -s -k --ssl-reqd  --url smtps://localhost --user jamie:Skill39@Lyon --mail-from 'jamie.oliver@dmz.worldskills.org(Jamie Oliver)' --mail-rcpt echo@dmz.worldskills.org --upload-file -"
    commands = [command]
    command_outputs = []
    msg = "User jamie cannot send to mail echo service"
    cmd_result = None

    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        msg = "LDAP User jamie can send mail to echo"
    except Exception:
        command_outputs.append(cmd_result.result if cmd_result else UNKNOWN_MSG)

    # Search for Subject WSC2024_ECHO_FLAG on IMAP server
    cmd_result = None
    command = r"""IFS=" " read -r -a mail_ids <<< "$(curl -s -k --user jamie:Skill39@Lyon imaps://localhost/INBOX?FROM%20echo@dmz.worldskills.org 2>&1 | grep -oP '(?<=SEARCH)[ 0-9]+')" && curl -s -k --user jamie:Skill39@Lyon "imaps://localhost/INBOX;MAILINDEX=${mail_ids[-1]}" 2>&1"""
    commands.append(command)
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        mail_body = cmd_result.result
        mail_body = mail_body.lower()
        if (
            "to: jamie.oliver@dmz.worldskills.org"
            and "from: echo@dmz.worldskills.org"
            and "report-type=delivery-status"
        ):
            score = 1.5
            msg = "Echo mail has been received"
    except Exception:
        command_outputs.append(cmd_result.result if cmd_result else UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=1.5,
    )

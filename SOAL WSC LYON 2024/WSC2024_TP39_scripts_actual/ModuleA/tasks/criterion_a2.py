from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG


def task_A02_01(task: Task) -> Result:
    """Root CA check"""
    command = (
        "openssl x509 -in /opt/grading/ca/ca.pem -noout -subject -ext basicConstraints,keyUsage || exit 0"
    )
    score = 0
    cmd_result = None
    try:
        cmd_result = run_command(task=task, command=command)
        msg = "Root CA exists"
        if "CA:TRUE" in cmd_result.result and "Certificate Sign" in cmd_result.result:
            score += 0.15
            msg = "Root CA exists and has correct attributes."
        if "clearsky root ca" in cmd_result.result.lower():
            score += 0.10
            msg = "Root CA exists and has correct attributes."
    except Exception:
        # Exit code is 1
        score += 0
        msg = "Root CA DOES NOT exist"

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.25,
    )

def task_A02_02(task: Task) -> Result:
    """Services CA check"""
    command = "openssl x509 -in /opt/grading/ca/services.pem -noout -ext basicConstraints,keyUsage"
    score = 0
    command_outputs = []
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        msg = "Services Sub CA exists"
        if "CA:TRUE" in cmd_result.result and "Certificate Sign" in cmd_result.result:
            score = 0.05
            msg = "Services Sub CA exists and has correct attributes."
    except Exception:
        msg = "Sub CA DOES NOT exist"
        command_outputs.append(UNKNOWN_MSG)

    verify_command = (
        "openssl verify -CAfile /opt/grading/ca/ca.pem /opt/grading/ca/services.pem || exit 0"
    )
    try:
        verify_cmd_result = run_command(task=task, command=verify_command)
        command_outputs.append(verify_cmd_result.result)
        if "/opt/grading/ca/services.pem: OK" in verify_cmd_result.result:
            score += 0.05
            msg += " Services Sub CA is signed by Root CA"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=[command, verify_command],
        command_output=command_outputs,
        score=score,
        max_score=0.1,
    )


def task_A02_03(task: Task) -> Result:
    """webserver cert check"""
    command = "openssl x509 -in /opt/grading/ca/web.pem -noout -subject || exit 0"
    score = 0
    msg = "webserver cert DOES NOT exist"
    command_outputs = []
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "www.dmz.worldskills.org" in cmd_result.result:
            score = 0.05
            msg = "webserver cert exists"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    verify_command = "openssl verify -CAfile <(cat /opt/grading/ca/services.pem /opt/grading/ca/ca.pem) /opt/grading/ca/web.pem || exit 0"
    try:
        verify_cmd_result = run_command(task=task, command=verify_command)
        command_outputs.append(verify_cmd_result.result)
        if "/opt/grading/ca/web.pem: OK" in verify_cmd_result.result:
            score += 0.05
            msg += " webserver cert is fully valid (signed)"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=[command, verify_command],
        command_output=command_outputs,
        score=score,
        max_score=0.1,
    )


def task_A02_04(task: Task) -> Result:
    """mailserver cert check"""
    command = "openssl x509 -in /opt/grading/ca/mail.pem -noout -subject || exit 0"
    score = 0
    msg = "mailserver cert DOES NOT exist"
    command_outputs = []
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "mail.dmz.worldskills.org" in cmd_result.result:
            score = 0.05
            msg = "mailserver cert exists"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    verify_command = "openssl verify -CAfile <(cat /opt/grading/ca/services.pem /opt/grading/ca/ca.pem) /opt/grading/ca/mail.pem || exit 0"
    try:
        verify_cmd_result = run_command(task=task, command=verify_command)
        command_outputs.append(verify_cmd_result.result)
        if "/opt/grading/ca/mail.pem: OK" in verify_cmd_result.result:
            score += 0.05
            msg += "\nmailserver cert is fully valid (signed)"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=[command, verify_command],
        command_output=command_outputs,
        score=score,
        max_score=0.1,
    )

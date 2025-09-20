from enum import StrEnum
from nornir.core.task import Task
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code
from tasks.common.sub_aspect_model import SubAspectResult


class DNS_RECORD_TYPE(StrEnum):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    SRV = "SRV"
    PTR = "PTR"


def check_dns_port_listen(task: Task) -> SubAspectResult:
    """DNS port check"""
    command = r"""echo -e '\x1dclose\x0d' | telnet 127.0.0.1 53 && echo -e '\x1dclose\x0d' | telnet ::1 53"""
    score = 0
    msg = f"{task.host.name} is not listening on tcp/53 for IPv4 AND IPv6"
    try:
        run_command(task=task, command=command)
        msg = f"{task.host.name} is listening on tcp/53 for IPv4 AND IPv6"
        score = 1
    except Exception:
        score = 0

    return {
        "score": score,
        "msg": msg,
        "command": command,
        "command_output": process_result_exit_code(score != 0),
    }


def check_dns_record(
    task: Task, record_type: DNS_RECORD_TYPE, query: str, expected: str
) -> SubAspectResult:
    command = f"dig +short +time=2 +tries=1 @127.0.0.1 {query} {record_type.value}"
    if record_type == DNS_RECORD_TYPE.PTR:
        command = f"dig +short +time=2 +tries=1 @127.0.0.1 -x {query}"
    score = 0
    cmd_result = None
    msg = f"{query} IN {record_type.value} is NOT {expected}"
    try:
        cmd_result = run_command(task=task, command=command)
        if expected in cmd_result.result:
            msg = f"{query} IN {record_type.value} {expected}"
            score = 1
    except Exception:
        score = 0

    return {
        "command": command,
        "msg": msg,
        "score": score,
        "command_output": cmd_result.result if cmd_result else UNKNOWN_MSG,
    }


def check_host_record(
    task: Task, record_type: DNS_RECORD_TYPE, hostname: str, ip_address: str
) -> SubAspectResult:
    result = check_dns_record(
        task=task, record_type=record_type, query=hostname, expected=ip_address
    )

    result_ptr = check_dns_record(
        task=task,
        record_type=DNS_RECORD_TYPE.PTR,
        query=ip_address,
        expected=hostname,
    )
    msg = f"{record_type.value} & PTR record for {hostname} not found"
    if result["score"] > 0 and result_ptr["score"] > 0:
        msg = f"{record_type.value} & PTR exists for {hostname}"
    elif result["score"] > 0 or result_ptr["score"] > 0:
        msg = f"{record_type.value} or PTR doesn't exist for {hostname}"
    else:
        msg = f"{record_type.value} & PTR record for {hostname} not found"
    result["score"] += result_ptr["score"]
    result["msg"] = msg
    result["command"] = [result["command"], result_ptr["command"]]
    result["command_output"] = [result["command_output"], result_ptr["command_output"]]
    return result

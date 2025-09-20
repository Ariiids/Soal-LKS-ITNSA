from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG
from tasks.common.dns_checks import (
    DNS_RECORD_TYPE,
    check_host_record,
)


def task_A04_01(task: Task) -> Result:
    """A int-srv01 check"""
    results = [
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.A,
            hostname="int-srv01.int.worldskills.org.",
            ip_address="10.1.10.10",
        )
    ]

    """AAAA int-srv01 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.AAAA,
            hostname="int-srv01.int.worldskills.org.",
            ip_address="2001:db8:1001:10::10",
        )
    )

    return Result(
        host=task.host,
        result=" ".join([res["msg"] for res in results]),
        command_run=[item for res in results for item in res["command"]],
        command_output=[item for res in results for item in res["command_output"]],
        score=0.2 if sum([res["score"] for res in results]) == 4 else 0.0,
        max_score=0.2,
    )


def task_A04_02(task: Task) -> Result:
    """SRV int-srv01 check"""
    command = (
        "dig +short +time=2 +tries=1 @127.0.0.1 _ldap._tcp.auth.int.worldskills.org SRV"
    )
    score = 0
    msg = "SRV record for int-srv01.int.worldskills.org does not exist"
    cmd_result = None
    try:
        cmd_result = run_command(task=task, command=command)
        if "10 50 389 int-srv01.int.worldskills.org" in cmd_result.result:
            msg = "SRV record for int-srv01.int.worldskills.org exists"
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


def task_A04_03(task: Task) -> Result:
    """Recurse resolver check"""
    command = "dig +recurse +time=2 +tries=1 @127.0.0.1 int.worldskills.org SOA"
    score = 0
    cmd_result = None
    msg = "int-srv01 is not a recursive"
    try:
        cmd_result = run_command(task=task, command=command)
        if "recursion requested but not available" not in cmd_result.result:
            msg = "int-srv01 is a recursive name server"
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


def task_A04_04(task: Task) -> Result:
    """Slave server check"""
    command = "rndc zonestatus dmz.worldskills.org."
    dig_command = "dig +short +time=2 +tries=1 @127.0.0.1 dmz.worldskills.org SOA"
    score = 0
    msg = "int-srv01 is not a secondary for dmz.worldskills.org."
    commands = [command, dig_command]
    command_outputs = []
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if (
            "type: secondary" in cmd_result.result
            and "next refresh" in cmd_result.result
        ):
            msg = "int-srv01 is secondary for dmz.worldskills.org."
            score += 0.05
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    try:
        cmd_result = run_command(task=task, command=dig_command)
        command_outputs.append(cmd_result.result)
        if "dmz.worldskills.org." in cmd_result.result:
            score += 0.05
        else:
            msg += " Cannot resolve dmz.worldskills.org on int-srv01"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.1,
    )


def task_A04_05(task: Task) -> Result:
    """Slave server for v4 & v6 reverse zone check"""
    command = "rndc zonestatus 20.1.10.in-addr.arpa."
    dig_command = "dig +short +time=2 +tries=1 @127.0.0.1 20.1.10.in-addr.arpa. SOA"
    v6_command = "rndc zonestatus 0.2.0.0.1.0.0.1.8.b.d.0.1.0.0.2.ip6.arpa."
    v6_dig_command = "dig +short +time=2 +tries=1 @127.0.0.1 0.2.0.0.1.0.0.1.8.b.d.0.1.0.0.2.ip6.arpa SOA"
    score = 0
    msg = "int-srv01 is not a secondary for IPv4 reverse zone in DMZ. "
    commands = [command, dig_command, v6_command, v6_dig_command]
    command_outputs = []
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if (
            "type: secondary" in cmd_result.result
            and "next refresh" in cmd_result.result
        ):
            msg = "int-srv01 is secondary for 20.1.10.in-addr.arpa; "
            score += 0.05

    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    try:
        cmd_result = run_command(task=task, command=dig_command)
        command_outputs.append(cmd_result.result)
        if "dmz.worldskills.org." in cmd_result.result:
            score += 0.05
        else:
            msg += " Cannot resolve 20.1.10.in-addr.arpa on int-srv01;"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    # IPv6 reverse zone check
    try:
        cmd_result = run_command(task=task, command=v6_command)
        command_outputs.append(cmd_result.result)
        if (
            "type: secondary" in cmd_result.result
            and "next refresh" in cmd_result.result
        ):
            msg = " is secondary for the IPv6 reverse zone"
            score += 0.05
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    try:
        cmd_result = run_command(task=task, command=v6_dig_command)
        command_outputs.append(cmd_result.result)
        if "dmz.worldskills.org." in cmd_result.result:
            score += 0.05
        else:
            msg += "; cannot resolve IPv6 reverse in DMZ on int-srv01"
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.2,
    )

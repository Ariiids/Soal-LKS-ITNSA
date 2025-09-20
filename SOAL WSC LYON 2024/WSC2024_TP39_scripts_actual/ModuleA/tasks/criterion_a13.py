from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG
from tasks.common.dns_checks import (
    DNS_RECORD_TYPE,
    check_dns_record,
    check_host_record,
)


def task_A13_01(task: Task) -> Result:
    """DNS zone check"""
    command = "rndc zonestatus dmz.worldskills.org."
    score = 0
    cmd_result = None
    msg = f"{task.host.name} is NOT secondary name server for dmz.worldskills.org"
    if task.host.name == "ha-prx01":
        msg = f"{task.host.name} is NOT primary name server for dmz.worldskills.org"
    try:
        cmd_result = run_command(task=task, command=command)
        if task.host.name == "ha-prx01" and "type: primary" in cmd_result.result:
            msg = f"{task.host.name} is primary name server for dmz.worldskills.org"
            score += 0.2
        if task.host.name == "ha-prx02" and "type: secondary" in cmd_result.result:
            msg = f"{task.host.name} is secondary name server for dmz.worldskills.org"
            score += 0.2
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


def task_A13_02(task: Task) -> Result:
    """Recurse resolver check"""
    command = "dig +recurse +time=2 +tries=1 @127.0.0.1 int.worldskills.org SOA"
    score = 0
    cmd_result = None
    msg = f"{task.host} is a recursive name server!"
    try:
        cmd_result = run_command(task=task, command=command)
        if "recursion requested but not available" in cmd_result.result:
            msg = f"{task.host} is a not a recursive name server"
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


def task_A13_03(task: Task) -> Result:
    """A record for mail check"""
    hostname = "mail.dmz.worldskills.org."
    ip_addr = "10.1.20.10"
    results = [
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.A,
            hostname=hostname,
            ip_address=ip_addr,
        )
    ]

    """A record for ha-prx01 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.A,
            hostname="ha-prx01.dmz.worldskills.org.",
            ip_address="10.1.20.21",
        )
    )

    """A record for ha-prx02 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.A,
            hostname="ha-prx02.dmz.worldskills.org.",
            ip_address="10.1.20.22",
        )
    )

    """A record for web01 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.A,
            hostname="web01.dmz.worldskills.org.",
            ip_address="10.1.20.31",
        )
    )

    """A record for web02 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.A,
            hostname="web02.dmz.worldskills.org.",
            ip_address="10.1.20.32",
        )
    )

    return Result(
        host=task.host,
        result=" ".join([res["msg"] for res in results]),
        command_run=[item for res in results for item in res["command"]],
        command_output=[item for res in results for item in res["command_output"]],
        score=0.15 if sum([res["score"] for res in results]) == 10 else 0.0,
        max_score=0.15,
    )


def task_A13_04(task: Task) -> Result:
    """A record for prx-vrrp check"""
    results = [
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.A,
            hostname="prx-vrrp.dmz.worldskills.org.",
            ip_address="10.1.20.20",
        )
    ]

    """AAAA record for prx-vrrp check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.AAAA,
            hostname="prx-vrrp.dmz.worldskills.org.",
            ip_address="2001:db8:1001:20::20",
        )
    )

    return Result(
        host=task.host,
        result=" ".join([res["msg"] for res in results]),
        command_run=[item for res in results for item in res["command"]],
        command_output=[item for res in results for item in res["command_output"]],
        score=0.1 if sum([res["score"] for res in results]) == 4 else 0.0,
        max_score=0.1,
    )


def task_A13_05(task: Task) -> Result:
    """AAAA record for mail check"""
    hostname = "mail.dmz.worldskills.org."
    ip_addr = "2001:db8:1001:20::10"
    results = [
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.AAAA,
            hostname=hostname,
            ip_address=ip_addr,
        )
    ]

    """AAAA record for ha-prx01 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.AAAA,
            hostname="ha-prx01.dmz.worldskills.org.",
            ip_address="2001:db8:1001:20::21",
        )
    )

    """AAAA record for ha-prx02 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.AAAA,
            hostname="ha-prx02.dmz.worldskills.org.",
            ip_address="2001:db8:1001:20::22",
        )
    )

    """AAAA record for web01 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.AAAA,
            hostname="web01.dmz.worldskills.org.",
            ip_address="2001:db8:1001:20::31",
        )
    )

    """AAAA record for web02 check"""
    results.append(
        check_host_record(
            task=task,
            record_type=DNS_RECORD_TYPE.AAAA,
            hostname="web02.dmz.worldskills.org.",
            ip_address="2001:db8:1001:20::32",
        )
    )

    return Result(
        host=task.host,
        result=" ".join([res["msg"] for res in results]),
        command_run=[item for res in results for item in res["command"]],
        command_output=[item for res in results for item in res["command_output"]],
        score=0.15 if sum([res["score"] for res in results]) == 10 else 0.0,
        max_score=0.15,
    )


def task_A13_06(task: Task) -> Result:
    """CNAME record for web check"""
    result = check_dns_record(
        task=task,
        record_type=DNS_RECORD_TYPE.CNAME,
        query="www.dmz.worldskills.org.",
        expected="prx-vrrp.dmz.worldskills.org.",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        command_output=result["command_output"],
        score=0.1 if result["score"] == 1 else 0,
        max_score=0.1,
    )

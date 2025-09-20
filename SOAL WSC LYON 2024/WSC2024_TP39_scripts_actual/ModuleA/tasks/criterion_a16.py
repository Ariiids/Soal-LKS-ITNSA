from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG, task_get_ca_cert


def task_A16_01(task: Task) -> Result:
    """Port forwarding udp/53 check"""
    command = "dig +short +time=2 +tries=1 @1.1.1.10 dmz.worldskills.org SOA"
    second_command = (
        "dig +tcp +short +time=2 +tries=1 @1.1.1.10 dmz.worldskills.org SOA"
    )
    score = 0
    commands = [command, second_command]
    command_outputs = []
    msg = "udp/53 and tcp/53 are NOT reachable over WAN"
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "dmz.worldskills.org" in cmd_result.result:
            msg = "udp/53 is reachable over WAN"
            score += 0.05
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    try:
        cmd_result = run_command(task=task, command=second_command)
        command_outputs.append(cmd_result.result)
        if "dmz.worldskills.org" in cmd_result.result:
            msg = (
                "udp/53 & tcp/53 are reachable over WAN"
                if score == 1
                else "tcp/53 are reachable over WAN"
            )
            score += 0.05
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

def task_A16_02(task: Task) -> Result:
    """Port forwarding tcp/80 & 443 check"""
    command = "curl -sv --connect-timeout 2 http://1.1.1.10 2>&1"
    commands = [command]
    score = 0
    cmd_result = None
    command_outputs = []
    msg = "tcp/80 & tcp/443 are NOT reachable over WAN"
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "Connected to 1.1.1.10" in cmd_result.result:
            score = 0.1
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    command = "curl -ksv --connect-timeout 2 https://1.1.1.10 2>&1"
    commands.append(command)

    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "Connected to 1.1.1.10" in cmd_result.result:
            score += 0.1
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    if score > 0:
        msg = "Only tcp/80 or tcp/443 are reachable over WAN"     

    return Result(
        host=task.host,
        result="tcp/80 & tcp/443 are reachable over WAN" if score == 0.2 else msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.2,
    )

def task_A16_03a(task: Task) -> Result:
    return task_get_ca_cert(task)

def task_A16_03(task: Task, cert: str) -> Result:
    """Check STARTTLS on port 143"""
    command = """timeout 2 bash -c 'echo "Q" | openssl s_client -connect 10.1.20.10:143 -verify_return_error -starttls imap -CAfile /tmp/ca.pem 2>&1 || echo "Q" | openssl s_client -connect 10.1.20.10:143 -verify_return_error -starttls imap' 2>&1 || exit 0"""
    score = 0
    cmd_result = None
    msg = "STARTTLS over IMAP not available on mailserver. "

    try:
        run_command(task=task, command=f'echo "{cert}" > /tmp/ca.pem')
    except Exception:
        pass

    try:
        cmd_result = run_command(task=task, command=command)
        if "Verification: OK" in cmd_result.result:
            msg = "Certificate is valid."
            score += 0.25
        if "clearsky root ca" in cmd_result.result.lower():
            msg += " Signed by ClearSky Root CA"
            score += 0.25
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.5,
    )


def task_A16_04(task: Task) -> Result:
    """Check IPv4 & IPv6 availabilties"""
    command = "wg show interfaces"
    score = 0
    commands = [command]
    command_outputs = []
    vpn_interface_name = ""
    try:
        cmd_result = run_command(task=task, command=command)
        vpn_interface_name = cmd_result.result.strip()
        command_outputs.append(cmd_result.result)
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    msg = "jamie-ws01 is not configured to allow IPv4 & IPv6"

    if vpn_interface_name:
        command = f"(ip route get 10.1.10.10 ; ip -6 route get 2001:db8:1001:10::10) | grep {vpn_interface_name} | wc -l"
        commands.append(command)
        try:
            cmd_result = run_command(task=task, command=command)
            command_outputs.append(cmd_result.result)
            # Route through wireguard per route has been found (IPv4 & IPv6)
            if "2" in cmd_result.result:
                score = 0.1
                msg = "jamie-ws01 has routes for IPv4 & IPv6 to reach int-srv01"
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


def task_A16_05(task: Task) -> Result:
    """End-to-End test"""
    command = "dig +time=2 +tries=1 +short @10.1.10.10 int.worldskills.org SOA"
    score = 0
    commands = [command]
    command_outputs = []

    msg = "jamie-ws01 is not able to reach DNS over IPv4 & IPv6"
    v4_reachable = False
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "worldskills.org" in cmd_result.result:
            msg = "jamie-ws01 is able to reach DNS over IPv4 only"
            score += 0.5
            v4_reachable = True
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    command = (
        "dig +time=2 +tries=1 +short @2001:db8:1001:10::10 int.worldskills.org SOA"
    )
    commands.append(command)
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "worldskills.org" in cmd_result.result:
            msg = (
                "jamie-ws01 is able to reach DNS over IPv4 & IPv6"
                if v4_reachable
                else "jamie-ws01 is able to reach DNS over IPv6 only"
            )
            score += 0.5
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=1.0,
    )

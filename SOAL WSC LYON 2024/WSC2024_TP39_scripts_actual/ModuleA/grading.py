#!/usr/local/share/grading/venv/bin/python
import argparse
import signal
import sys
import os

from runner.tag_runner import ThreadedTagRunner
from processors.score_report import PrintScoreReport
from nornir import InitNornir
from nornir.core.filter import F

from tasks import (
    criterion_a1,
    criterion_a2,
    criterion_a3,
    criterion_a4,
    criterion_a5,
    criterion_a6,
    criterion_a7,
    criterion_a8,
    criterion_a9,
    criterion_a10,
    criterion_a11,
    criterion_a12,
    criterion_a13,
    criterion_a14,
    criterion_a15,
    criterion_a16
)

# Set working dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# Keyboard interrupt handler
def signal_handler(signal, frame):
    print("\n\nAborted by the user!")
    sys.exit(0)


# Register ctrl+c handler
signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(
    prog="grading.py",
    description="Worldskills competition 2024 Module A (Linux) grading script",
)
parser.add_argument(
    "-t",
    "--tags",
    metavar="N",
    dest="run_tags",
    nargs="*",
    default=[],
    help="run only given tasks",
)
parser.add_argument(
    "-v",
    "--verbose",
    action=argparse.BooleanOptionalAction,
    dest="verbose",
    default=False,
    help="Enable verbose mode: prints the executed command and the command output as well.",
)
parser.add_argument(
    "-l",
    "--local",
    action=argparse.BooleanOptionalAction,
    dest="run_local",
    default=False,
    help="Run the task locally instead over SSH. Must be executed on the target machine!",
)

args = parser.parse_args()

nr = (
    InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": "inventory/hosts.yaml",
                "defaults_file": "inventory/defaults.yaml",
            },
        },
        user_defined={
            "run_tags": [f"task_{tag.upper()}" for tag in args.run_tags],
            "run_local": args.run_local
        },  # Store the task tags to run
    )
    .with_processors(
        [PrintScoreReport(args.verbose, args.run_local)]
    )  # Custom output handler. Prints the score report
    .with_runner(
        ThreadedTagRunner()
    )  # Tag Handler. Runs only tasks if a tag is set or no tags are set
)
# Inventory filters
host_int_srv = nr.filter(name="int-srv01")
host_fw = nr.filter(name="fw")
host_mail = nr.filter(name="mail")
host_ha_prx01 = nr.filter(name="ha-prx01")
host_ha_proxies = nr.filter(F(name__eq="ha-prx01") | F(name__eq="ha-prx02"))
host_jamie = nr.filter(name="jamie-ws01")
host_int_srv_vpn = nr.filter(F(name__eq="int-srv01") | F(name__eq="jamie-ws01"))
host_web01 = nr.filter(name="web01")
host_web02 = nr.filter(name="web02")

tasks_to_run_int_srv = [
    criterion_a1.task_A01_01,
    criterion_a1.task_A01_02,
    criterion_a1.task_A01_03,
    criterion_a1.task_A01_04,
    criterion_a2.task_A02_01,
    criterion_a2.task_A02_02,
    criterion_a2.task_A02_03,
    criterion_a2.task_A02_04,
    criterion_a3.task_A03_01,
    criterion_a3.task_A03_02,
    criterion_a3.task_A03_03,
    criterion_a3.task_A03_04,
    criterion_a3.task_A03_05,
    criterion_a3.task_A03_06,
    criterion_a4.task_A04_01,
    criterion_a4.task_A04_02,
    criterion_a4.task_A04_03,
    criterion_a4.task_A04_04,
    criterion_a4.task_A04_05,
]
# Run tasks
for task in tasks_to_run_int_srv:
    host_int_srv.run(task=task, on_failed=True)

# Firewall checks
tasks_to_run_fw = [
    criterion_a5.task_A05_01,
]
for task in tasks_to_run_fw:
    host_fw.run(task=task, on_failed=True)

# Test SNAT
snat_precheck_result = host_jamie.run(task=criterion_a6.task_A06_01a, on_failed=True)
# Verify SNAT
host_int_srv.run(
    task=criterion_a6.task_A06_01,
    on_failed=True,
    cheated=snat_precheck_result["jamie-ws01"].result,
    check_command=getattr(snat_precheck_result["jamie-ws01"], "command", ""),
    check_command_output=getattr(
        snat_precheck_result["jamie-ws01"], "command_output", ""
    ),
)

# Wireguard checks
tasks_to_run_fw = [
    criterion_a7.task_A07_01,
    criterion_a7.task_A07_02,
]
for task in tasks_to_run_fw:
    host_fw.run(task=task, on_failed=True)
# Transparent Proxy checks
host_int_srv_vpn.run(task=criterion_a8.task_A08_01, on_failed=True)

# Send and receive mail
host_mail.run(criterion_a9.task_A09_01, on_failed=True)
# Send and receive echo mail
host_mail.run(criterion_a9.task_A09_02, on_failed=True)

# Backup and LUKS checks
task_to_run_mail = [
    criterion_a10.task_A10_01,
    criterion_a10.task_A10_02,
]

for task in task_to_run_mail:
    host_mail.run(task=task, on_failed=True)

# SSH Cert based auth
host_mail.run(task=criterion_a11.task_A11_01, on_failed=True)
host_ha_prx01.run(task=criterion_a11.task_A11_02, on_failed=True)

tasks_to_run_for_reverse_proxy = [criterion_a12.task_A12_01, criterion_a12.task_A12_02]
for task in tasks_to_run_for_reverse_proxy:
    host_ha_proxies.run(task=task)

# Check high available reverse proxy
tasks_to_run_for_reverse_proxy = [
    criterion_a12.task_A12_03,
    criterion_a12.task_A12_04,
    criterion_a12.task_A12_05,
]

for task in tasks_to_run_for_reverse_proxy:
    # Run checks on mail server as it is in the same subnet
    host_mail.run(task=task, on_failed=True)

# Certificate fingerprint from CA
ca_cert_result = host_int_srv.run(
    task=criterion_a12.task_A12_06a, on_failed=True
)
# Use the certificate fingerprint to validate certificate
host_mail.run(
    task=criterion_a12.task_A12_06,
    on_failed=True,
    ca_cert=ca_cert_result["int-srv01"].result,
    check_command=getattr(ca_cert_result["int-srv01"], "command", ""),
    check_command_output=getattr(
        ca_cert_result["int-srv01"], "command_output", ""
    ),
)
# Run VIP check
host_mail.run(task=criterion_a12.task_A12_07, on_failed=True)

# DNS checks for dmz.worldskills.org
host_ha_proxies.run(task=criterion_a13.task_A13_01, on_failed=True)
tasks_to_run_ha_prx01 = [
    criterion_a13.task_A13_02,
    criterion_a13.task_A13_03,
    criterion_a13.task_A13_04,
    criterion_a13.task_A13_05,
    criterion_a13.task_A13_06,
]
for task in tasks_to_run_ha_prx01:
    host_ha_prx01.run(task=task, on_failed=True)

# Web server checks
host_web01.run(task=criterion_a14.task_A14_01, on_failed=True)
host_web01.run(task=criterion_a14.task_A14_02, on_failed=True)

# Ansible
host_ha_prx01.run(task=criterion_a15.task_A15_01, on_failed=True)
host_web02.run(task=criterion_a15.task_A15_02, on_failed=True)

# Port forwarding checks from WAN (jamie-ws)
tasks_to_run_fw = [
    criterion_a16.task_A16_01,
    criterion_a16.task_A16_02,
]
for task in tasks_to_run_fw:
    host_jamie.run(task=task, on_failed=True)

# Get CA cert payload
cert_payload_result = host_int_srv.run(
    task=criterion_a16.task_A16_03a, on_failed=True
)
# Mail E2E test
host_jamie.run(criterion_a16.task_A16_03, on_failed=True, cert=cert_payload_result["int-srv01"].result)
# VPN - IPv4 & IPv6 route check
host_jamie.run(task=criterion_a16.task_A16_04, on_failed=True)
# VPN - E2E check
host_jamie.run(task=criterion_a16.task_A16_05, on_failed=True)
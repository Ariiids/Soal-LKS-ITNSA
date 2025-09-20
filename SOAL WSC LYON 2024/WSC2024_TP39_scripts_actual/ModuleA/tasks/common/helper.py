from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

# Constants
UNKNOWN_MSG = "unknown"


def process_result_exit_code(success: bool) -> str:
    return "Exit code was 0" if success else "Exit code was NOT 0"

def task_get_ca_cert(task: Task) -> Result:
    """Pretask to get certificate fingerprint"""
    command = "cat /opt/grading/ca/ca.pem"
    cmd_result = None
    try:
        cmd_result = run_command(task=task, command=command)
    except Exception:
        # Exit code 1
        pass
    return Result(
        host=task.host,
        result=cmd_result.result if cmd_result else "",
        command=f"root@{task.host} $ {command}",
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
    )
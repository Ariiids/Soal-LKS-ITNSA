from nornir_paramiko.plugins.tasks import paramiko_command
from paramiko.ssh_exception import NoValidConnectionsError
from colorama import Fore, Style


from nornir.core.task import Result, Task

from tasks.common.local_command import local_command


def run_command(task: Task, command: str) -> Result:
    """
    Executes a command depending on command flag either remotely over SSH or locally

    Arguments:
        command: command to execute

    Returns:
        Result object with the following attributes set:
          * result (``str``): stderr or stdout
          * stdout (``str``): stdout
          * stderr (``str``): stderr

    Raises:
        :obj:`nornir_paramiko.exceptions.CommandError`: when there is a command error
    """
    # If flag local is set, then run directly on the current machine
    if task.nornir.config.user_defined and task.nornir.config.user_defined["run_local"] is True:
        return task.run(task=local_command, command=command)
    # Otherwise run over SSH
    try:
        result = task.run(task=paramiko_command, command=command)
    except Exception as ex:
        # If we cannot connect over SSH, then print a warning
        if isinstance(ex.result, list):
            exceptions = [item.exception for item in ex.result if item.exception and isinstance(item.exception, NoValidConnectionsError)]
            
            if len(exceptions) > 0:
                print(f"{Style.BRIGHT}{Fore.RED}[WARNING]: Unable to connect over SSH to execute grading command")
        else:
            if ex.result and ex.result.exception and isinstance(ex.result.exception, NoValidConnectionsError):
                print(f"{Style.BRIGHT}{Fore.RED}[WARNING]: Unable to connect over SSH to execute grading command")
        raise ex
    return result
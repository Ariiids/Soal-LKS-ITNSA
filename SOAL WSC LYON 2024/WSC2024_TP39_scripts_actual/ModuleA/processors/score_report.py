import textwrap
import threading

from colorama import Fore, Style, init

from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Task

init(autoreset=True, strip=False)

PREFIX_LENGTH = 11


class PrintScoreReport:
    """
    Prints score report.
    """

    def __init__(self, verbose: bool = False, run_local = False) -> None:
        self.verbose = verbose
        self.run_local = run_local
        self.even = False
        self.lock = threading.Lock()
        banner = """
_ _ _ ____ ____    _  _ ____ ___  _  _ _    ____    ____ 
| | | [__  |       |\/| |  | |  \ |  | |    |___    |__| 
|_|_| ___] |___    |  | |__| |__/ |__| |___ |___    |  |

____ ____ ____ ____ ____    ____ ____ ___  ____ ____ ___ 
[__  |    |  | |__/ |___    |__/ |___ |__] |  | |__/  |  
___] |___ |__| |  \ |___    |  \ |___ |    |__| |  \  |                                                                                                                   
"""
        print(f"{Style.BRIGHT}{Fore.BLUE}{banner}")
        print(f"{'=' * (75)}")

    def task_started(self, task: Task) -> None:
        return

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        return

    def task_instance_started(self, task: Task, host: Host) -> None:
        return

    def task_instance_completed(
        self, task: Task, host: Host, results: MultiResult
    ) -> None:
        self.lock.acquire()
        for res in results:
            # Skip any non WSC marking tasks
            if not hasattr(res, "score"):
                continue

            # Get attributes
            id = res.name.replace("task_", "")
            score = round(getattr(res, "score", 0.0), 2)
            max_score = getattr(res, "max_score", 0.0)
            color = Fore.GREEN if score == max_score else Fore.RED
            # Either full points or zero points
            score = max_score if score == max_score else 0.0

            # print task
            intend = "".ljust(PREFIX_LENGTH)
            output_formatted = f"\n{intend}".join(textwrap.wrap(res.result, 64))
            output_split = output_formatted.split("\n")
            padding_size = (
                70 - len(output_split[-1])
                if len(output_split) > 1
                else 70 - (len(output_split[-1]) + PREFIX_LENGTH)
            )
            msg = f"=> [{id}] {output_formatted}: {''.ljust(padding_size)}{Style.BRIGHT}{color}{score}"
            print(msg)
            # If verbose is enabled, print the command as well the command output
            if self.verbose:
                command_color = Fore.CYAN
                command_output_color = Fore.BLUE
                executed_commands = getattr(res, "command_run", "<unknown>")
                command_results = getattr(res, "command_output", "<unknown>")
                # Check if multiple commands needed to be print or just single command
                if isinstance(executed_commands, list):
                    for i, c in enumerate(executed_commands):
                        # Print command
                        try:
                            if self.run_local is False:
                                print(
                                    f"{Style.BRIGHT}{command_color}Executed command on {host} =>\n$ {executed_commands[i]}"
                                )
                            else:
                                print(
                                    f"{Style.BRIGHT}{command_color}Executed command {Fore.YELLOW}locally{command_color} =>\n$ {executed_commands[i]}"
                                )
                        except IndexError:
                            print(
                                f"{Style.BRIGHT}{command_color}Unknown command on {host}!"
                            )
                        # Print command output
                        try:
                            print(
                                f"{Style.BRIGHT}{command_output_color}{command_results[i]}"
                            )
                        except IndexError:
                            print(
                                f"{Style.BRIGHT}{command_output_color}Unknown command output!"
                            )
                            continue
                else:
                    if self.run_local is False:
                        print(
                            f"{Style.BRIGHT}{command_color}Executed command on {host} =>\n$ {executed_commands}"
                        )
                    else:
                        print(
                            f"{Style.BRIGHT}{command_color}Executed command {Fore.YELLOW}locally{command_color} =>\n$ {executed_commands}"
                        )
                    print(f"{Style.BRIGHT}{command_output_color}> {command_results}")
            placeholder = "=" if self.even else "-"
            self.even = not self.even
            print(f"{placeholder * (75)}")

        self.lock.release()

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        self.task_instance_started(task, host)

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        self.task_instance_completed(task, host, result)

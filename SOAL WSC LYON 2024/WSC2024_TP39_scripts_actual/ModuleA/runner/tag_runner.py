from concurrent.futures import ThreadPoolExecutor
from typing import List

from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, Task, Result


class ThreadedTagRunner:
    """
    ThreadedTagRunner runs the task only if a partially matching tag is set over each host using threads.
    If no tags are set, it will skip the task

    Arguments:
        num_workers: number of threads to use
    """

    def __init__(self, num_workers: int = 20) -> None:
        self.num_workers = num_workers

    def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:
        result = AggregatedResult(task.name)
        # If no tags are set, run the task
        # if a partially matching tag is set, then run the task
        if (
            "run_tags" not in task.nornir.config.user_defined
            or len(task.nornir.config.user_defined["run_tags"]) == 0
            or any(
                [
                    tag
                    for tag in task.nornir.config.user_defined["run_tags"]
                    if tag in task.name
                ]
            )
        ):
            # Run the task in a thread
            futures = []
            with ThreadPoolExecutor(self.num_workers) as pool:
                for host in hosts:
                    future = pool.submit(task.copy().start, host)
                    futures.append(future)

            # Collect the results and return
            for future in futures:
                worker_result = future.result()
                result[worker_result.host.name] = worker_result
            return result

        # If no matching tags are found, then directly return an empty result
        for host in hosts:
            result[host.name] = Result(
                host=host, result="Task skipped!", failed=False, changed=False
            )
        return result

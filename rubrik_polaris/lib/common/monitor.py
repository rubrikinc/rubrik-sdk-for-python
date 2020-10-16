# Copyright 2020 Rubrik, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.


"""
Collection of methods that monitor tasks
"""

from multiprocessing.pool import ThreadPool
from time import sleep
from timeit import default_timer as timer


# Threader setup
def _monitor_threader(self, tasks, thread_count, monitor_job):
    if not isinstance(tasks, list):
        tasks = [tasks]

    task_list = [(self, t) for t in tasks]

    thread_pool = ThreadPool(thread_count)

    pool_instance = thread_pool.map_async(monitor_job, task_list, chunksize=1)
    while not pool_instance.ready():
        sleep(3)

    thread_pool.close()
    thread_pool.join()

    return pool_instance.get()


# Worker thread
def _monitor_job(job):
    from rubrik_polaris.exceptions import RequestException

    self, task = job
    try:
        start = timer()
        while self.get_task_status(task['taskchainUuid']) not in ["SUCCEEDED", "FAILED"]:
            _ = self.get_task_status(task['taskchainUuid'])
            sleep(3)
        status = self.get_task_status(task['taskchainUuid'])

        # TODO: Add something to handle failures

        task['status'] = status
        task['elapsed'] = timer() - start

        return task

    except Exception as err:
        task['status'] = 'FAILED'
        task['elapsed'] = 0

        return task


# Start threader
def _monitor_task(self, tasks):
    outcome = (_monitor_threader(self, tasks, len(tasks), _monitor_job))

    if len(outcome) > 1:
        return outcome

    return outcome[0]

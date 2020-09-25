""" Collection of methods that monitor tasks """

import time
from timeit import default_timer as timer
from multiprocessing.pool import ThreadPool

# Threader setup
def _monitor_threader(self, _tasks, _thread_count, _monitor_job):
    if not isinstance(_tasks, list):
        _tasks = [_tasks]
    try:
        _task_list = []
        for _task in _tasks:
                _task_list.append((self, _task))
        _thread_pool = ThreadPool(_thread_count)
        _pool_instance = _thread_pool.map_async(_monitor_job, _task_list, chunksize=1)
        while not _pool_instance.ready():
            time.sleep(3)
        _thread_pool.close()
        _thread_pool.join()
        return _pool_instance.get()
    except Exception as e:
        print(e)

# Worker thread
def _monitor_job(_in):
    self, _task = _in
    try:
        _start = timer()
        _last_status = None
        while self.get_task_status(_task['taskchainUuid']) not in ["SUCCEEDED", "FAILED"]:
            _status = self.get_task_status(_task['taskchainUuid'])
            if _status != _last_status:
                _last_status = _status
            time.sleep(3)
        _status = self.get_task_status(_task['taskchainUuid'])
        #Todo: Add something to handle failures
        _task['status'] = _status
        _task['elapsed'] = timer() - _start
        return _task
    except Exception as e:
        print(e)
        return 0

# Start threader
def _monitor_task(self, _tasks):
    _outcome = (_monitor_threader(self, _tasks, len(_tasks), _monitor_job))
    if len(_outcome) > 1:
        return _outcome
    else:
        return _outcome[0]

# Round Robin Scheduler

Simulator of a process scheduler using the Round Robin algorithm.

This is a college assignment.

## How to Run

1. Navigate to the project directory:
    ```bash
    cd /path/to/scheduler_simulator
    ```
2. Run the main script:
    ```bash
    python main.py
    ```

## Code Explanation

The simulator schedules 4 counting processes (incrementing a number), each with a different total execution time and a different increment, resulting in distinct execution times. The main program initializes the scheduler, creates separate processes for each task, adds these processes to the scheduler's queue, and starts the scheduling. The processes run for 2 seconds before being paused and moved to the end of the queue.

The project consists of the following files:

`main.py` defines the `quantum`, the total execution times (`job_times`), and the time increments (`increments`) for each task. Each process executes the `run_job` function, which instantiates and runs a `Task`.

```python
processes = []
for i in range(num_jobs):
    job_id = i + 1
    total_time = job_times[i]
    increment = increments[i]
    process = multiprocessing.Process(target=run_job, args=(job_id, total_time, increment))
    processes.append({'process': process, 'job_id': job_id, 'increment': increment})
    process.start()
    logging.info(f"PID {process.pid} - Task process {job_id} started.")
```
The processes are then added to the `Scheduler` queue, and it is started.

```python
for item in processes:
     if item['process'].pid:
        scheduler.add_process(item['process'], item['job_id'], item['increment'])
     else:
         logging.error(f"Failed to obtain PID. Try running again.")

scheduler.execute()
```

`tarefa.py` contains the `Task` class, which represents a counting program (increments numbers). `increment` is how much each process can increment its counter per time unit. The loop continues until `time_executed` reaches the `total_execution_time` defined for the task.

```python
def execute(self):
    while self.time_executed < self.total_execution_time:
        time.sleep(self.increment)
        self.time_executed += self.increment
        self.time_executed = min(self.time_executed, self.total_execution_time)
        logging.info(f"PID {self.pid} - Task {self.job_id} counting: {self.time_executed:.2f} of {self.total_execution_time}")

    logging.info(f"PID {self.pid} - Task {self.job_id} finished.")
    os.kill(self.pid, 0)
```

`escalonador.py`: The `Scheduler` class uses a `deque` to maintain the order of tasks ready for execution. All processes are paused before scheduling.

```python
for item in self.process_queue:
    process = item['process']
    job_id = item['job_id']
    time.sleep(0.1) 
    if process.is_alive() and process.pid:
         self.stop_process(process.pid, job_id)
    elif not process.is_alive():
         logging.warning(f"PID {process.pid} - Task {job_id} finished before scheduling started.")
```
It enters a loop that continues as long as there are processes to execute. In each iteration, it removes a process from the front of the queue and resumes it by sending a `SIGCONT`.

```python
while self.process_queue:
    item = self.process_queue.popleft()
    process = item['process']
    job_id = item['job_id']
    pid = process.pid
    if not process.is_alive():
        logging.info(f"PID {pid} - Task {job_id} already finished. Removing from queue.")
        continue

    logging.info(f"PID {pid} - Task {job_id} resuming for {self.quantum}s.")
    self.continue_process(pid, job_id) 
    time.sleep(self.quantum) 

    if process.is_alive():
        logging.info(f"PID {pid} - Task {job_id} pausing after quantum.")
        self.stop_process(pid, job_id) 
        self.process_queue.append(item)
    else:
        logging.info(f"PID {pid} - Task {job_id} finished during its quantum.")
    time.sleep(0.1)
```
After the quantum expires, the scheduler pauses the process and adds it back to the queue if it has not yet finished. If it has finished, it is removed from the queue.

`log.txt` is the file where all log messages are recorded.

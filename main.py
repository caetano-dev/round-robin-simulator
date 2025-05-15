import multiprocessing
import time
import logging
import os
from process import Process
from scheduler import Scheduler

increments = [0.3, 1, 0.5, 2]
job_times = [6, 15, 3, 10]
num_jobs = len(job_times)
log_file = "log.txt"
quantum = 2 

def run_job(job_id, total_time, increment):
    job = Process(job_id, total_time, log_file=log_file, increment=increment)
    job.execute()

if __name__ == "__main__":
    if os.path.exists(log_file):
        os.remove(log_file)
    if not os.path.exists(log_file):
        with open(log_file, 'a') as f:
            f.write("")

    scheduler = Scheduler(quantum=quantum, log_file=log_file)
    logging.info(f"Starting {num_jobs} tasks with a quantum of {quantum}s. Each counting up to: {job_times}")



    processes = []
    for i in range(num_jobs):
        job_id = i + 1
        total_time = job_times[i]
        increment = increments[i]
        process = multiprocessing.Process(target=run_job, args=(job_id, total_time, increment))
        processes.append({'process': process, 'job_id': job_id, 'increment': increment})
        process.start()
        logging.info(f"PID {process.pid} - Task process {job_id} started.")

    for item in processes:
         if item['process'].pid:
            scheduler.add_process(item['process'], item['job_id'], item['increment'])
         else:
             logging.error(f"Failed to obtain PID. Try running again.")


    scheduler.execute()
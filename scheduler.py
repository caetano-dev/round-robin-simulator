import os
import signal
import time
import logging
from multiprocessing import Process
from collections import deque 

class Scheduler:

    def __init__(self, quantum, log_file):
        self.quantum = quantum
        self.process_queue = deque() 
        self.log_file = log_file
        self.configure_logging()
        logging.info(f"Starting scheduler with a quantum of {self.quantum} seconds.")

    def configure_logging(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)


        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.FileHandler(self.log_file, mode='a'),
                logging.StreamHandler()
            ]
        )

    def add_process(self, process, job_id, increment):  
        if isinstance(process, Process):
            self.process_queue.append({'process': process, 'job_id': job_id, 'increment': increment})
            logging.info(f"PID {process.pid} - Task {job_id} added to the queue.")

    def stop_process(self, pid, job_id):
        os.kill(pid, signal.SIGSTOP)
        logging.info(f"PID {pid} - Task {job_id} received SIGSTOP signal.")

    def continue_process(self, pid, job_id):
        os.kill(pid, signal.SIGCONT)
        logging.info(f"PID {pid} - Task {job_id} received SIGCONT signal.")


    def execute(self):
        for item in self.process_queue:
            process = item['process']
            job_id = item['job_id']
            time.sleep(0.1)
            if process.is_alive() and process.pid:
                 self.stop_process(process.pid, job_id)
            elif not process.is_alive():
                 logging.warning(f"PID {process.pid} - Task {job_id} finished before scheduling started.")
        
        logging.info("Scheduler started after adding all processes to the queue.")
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

        logging.info("Process queue empty. Scheduling completed.")

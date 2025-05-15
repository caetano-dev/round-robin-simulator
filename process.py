import time
import os
import logging

class Process:
    def __init__(self, job_id, total_execution_time, log_file, increment):

        self.job_id = job_id
        self.total_execution_time = total_execution_time
        self.time_executed = 0
        self.pid = os.getpid()
        self.log_file = log_file
        self.increment = increment


        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.FileHandler(self.log_file, mode='a'), 
                logging.StreamHandler()
            ]
        )
        logging.info(f"PID {self.pid} - Task {self.job_id} counting from {self.time_executed} to: {self.total_execution_time}")

    def execute(self):
        while self.time_executed < self.total_execution_time:
            time.sleep(self.increment)
            self.time_executed += self.increment
            self.time_executed = min(self.time_executed, self.total_execution_time)
            logging.info(f"PID {self.pid} - Task {self.job_id} counting: {self.time_executed:.2f} of {self.total_execution_time}")

        logging.info(f"PID {self.pid} - Task {self.job_id} finished.")
        os.kill(self.pid, 0)
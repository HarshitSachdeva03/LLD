import time
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional
from app.models.job import Job, JobState
from app.core.queue_manager import PriorityJobQueue

logger = logging.getLogger(__name__)

class JobEngine:
    def __init__(self, queue: PriorityJobQueue, max_workers: int = 3):
        self.queue = queue
        self.max_workers = max_workers
        self.jobs_registry: Dict[str, Job] = {}  # In-memory database of jobs
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._is_running = False

    def submit_job(self, job: Job) -> Job:
        """Producer method: stores job and puts it in queue."""
        self.jobs_registry[job.id] = job
        self.queue.push(job)
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs_registry.get(job_id)

    def start(self) -> None:
        """Starts background worker threads."""
        self._is_running = True
        for _ in range(self.max_workers):
            self._executor.submit(self._worker_loop)

    def _worker_loop(self) -> None:
        """Consumer loop running on background threads."""
        while self._is_running:
            job = self.queue.pop()
            
            if job is None:
                time.sleep(0.1)  # Rest briefly if no work is available
                continue
            
            self._execute_job(job)

    def _execute_job(self, job: Job) -> None:
        """Executes task and updates status."""
        job.state = JobState.RUNNING
        try:
            time.sleep(1)  # Simulate processing task
            
            if job.payload == "fail_test":
                raise ValueError("Simulated job failure")

            job.state = JobState.COMPLETED
        except Exception as e:
            logger.error(f"Job {job.id} failed: {e}")
            job.state = JobState.FAILED

    def stop(self) -> None:
        self._is_running = False
        self._executor.shutdown(wait=False)
"""Background worker for processing queued jobs using RQ."""
from redis import Redis
from rq import Queue
from main import run_crew
from db import SessionLocal, Analysis

# Redis connection (default localhost:6379)
redis_conn = Redis()
queue = Queue('financial', connection=redis_conn)


def process_job(job_id: str, query: str, file_path: str) -> None:
    """Function executed by worker to run analysis and update database."""
    session = SessionLocal()
    record = session.get(Analysis, job_id)
    if not record:
        session.close()
        return
    try:
        result = run_crew(query=query, file_path=file_path)
        record.result = str(result)
        record.status = 'completed'
    except Exception as e:
        record.result = f'error: {e}'
        record.status = 'failed'
    finally:
        session.commit()
        session.close()


if __name__ == '__main__':
    # This file can be started as an RQ worker via `rq worker financial`
    print("run 'rq worker financial' to start processing jobs")

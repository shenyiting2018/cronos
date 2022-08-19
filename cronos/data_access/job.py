from cronos.models.job import Job, JobExecution
from typing import List
from datetime import datetime


def list_jobs(
    job_id: int = None,
    name: str = None,
    cron_expression: str = None,
    service_id: str = None,
) -> List[Job]:
    query = Job.objects.filter(is_inactive=False)
    if job_id:
        query = query.filter(id=job_id)
    if name:
        query = query.filter(name=name)
    if cron_expression:
        query = query.filter(cron_expression=cron_expression)
    if service_id:
        query = query.filter(service_id=service_id)
    return list(query.all())


def create_job(
    name: str,
    cron_expression: str,
    service_id: str = None,
) -> Job:
    if service_id and not isinstance(service_id, str):
        raise ValueError("Service id must be a string")
    new_job = Job.objects.create(
        name=name,
        cron_expression=cron_expression,
        service_id=service_id,
    )
    return new_job


def update_job(
    job_id: int,
    name: str = None,
    cron_expression: str = None,
    service_id: str = None,
) -> Job:
    job = Job.objects.get(id=job_id)

    if name:
        job.name = name
    if cron_expression:
        job.cron_expression = cron_expression
    if service_id:
        if not isinstance(service_id, str):
            raise ValueError("Service id must be a string")
        job.service_id = service_id
    job.updated_time = datetime.now()
    job.save()
    return job


def remove_job(
    job_id: int,
):
    job = Job.objects.get(id=job_id)
    if not job.is_inactive:
        job.is_inactive = True
    else:
        raise Exception("This job has been already inactived")
    job.save()


def list_executions(
    exec_id: int = None,
    job_id: int = None,
    cron_expression: str = None,
    status: int = None,
) -> List[JobExecution]:
    query = JobExecution.objects.all()
    if exec_id:
        query = query.filter(id=exec_id)
    if job_id:
        query = query.filter(job_id=job_id)
    if cron_expression:
        query = query.filter(cron_expression=cron_expression)
    if status:
        query = query.filter(status=status)
    return list(query.all())


def create_execution(
    job_id: int,
) -> JobExecution:
    job = Job.objects.get(id=job_id)
    if not job:
        raise Exception("Job does not exist")
    cron_expression = job.cron_expression
    new_execution = JobExecution.objects.create(
        job_id=job_id,
        cron_expression=cron_expression,
    )
    return new_execution


def update_execution(
    exec_id: int,
    status: int = None,
    scheduled_start_time: str = None,
    start_time: str = None,
    end_time: str = None,
) -> JobExecution:
    execution = JobExecution.objects.get(id=exec_id)
    if not execution:
        raise Exception("Execution does not exist")
    if status:
        execution.status = status
    # will move the following to logic file later
    if scheduled_start_time:
        execution.scheduled_start_time = datetime.strptime(
            scheduled_start_time.replace(" ", "-"), "%Y-%m-%d-%H:%M:%S"
        )
    if start_time:
        execution.start_time = datetime.strptime(
            start_time.replace(" ", "-"), "%Y-%m-%d-%H:%M:%S"
        )
    if end_time:
        execution.end_time = datetime.strptime(
            end_time.replace(" ", "-"), "%Y-%m-%d-%H:%M:%S"
        )
    execution.save()
    return execution

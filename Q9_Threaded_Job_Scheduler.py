"""Q9: Deterministic multi-worker scheduling simulation.
Priority is higher for larger values; ties use arrival time then input order.
"""
import sys
import heapq

def schedule_jobs(worker_count, jobs):
    jobs.sort(key=lambda j: (j["arrival"], j["input_order"]))
    waiting, workers = [], [(0, i + 1) for i in range(worker_count)]
    heapq.heapify(workers)
    events, output = [], []
    next_job = 0
    while next_job < len(jobs) or waiting:
        if not waiting and next_job < len(jobs):
            earliest_free = workers[0][0]
            if jobs[next_job]["arrival"] > earliest_free:
                # All workers idle until next arrival.
                workers = [(jobs[next_job]["arrival"], wid) if t < jobs[next_job]["arrival"] else (t, wid)
                           for t, wid in workers]
                heapq.heapify(workers)
        current_time = min(workers)[0]
        while next_job < len(jobs) and jobs[next_job]["arrival"] <= current_time:
            job = jobs[next_job]
            heapq.heappush(waiting, (-job["priority"], job["arrival"], job["input_order"], job))
            next_job += 1
        if not waiting:
            continue
        free_time, worker_id = heapq.heappop(workers)
        job = heapq.heappop(waiting)[3]
        start = max(free_time, job["arrival"])
        finish = start + job["duration"]
        output.append((job["job_id"], f"W{worker_id}", start, finish, start-job["arrival"]))
        heapq.heappush(workers, (finish, worker_id))
    return output

def main():
    data = sys.stdin.read().splitlines()
    try:
        w, n = map(int, data[0].split())
        if not 1 <= w <= 64: raise ValueError("Worker count must be 1..64")
        jobs = []
        for i, line in enumerate(data[1:n+1]):
            arrival, job_id, priority, duration, resources = line.split()
            arrival, priority, duration, resources = map(int, (arrival, priority, duration, resources))
            if arrival < 0 or duration < 1 or resources < 1: raise ValueError("Invalid job values")
            jobs.append({"arrival": arrival, "job_id": job_id, "priority": priority,
                         "duration": duration, "resources": resources, "input_order": i})
        results = schedule_jobs(w, jobs)
        for job_id, worker, start, finish, _ in sorted(results, key=lambda x: (x[2], x[0])):
            print(job_id, worker, start, finish)
        average = sum(item[4] for item in results) / len(results) if results else 0
        print(f"AVG_WAIT {average:.2f}")
    except (ValueError, IndexError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

"""
Process Scheduling Simulation
=============================
Simulates all 6 scheduling algorithms from the assignment and prints
Gantt charts with performance metrics.

Usage: python scheduling_simulation.py
"""

# Process data: (name, arrival_time, burst_time)
processes = [
    ("P1", 0,  5),
    ("P2", 3,  1),
    ("P3", 10, 11),
    ("P4", 12, 5),
    ("P5", 15, 12),
]


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_gantt(gantt):
    """Print a text-based Gantt chart from list of (process, start, end)."""
    print("\n  Gantt Chart:")
    line1 = "  |"
    line2 = "  "
    for proc, start, end in gantt:
        width = max(len(proc), (end - start) * 2)
        line1 += f" {proc:^{width}} |"
        line2 += f" {start:<{width}}  "
    line2 += str(gantt[-1][2])
    print(line1)
    print(line2)


def print_metrics(results, procs):
    """Print performance metrics table."""
    print("\n  Performance Metrics:")
    print(f"  {'Process':<8} {'Arrival':<8} {'Burst':<8} {'Completion':<12} {'TAT':<8} {'WT':<8}")
    print("  " + "-" * 52)
    total_tat = 0
    total_wt = 0
    for name, arrival, burst in procs:
        completion = results[name]
        tat = completion - arrival
        wt = tat - burst
        total_tat += tat
        total_wt += wt
        print(f"  {name:<8} {arrival:<8} {burst:<8} {completion:<12} {tat:<8} {wt:<8}")
    n = len(procs)
    print(f"\n  Average Turnaround Time = {total_tat / n:.2f}")
    print(f"  Average Waiting Time    = {total_wt / n:.2f}")


# ============================================================
# 1. FCFS (First Come First Served)
# ============================================================
def fcfs(procs):
    print_header("1. FCFS (First Come First Served)")
    procs_sorted = sorted(procs, key=lambda x: x[1])
    time = 0
    gantt = []
    results = {}

    for name, arrival, burst in procs_sorted:
        if time < arrival:
            gantt.append(("idle", time, arrival))
            time = arrival
        gantt.append((name, time, time + burst))
        time += burst
        results[name] = time

    print_gantt(gantt)
    print_metrics(results, procs)


# ============================================================
# 2. SJF Non-Preemptive
# ============================================================
def sjf_non_preemptive(procs):
    print_header("2. SJF Non-Preemptive")
    remaining = [(name, arrival, burst) for name, arrival, burst in procs]
    time = 0
    gantt = []
    results = {}
    completed = set()

    while len(completed) < len(procs):
        available = [(n, a, b) for n, a, b in remaining if a <= time and n not in completed]
        if not available:
            next_arrival = min(a for n, a, b in remaining if n not in completed)
            gantt.append(("idle", time, next_arrival))
            time = next_arrival
            continue
        # Pick shortest burst
        available.sort(key=lambda x: x[2])
        name, arrival, burst = available[0]
        gantt.append((name, time, time + burst))
        time += burst
        results[name] = time
        completed.add(name)

    print_gantt(gantt)
    print_metrics(results, procs)


# ============================================================
# 3. SRTF (Shortest Remaining Time First)
# ============================================================
def srtf(procs):
    print_header("3. SRTF (Shortest Remaining Time First)")
    remaining = {name: burst for name, _, burst in procs}
    arrivals = {name: arrival for name, arrival, _ in procs}
    time = 0
    gantt = []
    results = {}
    completed = set()
    max_time = sum(b for _, _, b in procs) + max(a for _, a, _ in procs)
    current = None

    while len(completed) < len(procs) and time <= max_time:
        available = {n: remaining[n] for n in remaining
                     if arrivals[n] <= time and n not in completed}
        if not available:
            time += 1
            continue

        shortest = min(available, key=available.get)

        if shortest != current:
            if gantt and gantt[-1][0] == shortest:
                pass  # continue same block
            else:
                current = shortest

        remaining[shortest] -= 1
        if remaining[shortest] == 0:
            completed.add(shortest)
            results[shortest] = time + 1

        time += 1

    # Build gantt from time trace
    # Re-simulate to build proper gantt
    remaining2 = {name: burst for name, _, burst in procs}
    time = 0
    gantt = []
    completed2 = set()
    prev = None
    seg_start = 0

    while len(completed2) < len(procs) and time <= max_time:
        available = {n: remaining2[n] for n in remaining2
                     if arrivals[n] <= time and n not in completed2}
        if not available:
            if prev is not None:
                gantt.append((prev, seg_start, time))
                prev = None
            if gantt and gantt[-1][0] == "idle":
                pass
            seg_start = time
            time += 1
            if prev is None and (not gantt or gantt[-1][0] != "idle"):
                prev = "idle"
                seg_start = time - 1
            continue

        shortest = min(available, key=available.get)

        if shortest != prev:
            if prev is not None:
                gantt.append((prev, seg_start, time))
            prev = shortest
            seg_start = time

        remaining2[shortest] -= 1
        if remaining2[shortest] == 0:
            completed2.add(shortest)

        time += 1

    if prev is not None:
        gantt.append((prev, seg_start, time))

    print_gantt(gantt)
    print_metrics(results, procs)


# ============================================================
# 4. Round Robin (Time Slice = 2)
# ============================================================
def round_robin(procs, quantum=2):
    print_header(f"4. Round Robin (Time Slice = {quantum})")
    from collections import deque

    remaining = {name: burst for name, _, burst in procs}
    arrivals = sorted(procs, key=lambda x: x[1])
    arrival_map = {name: arrival for name, arrival, _ in procs}
    queue = deque()
    time = 0
    gantt = []
    results = {}
    arrived = set()
    idx = 0

    while len(results) < len(procs):
        # Add newly arrived processes
        while idx < len(arrivals) and arrivals[idx][1] <= time:
            name = arrivals[idx][0]
            if name not in arrived:
                queue.append(name)
                arrived.add(name)
            idx += 1

        if not queue:
            next_time = arrivals[idx][1] if idx < len(arrivals) else time + 1
            gantt.append(("idle", time, next_time))
            time = next_time
            continue

        current = queue.popleft()
        run_time = min(quantum, remaining[current])
        gantt.append((current, time, time + run_time))
        time += run_time
        remaining[current] -= run_time

        # Add processes that arrived during this quantum
        while idx < len(arrivals) and arrivals[idx][1] <= time:
            name = arrivals[idx][0]
            if name not in arrived:
                queue.append(name)
                arrived.add(name)
            idx += 1

        if remaining[current] == 0:
            results[current] = time
        else:
            queue.append(current)

    print_gantt(gantt)
    print_metrics(results, procs)


# ============================================================
# 5. Multiprocessing with 3 CPUs (FCFS)
# ============================================================
def multiprocessing_fcfs(procs, num_cpus=3):
    print_header(f"5. Multiprocessing with {num_cpus} CPUs (FCFS)")
    import heapq

    procs_sorted = sorted(procs, key=lambda x: x[1])
    cpu_free = [0] * num_cpus  # When each CPU becomes free
    results = {}
    gantt_per_cpu = [[] for _ in range(num_cpus)]

    for name, arrival, burst in procs_sorted:
        # Find earliest available CPU at or after arrival
        best_cpu = 0
        best_time = max(cpu_free[0], arrival)
        for i in range(1, num_cpus):
            t = max(cpu_free[i], arrival)
            if t < best_time:
                best_time = t
                best_cpu = i

        start = best_time
        end = start + burst
        gantt_per_cpu[best_cpu].append((name, start, end))
        cpu_free[best_cpu] = end
        results[name] = end

    print("\n  Gantt Charts:")
    for i, g in enumerate(gantt_per_cpu):
        if g:
            line = f"  CPU{i+1}: "
            for proc, start, end in g:
                line += f"|{proc}({start}-{end})"
            line += "|"
            print(line)

    print_metrics(results, procs)


# ============================================================
# 6. Multiprocessing RR with 2 CPUs (Time Slice = 2)
# ============================================================
def multiprocessing_rr(procs, num_cpus=2, quantum=2):
    print_header(f"6. Multiprocessing RR with {num_cpus} CPUs (Time Slice = {quantum})")
    from collections import deque

    remaining = {name: burst for name, _, burst in procs}
    arrivals = sorted(procs, key=lambda x: x[1])
    arrival_map = {name: arrival for name, arrival, _ in procs}
    queue = deque()
    results = {}
    arrived = set()
    idx = 0
    gantt_per_cpu = [[] for _ in range(num_cpus)]
    cpu_free = [0] * num_cpus

    while len(results) < len(procs):
        # Find the earliest CPU free time
        min_free = min(cpu_free)

        # Add processes that have arrived by min_free
        while idx < len(arrivals) and arrivals[idx][1] <= min_free:
            name = arrivals[idx][0]
            if name not in arrived and name not in results:
                queue.append(name)
                arrived.add(name)
            idx += 1

        if not queue:
            if idx < len(arrivals):
                next_arrival = arrivals[idx][1]
                for i in range(num_cpus):
                    if cpu_free[i] <= min_free:
                        cpu_free[i] = next_arrival
                continue
            else:
                break

        # Assign processes to free CPUs
        for i in range(num_cpus):
            if cpu_free[i] <= min_free and queue:
                current = queue.popleft()
                start = max(cpu_free[i], min_free)
                run_time = min(quantum, remaining[current])
                end = start + run_time
                gantt_per_cpu[i].append((current, start, end))
                cpu_free[i] = end
                remaining[current] -= run_time

                # Add arrivals during this quantum
                while idx < len(arrivals) and arrivals[idx][1] <= end:
                    name = arrivals[idx][0]
                    if name not in arrived and name not in results:
                        queue.append(name)
                        arrived.add(name)
                    idx += 1

                if remaining[current] == 0:
                    results[current] = end
                else:
                    queue.append(current)

    print("\n  Gantt Charts:")
    for i, g in enumerate(gantt_per_cpu):
        if g:
            line = f"  CPU{i+1}: "
            for proc, start, end in g:
                line += f"|{proc}({start}-{end})"
            line += "|"
            print(line)

    print_metrics(results, procs)


# ============================================================
# Run all simulations
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  PROCESS SCHEDULING SIMULATION")
    print("=" * 60)
    print("\n  Process Data:")
    print(f"  {'Process':<8} {'Arrival':<8} {'Burst':<8}")
    print("  " + "-" * 24)
    for name, arrival, burst in processes:
        print(f"  {name:<8} {arrival:<8} {burst:<8}")

    fcfs(processes)
    sjf_non_preemptive(processes)
    srtf(processes)
    round_robin(processes, quantum=2)
    multiprocessing_fcfs(processes, num_cpus=3)
    multiprocessing_rr(processes, num_cpus=2, quantum=2)

    print("\n" + "=" * 60)
    print("  ALL SIMULATIONS COMPLETE")
    print("=" * 60)
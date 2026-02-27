# Process Scheduling Assignment - Solution

## Process Details and Assumptions

To solve the scheduling algorithms, we will normalize the arrival times. Assuming 1 time unit = 1 minute, we set 5:30 PM as `T = 0`. This gives us the following relative arrival times:

| Process ID | Arrival Time (Absolute) | Arrival Time (Relative `T`) | Estimated Processing Time (Burst Time) |
|------------|-------------------------|--------------------------|----------------------------------------|
| **P1**     | 5:30 PM                 | 0                        | 5                                      |
| **P2**     | 5:33 PM                 | 3                        | 1                                      |
| **P3**     | 5:40 PM                 | 10                       | 11                                     |
| **P4**     | 5:42 PM                 | 12                       | 5                                      |
| **P5**     | 5:45 PM                 | 15                       | 12                                     |

---

## 1. Multiprogramming System
*Assuming a basic First-Come-First-Serve (FCFS) since no priority is mentioned.*

* **T = 0:** P1 arrives and starts processing.
* **T = 3:** P2 arrives and waits in the ready queue.
* **T = 5:** P1 completes. P2 starts processing.
* **T = 6:** P2 completes. The CPU becomes idle.
* **T = 10:** P3 arrives and starts processing.
* **T = 12:** P4 arrives and waits.
* **T = 15:** P5 arrives and waits.
* **T = 21:** P3 completes. P4, which arrived first among the waiting, starts processing.
* **T = 26:** P4 completes. P5 starts processing.
* **T = 38:** P5 completes.

### Gantt Chart
| Time  | 0 - 5 | 5 - 6 | 6 - 10 | 10 - 21 | 21 - 26 | 26 - 38 |
|-------|-------|-------|--------|---------|---------|---------|
| **Process**| P1    | P2    | *Idle* | P3      | P4      | P5      |

---

## 2. Multiprogramming with priority for shortest job first in non-preemptive mode

In this mode (SJF Non-preemptive), whenever the CPU is free, it selects the process in the ready queue with the shortest burst time. Since it is non-preemptive, a running process is not interrupted by a new, shorter arrival.

* **T = 0:** Only P1 is available. It executes fully `[0-5]`.
* **T = 5:** P1 finishes. Only P2 is in the ready queue. P2 executes `[5-6]`.
* **T = 6:** P2 finishes. CPU falls **Idle**.
* **T = 10:** P3 arrives. Since it's the only one, it executes fully `[10-21]`.
* **T = 21:** P3 finishes. Now, both P4 ($BT=5$) and P5 ($BT=12$) are waiting in the queue.
* **T = 21:** The scheduler selects P4 (shortest process). P4 executes `[21-26]`.
* **T = 26:** P4 finishes. P5 executes `[26-38]`.

*(Note: In this specific scenario, the Gantt Chart happens to be identical to FCFS).*

### Gantt Chart
| Time  | 0 - 5 | 5 - 6 | 6 - 10 | 10 - 21 | 21 - 26 | 26 - 38 |
|-------|-------|-------|--------|---------|---------|---------|
| **Process**| P1    | P2    | *Idle* | P3      | P4      | P5      |

---

## 3. Multiprogramming with priority for shortest job first in pre emptive mode

Also known as Shortest Remaining Time First (SRTF). A newly arriving process can preempt the currently running process if its burst time is less than the remaining time of the running process.

* **T = 0:** P1 starts. (Rem: P1=5)
* **T = 3:** P2 ($BT=1$) arrives. P1 has 2 units remaining. P2 requires less time than P1, so P1 is **preempted**. P2 starts.
* **T = 4:** P2 completes. P1 resumes.
* **T = 6:** P1 completes. CPU falls **Idle**.
* **T = 10:** P3 arrives and starts. (Rem: P3=11)
* **T = 12:** P4 ($BT=5$) arrives. P3 has 9 units remaining. P4 is shorter, so P3 is **preempted**. P4 starts.
* **T = 15:** P5 ($BT=12$) arrives. P4 has 2 units remaining. P4 is still the shortest, so it continues.
* **T = 17:** P4 completes. P3 (Rem:9) and P5 (Rem:12) are in the queue. P3 starts.
* **T = 26:** P3 completes. P5 starts.
* **T = 38:** P5 completes.

### Gantt Chart
| Time | 0 - 3 | 3 - 4 | 4 - 6 | 6 - 10 | 10 - 12 | 12 - 17 | 17 - 26 | 26 - 38 |
|---|---|---|---|---|---|---|---|---|
| **Process** | P1 | P2 | P1 | *Idle* | P3 | P4 | P3 | P5 |

---

## 4. Time sharing system with time slice of 2-unit time
Standard Round Robin (RR) scheduling using a unified ready queue. Time Quantum ($Q$) = 2.

* **T = 0:** P1 gets 2 units `[0-2]`.
* **T = 2:** P1 (Rem: 3) reinserted to queue. Takes next 2 units `[2-4]`.
* **T = 3:** P2 arrives. Waits in RQ.
* **T = 4:** P1 (Rem: 1) preempted. P2 takes its 1 requested unit `[4-5]`.
* **T = 5:** P2 finishes. P1 gets 1 unit `[5-6]` & finishes. CPU Idles until T = 10.
* **T = 10:** P3 gets 2 units `[10-12]`.
* **T = 12:** P4 arrives. P3 (Rem: 9) added back to RQ. P4 & P3 cycle via 2-unit chunks.
* At **T = 15**, P5 arrives. The RQ cycles through P4, P5, P3 sequentially in chunks of 2.
* At **T = 23**, P4 finishes.
* At **T = 34**, P3 finishes.
* At **T = 38**, P5 finishes.

### Timeline
| Process block     | Interval | Remaining time after block |
|-------------------|----------|----------------------------|
| **P1**            | `0-2`    | P1 (3)                     |
| **P1**            | `2-4`    | P1 (1)                     |
| **P2**            | `4-5`    | P2 (0)                     |
| **P1**            | `5-6`    | P1 (0)                     |
| *IDLE*            | `6-10`   |                            |
| **P3**            | `10-12`  | P3 (9)                     |
| **P4**            | `12-14`  | P4 (3)                     |
| **P3**            | `14-16`  | P3 (7)                     |
| **P4**            | `16-18`  | P4 (1)                     |
| **P5**            | `18-20`  | P5 (10)                    |
| **P3**            | `20-22`  | P3 (5)                     |
| **P4**            | `22-23`  | P4 (0)                     |
| **P5**            | `23-25`  | P5 (8)                     |
| **P3**            | `25-27`  | P3 (3)                     |
| **P5**            | `27-29`  | P5 (6)                     |
| **P3**            | `29-31`  | P3 (1)                     |
| **P5**            | `31-33`  | P5 (4)                     |
| **P3**            | `33-34`  | P3 (0)                     |
| **P5**            | `34-36`  | P5 (2)                     |
| **P5**            | `36-38`  | P5 (0)                     |

---

## 5. Multiprocessing system with three processors
Assuming standard FCFS routing utilizing CPU 1, CPU 2, and CPU 3 whenever a free processor arises.

* **T = 0:** P1 arrives. Assigned to **CPU 1**. Runs `[0-5]`.
* **T = 3:** P2 arrives. Assigned to **CPU 2**. Runs `[3-4]`.
* **T = 10:** P3 arrives. Assigned to **CPU 1** (Since all CPUs are free, CPU 1 takes it). Runs `[10-21]`.
* **T = 12:** P4 arrives. Assigned to **CPU 2**. Runs `[12-17]`.
* **T = 15:** P5 arrives. Assigned to **CPU 3**. Runs `[15-27]`.

### Execution Chart (Per Processor):
| Processor | 0-3 | 3-4 | 4-5 | 5-10 | 10-12 | 12-15 | 15-17 | 17-21 | 21-27 |
|-----------|---|---|---|---|---|---|---|---|---|
| **CPU 1** | P1 | P1 | P1 | *Idle* | P3 | P3 | P3 | P3 | *Idle* |
| **CPU 2** | *Idle* | P2 | *Idle*| *Idle* | *Idle* | P4 | P4 | *Idle* | *Idle* |
| **CPU 3** | *Idle* | *Idle*| *Idle*| *Idle* | *Idle*| *Idle* | P5 | P5 | P5 |

---

## 6. Multiprocessing time sharing system with two processors and with time slice of 2-unit time
(Global Queue Round Robin across CPU 1 and CPU 2). Time slice = 2. Short jobs are multiplexed if both CPUs have work.

* **[0-4]:** P1 is the only process, cycles independently on CPU 1.
* **[4-5]:** P2 arrives. Both CPUs are engaged parallelly (CPU 1: P2, CPU 2: P1). Both finish at T=5.
* **[5-10]:** System is idle.
* **[10-12]:** P3 engages CPU 1.
* **[12-17]:** P4 arrives. CPU 1 handles P4, CPU 2 handles P3 chunks. Run in parallel.
* **[17-28]:** P5 arrives. CPU 1 and CPU 2 alternate chunks among P3, P4(finishes at 17), and P5.

### CPU Execution Blocks
#### CPU 1:
* `[0-2]` P1
* `[2-4]` P1
* `[4-5]` P2
* `[5-10]` *IDLE*
* `[10-12]` P3
* `[12-14]` P4
* `[14-16]` P4
* `[16-18]` P5
* `[18-20]` P5
* `[20-22]` P5
* `[22-24]` P5
* `[24-26]` P5
* `[26-28]` P5

#### CPU 2:
* `[0-4]` *IDLE*
* `[4-5]` P1
* `[5-12]` *IDLE*
* `[12-14]` P3
* `[14-16]` P3
* `[16-17]` P4
* `[17-19]` P3
* `[19-21]` P3
* `[21-22]` P3

**End of Report.**

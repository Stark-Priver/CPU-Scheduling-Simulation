import pandas as pd

def fcfs(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time, results = 0, []
    for p in processes:
        start = max(time, p['arrival'])
        finish = start + p['burst']
        results.append({'Process': p['id'], 'Start': start, 'Finish': finish, 'Waiting': start - p['arrival'], 'Turnaround': finish - p['arrival']})
        time = finish
    return pd.DataFrame(results)

def sjf(processes):
    time, results, ready_queue = 0, [], []
    processes = sorted(processes, key=lambda x: x['arrival'])
    while processes or ready_queue:
        ready_queue.extend([p for p in processes if p['arrival'] <= time])
        processes = [p for p in processes if p['arrival'] > time]
        if ready_queue:
            next_proc = min(ready_queue, key=lambda x: x['burst'])
            ready_queue.remove(next_proc)
            start, finish = time, time + next_proc['burst']
            results.append({'Process': next_proc['id'], 'Start': start, 'Finish': finish, 'Waiting': start - next_proc['arrival'], 'Turnaround': finish - next_proc['arrival']})
            time = finish
        else:
            time += 1
    return pd.DataFrame(results)

def priority_scheduling(processes):
    time, results, ready_queue = 0, [], []
    processes = sorted(processes, key=lambda x: x['arrival'])
    while processes or ready_queue:
        ready_queue.extend([p for p in processes if p['arrival'] <= time])
        processes = [p for p in processes if p['arrival'] > time]
        if ready_queue:
            next_proc = min(ready_queue, key=lambda x: x['priority'])
            ready_queue.remove(next_proc)
            start, finish = time, time + next_proc['burst']
            results.append({'Process': next_proc['id'], 'Start': start, 'Finish': finish, 'Waiting': start - next_proc['arrival'], 'Turnaround': finish - next_proc['arrival']})
            time = finish
        else:
            time += 1
    return pd.DataFrame(results)

def round_robin(processes, quantum):
    time, results, ready_queue = 0, [], []
    processes = sorted(processes, key=lambda x: x['arrival'])
    remaining_burst = {p['id']: p['burst'] for p in processes}
    while processes or ready_queue:
        ready_queue.extend([p for p in processes if p['arrival'] <= time])
        processes = [p for p in processes if p['arrival'] > time]
        if ready_queue:
            current_proc = ready_queue.pop(0)
            start = time
            exec_time = min(quantum, remaining_burst[current_proc['id']])
            time += exec_time
            remaining_burst[current_proc['id']] -= exec_time
            if remaining_burst[current_proc['id']] == 0:
                finish = time
                results.append({'Process': current_proc['id'], 'Start': start, 'Finish': finish, 'Waiting': finish - current_proc['arrival'] - current_proc['burst'], 'Turnaround': finish - current_proc['arrival']})
            else:
                ready_queue.append(current_proc)
        else:
            time += 1
    return pd.DataFrame(results)

def get_user_input():
    processes = []
    n = int(input("Enter the number of processes: "))
    for i in range(n):
        print(f"\nEnter details for Process {i + 1}:")
        pid = input("Process ID: ")
        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))
        priority = int(input("Priority (lower number = higher priority): "))
        processes.append({'id': pid, 'arrival': arrival, 'burst': burst, 'priority': priority})
    return processes

def main():
    print("CPU Scheduling Algorithms")
    print("1. First Come First Serve (FCFS)")
    print("2. Shortest Job First (SJF)")
    print("3. Priority Scheduling")
    print("4. Round Robin")

    choice = int(input("\nSelect an algorithm (1-4): "))
    processes = get_user_input()

    if choice == 1:
        print("\nFirst Come First Serve (FCFS):")
        print(fcfs(processes))
    elif choice == 2:
        print("\nShortest Job First (SJF):")
        print(sjf(processes))
    elif choice == 3:
        print("\nPriority Scheduling:")
        print(priority_scheduling(processes))
    elif choice == 4:
        quantum = int(input("Enter the time quantum for Round Robin: "))
        print(f"\nRound Robin (Quantum = {quantum}):")
        print(round_robin(processes, quantum))
    else:
        print("Invalid choice. Please run the program again.")

if __name__ == "__main__":
    main()

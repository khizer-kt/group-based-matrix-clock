class GroupBasedMatrixClock:
    def __init__(self, num_processes, num_groups, num_processes_per_group):
        self.num_processes = num_processes
        self.num_groups = num_groups
        self.num_processes_per_group = num_processes_per_group
        self.intra_group_clocks = [[[0] * num_processes_per_group[g] for _ in range(num_processes_per_group[g])] for g in range(num_groups)]
        self.inter_group_clock = [[0] * num_groups for _ in range(num_groups)]
        self.process_group_map = [0] * num_processes

    def update_intra_group_clock(self, process_id, event_time):
        group_id = self.process_group_map[process_id]
        self.intra_group_clocks[group_id][process_id % self.num_processes_per_group[group_id]][event_time] += 1
        print(f"Process {process_id} in Group {group_id}: Intra-group clock updated at event time {event_time}")

    def update_inter_group_clock(self, sender_group_id, receiver_group_id, event_time):
        self.inter_group_clock[sender_group_id][receiver_group_id] = max(self.inter_group_clock[sender_group_id][receiver_group_id], event_time)
        print(f"Inter-group clock updated between Group {sender_group_id} and Group {receiver_group_id} at event time {event_time}")

    def communicate(self, sender_process_id, receiver_process_id, event_time):
        sender_group_id = self.process_group_map[sender_process_id]
        receiver_group_id = self.process_group_map[receiver_process_id]
        self.update_intra_group_clock(sender_process_id, event_time)
        self.update_inter_group_clock(sender_group_id, receiver_group_id, event_time)

        print(f"Process {sender_process_id} in Group {sender_group_id} communicates with Process {receiver_process_id} in Group {receiver_group_id} at event time {event_time}")

if __name__ == "__main__":
    num_processes = 10
    num_groups = 3
    num_processes_per_group = [4, 3, 3]  

    clock = GroupBasedMatrixClock(num_processes, num_groups, num_processes_per_group)
    clock.process_group_map = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2] 
    clock.communicate(0, 5, 1)  # Process 0 communicates with process 5 at event time 1
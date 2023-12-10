# cloud-comp-lambda-function

## Serveless Function and Runtime

Serverless function and runtime to process the periodic resource use measurements.  The function should compute two stateless metrics at each point in time: the percentage of outgoing traffic bytes and the percentage of memory caching content (given by the cached and buffer memory areas). Your function should also compute a moving average utilization of each CPU over the last minute.

## Data Input

- **timestamp**: A string containing the time of the current measurement.
- **cpu_freq_current**: A float representing the current CPU frequency (in MHz).
- **cpu_percent-X**: A float representing the utilization of CPU X (in %).
- **cpu_stats-ctx_switches**: The number of context switches (voluntary + involuntary) since boot.
- **cpu_stats-interrupts**: The number of interrupts since boot.
- **cpu_stats-soft_interrupts**: The number of software interrupts since boot.
- **cpu_stats-syscalls**: The number of system calls since boot.
- **n_pids**: Number of the running PIDs.
- **virtual_memory-total**: The total physical memory.
- **virtual_memory-available**: Amount of memory that can be given instantly to processes without the system going into swap. This is calculated by summing different memory values depending on the platform and it is supposed to be used to monitor actual memory usage in a cross platform fashion.
- **virtual_memory-percent**: A float representing the memory utilization as a percentage.
- **virtual_memory-used**: Memory used, calculated differently depending on the platform and intended for informational purposes only.
- **virtual_memory-free**: Memory not being used at all that is readily available.
- **virtual_memory-active**: Memory currently in use or very recently used.
- **virtual_memory-inactive**: Memory that is marked as not used.
- **virtual_memory-buffers**: Cache for things like I/O buffers.
- **virtual_memory-cached**: Cache for things like filesystem inodes and data read from disk.
- **virtual_memory-shared**: Memory that may be simultaneously accessed by multiple processes.
- **virtual_memory-slab**: In-kernel data structures cache.
- **net_io_counters_eth0-bytes_sent1**: Number of bytes sent.
- **net_io_counters_eth0-bytes_recv1**: Number of bytes received.
- **net_io_counters_eth0-packets_sent1**: Number of packets sent.
- **net_io_counters_eth0-packets_recv1**: Number of packets received.
- **net_io_counters_eth0-errin1**: Total number of errors while receiving.
- **net_io_counters_eth0-errout1**: Total number of errors while sending.
- **net_io_counters_eth0-dropin1**: Total number of incoming packets which were dropped.
- **net_io_counters_eth0-dropout1**: Total number of outgoing packets which were dropped.
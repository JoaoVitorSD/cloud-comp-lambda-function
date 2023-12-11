from datetime import datetime, timedelta
def handler(input: dict, context: object) -> dict[str, any]:

    sent = input['net_io_counters_eth0-bytes_sent']
    received = input['net_io_counters_eth0-bytes_recv']
    cached_percent = input['virtual_memory-cached'] /  (input['virtual_memory-cached']+ input['virtual_memory-buffers'] ) * 100

    outgoing_traffic = sent/received*100

    cpus = [key for key in input.keys() if key.startswith("cpu_percent")]
    last_minute = datetime.now() - timedelta(minutes=1)

    env = context.env
    stats = None
    if env == None:
        env = {'cpu_stats': {}}
    elif not 'cpu_stats' in env:
        env['cpu_stats'] = {}
        stats = env['cpu_stats']
    else:
        stats = env['cpu_stats']
        
    timestamp_format = '%Y-%m-%d %H:%M:%S.%f'

    for cpu_stats in stats.values():
        for cpu_stat in cpu_stats:
            stat_time = datetime.strptime(cpu_stat['time'] , timestamp_format)
            if stat_time < last_minute:
                cpu_stats.remove(cpu_stat)

    for cpu in cpus:
        cpu_usage = input[cpu]
        cpu_key = f"cpu_{cpu[12:]}"
        
        if not cpu_key in stats:
            stats[cpu_key] = [{'usage':cpu_usage, 'time':input['timestamp']}]
            continue
        stats[cpu_key].append({'usage':cpu_usage, 'time':input['timestamp']})

    response = {'cached_percent': cached_percent, 'outgoing_traffic': outgoing_traffic}

    cpu_avg = []
    for cpu in stats.keys():
        cpu_stat = stats[cpu]
        cpu_stats_len = len(cpu_stat)
        if cpu_stats_len == 0:
            response[cpu] = 0
            continue
        cpu_avg.append({cpu:   sum(stat['usage'] for stat in cpu_stat ) / cpu_stats_len})
    response['pon'] = stats
    response['cpus_avg'] = cpu_avg
    return response

class MyObject:
    def __init__(self, env):
        self.env = env

context = MyObject({})
entry = {'timestamp':'2023-12-10 00:05:54.149111', 'cpu_percent-0': 2.2, 'cpu_percent-1': 3.4, 'cpu_percent-2': 1.2, 'cpu_percent-3': 0.8, 'cpu_percent-4': 1.6, 'cpu_percent-5': 1.0, 'cpu_percent-6': 0.0, 'cpu_percent-7': 1.6, 'cpu_percent-8': 0.8, 'cpu_percent-9': 0.8, 'cpu_percent-10': 0.8, 'cpu_percent-11': 1.6, 'cpu_percent-12': 1.0, 'cpu_percent-13': 1.4, 'cpu_percent-14': 1.2, 'cpu_percent-15': 0.2, 'cpu_freq_current': 2592.0, 'cpu_stats-ctx_switches': 6504024347, 'cpu_stats-interrupts': 2553770348, 'cpu_stats-soft_interrupts': 1108094753, 'cpu_stats-syscalls': 0, 'virtual_memory-total': 25202008064, 'virtual_memory-available': 15578464256, 'virtual_memory-percent': 38.2, 'virtual_memory-used': 9192042496, 'virtual_memory-free': 5453164544, 'virtual_memory-active': 11894468608, 'virtual_memory-inactive': 4946059264, 'virtual_memory-buffers': 2871951360, 'virtual_memory-cached': 7684849664, 'virtual_memory-shared': 12812288, 'virtual_memory-slab': 2580553728, 'n_pids': 789, 'net_io_counters_eth0-bytes_sent': 9628166233, 'net_io_counters_eth0-bytes_recv': 440769338917, 'net_io_counters_eth0-packets_sent': 116797637, 'net_io_counters_eth0-packets_recv': 204376042, 'net_io_counters_eth0-errin': 0, 'net_io_counters_eth0-errout': 0, 'net_io_counters_eth0-dropin': 27, 'net_io_counters_eth0-dropout': 0}
print(handler(entry,context))
entry = {'timestamp': '2023-12-10 00:05:54.149111', 'cpu_percent-0': 8.4, 'cpu_percent-1': 10.6, 'cpu_percent-2': 8.6, 'cpu_percent-3': 9.4, 'cpu_percent-4': 9.1, 'cpu_percent-5': 9.5, 'cpu_percent-6': 7.8, 'cpu_percent-7': 8.8, 'cpu_percent-8': 12.6, 'cpu_percent-9': 8.4, 'cpu_percent-10': 8.8, 'cpu_percent-11': 8.7, 'cpu_percent-12': 7.6, 'cpu_percent-13': 8.7, 'cpu_percent-14': 33.2, 'cpu_percent-15': 9.2, 'cpu_freq_current': 2592.0, 'cpu_stats-ctx_switches': 6504141412, 'cpu_stats-interrupts': 2553806591, 'cpu_stats-soft_interrupts': 1108111008, 'cpu_stats-syscalls': 0, 'virtual_memory-total': 25202008064, 'virtual_memory-available': 15512096768, 'virtual_memory-percent': 38.4, 'virtual_memory-used': 9257938944, 'virtual_memory-free': 5367758848, 'virtual_memory-active': 11962163200, 'virtual_memory-inactive': 4959592448, 'virtual_memory-buffers': 2871980032, 'virtual_memory-cached': 7704330240, 'virtual_memory-shared': 12849152, 'virtual_memory-slab': 2587594752, 'n_pids': 802, 'net_io_counters_eth0-bytes_sent': 9628190539, 'net_io_counters_eth0-bytes_recv': 440769386908, 'net_io_counters_eth0-packets_sent': 116797773, 'net_io_counters_eth0-packets_recv': 204376167, 'net_io_counters_eth0-errin': 0, 'net_io_counters_eth0-errout': 0, 'net_io_counters_eth0-dropin': 27, 'net_io_counters_eth0-dropout': 0}
print(handler(entry,context))


# print(handler(entry,context))

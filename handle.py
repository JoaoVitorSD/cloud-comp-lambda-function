from datetime import datetime, timedelta
def handler(input: dict, context: object) -> dict[str, any]:


    cpus = [key for key in input.keys() if key.startswith("cpu_percent")]
    timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
    last_execution = datetime.now() - timedelta(minutes=1)

    env = context.env
    stats = None
    output_stats = None
    if env == None:
        env = {'cpu_stats': {}}
        stats = env['cpu_stats']
    elif not 'cpu_stats' in env:
        env['cpu_stats'] = {}
        stats = env['cpu_stats']
    else:
        stats = env['cpu_stats']
    if not 'output_stats' in env:
        env['output_stats'] = []
        output_stats = env['output_stats']
    else:
        output_stats = env['output_stats']

    

    for cpu_stats in stats.values():
        for cpu_stat in cpu_stats:
            stat_time = datetime.strptime(cpu_stat['time'] , timestamp_format)
            if stat_time < last_execution:
                cpu_stats.remove(cpu_stat)

    for output_stat in output_stats:
        stat_time = datetime.strptime(output_stat['time'] , timestamp_format)
        if stat_time < last_execution:
            output_stats.remove(output_stat)

        
    for cpu in cpus:
        cpu_usage = input[cpu]
        cpu_key = f"cpu_{cpu[12:]}"
        
        if not cpu_key in stats:
            stats[cpu_key] = [{'usage':cpu_usage, 'time':input['timestamp']}]
            continue
        stats[cpu_key].append({'usage':cpu_usage, 'time':input['timestamp']})

    cached_percent = input['virtual_memory-cached'] /  (input['virtual_memory-cached']+ input['virtual_memory-buffers'] ) * 100
    outgoing_traffic = input['net_io_counters_eth0-bytes_sent']/(sum(stat['sent'] for stat in output_stats)/len(output_stats))*100
    output_stats.append({'sent':input['net_io_counters_eth0-bytes_sent'], 'time': input['timestamp']})


    response = {'cached_percent': cached_percent, 'outgoing_traffic': outgoing_traffic, 'outputs':output_stats,'virtual_memory_used': input['virtual_memory-used']/input['virtual_memory-total']}

    cpu_avg = []
    for cpu in stats.keys():
        cpu_stat = stats[cpu]
        cpu_stats_len = len(cpu_stat)
        if cpu_stats_len == 0:
            response[cpu] = 0
            continue
        cpu_avg.append({cpu:   sum(stat['usage'] for stat in cpu_stat ) / cpu_stats_len})
    response['cpu_stats'] = stats
    response['cpus_avg'] = cpu_avg
    return response

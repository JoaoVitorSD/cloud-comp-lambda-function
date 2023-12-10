import datetime
def handler(input: dict, context: object) -> dict[str, any]:

    sent = input['net_io_counters_eth0-bytes_sent']
    received = input['net_io_counters_eth0-bytes_recv']
    cached = input['virtual_memory-buffers'] + input['virtual_memory-cached']
    cached_percent = cached / sent  * 100

    outgoing_traffic = sent/received*100

    cpus = [key for key in input.keys() if key.startswith("cpu-percent")]
    last_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)
    env = context.env
    if not env:
        env = {'cpu_stats': []}
    elif not env['cpu_stats']:
        env['cpu_stats'] = []
    
    stats = env['cpu_stats']

    for cpu_stat in stats:
        if cpu_stat.time < last_minute:
            stats.remove(cpu_stat)

    for cpu in cpus:
        cpu_usage = input[cpu]
        stats.append( {f"{cpu[12:]}":{'usage':cpu_usage, 'time':input['timestamp']}})

    context.env = env

    cpu_percentage_average = sum([x.cpu_usage for x in stats]) / len(stats)
    return {'cached_percent': cached_percent, 'outgoing_traffic': outgoing_traffic, 'cpu_usage_avg': cpu_percentage_average}